"""
External API services for fetching publication and repository data.
"""
import logging
import re
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache, partial
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import unquote

import backoff
import httpx
import requests
from habanero import Crossref, counts
from models import (
    Config,
    Entry,
    ProcessingResult,
    Publication,
    Repository,
)
from paperscraper.impact import Impactor
from rich.console import Console
from rich.progress import Progress


"""
Publication service that handles all publication-related functionality including preprints.
"""

import logging
from typing import Optional, Tuple, Dict, Any
import re
from urllib.parse import unquote
import httpx
import backoff
from habanero import Crossref, counts
from paperscraper.impact import Impactor
from dataclasses import dataclass

@dataclass
class PreprintResult:
    """Container for preprint checking results"""
    original_url: str
    published_doi: Optional[str] = None
    published_url: Optional[str] = None
    title: Optional[str] = None
    publication_status: str = "unpublished"
    error: Optional[str] = None

class PublicationService:
    """Handles all publication-related operations including preprints"""

    def __init__(self, config: Config):
        self.config = config
        self.headers = {
            "User-Agent": f"PublicationManager/1.0 (mailto:{config.email})"
        }
        self.logger = logging.getLogger(self.__class__.__name__)
        self.crossref = Crossref(mailto=config.email)
        self.impactor = Impactor()
        
        # Cache for impact factors and journals
        self._impact_factor_cache = {}
        self._journal_cache = {}
        
        # Preprint configuration
        self.preprint_domains = ['arxiv', 'biorxiv', 'medrxiv', 'chemrxiv', 'zenodo']
        self.preprint_patterns = {
            'arxiv': {
                'doi': r'10\.48550/arxiv\.(.+?)(?:v\d+)?$',
                'url': r'arxiv\.org/(?:abs|pdf)/(\d+\.\d+)',
                'id': r'(\d+\.\d+)'
            },
            'chemrxiv': {
                'doi': r'10\.26434/chemrxiv[.-](.+?)(?:/|$)',
                'url': r'chemrxiv\.org/(?:engage/)?(?:api/)?(?:download|viewer)?[^/]*/(\d+|[A-Za-z0-9-]+)',
                'id': r'([A-Za-z0-9-]+)'
            },
            'biorxiv': {
                'doi': r'10\.1101/(.+?)(?:/|$)',
                'url': r'biorxiv\.org/content/([^/]+)',
                'id': r'(\d{4}\.\d{2}\.\d{2}\.\d+)'
            }
        }

    def normalize_doi(self, doi: str) -> Optional[str]:
        """Normalize DOI format for consistency"""
        if not doi:
            return None

        # Convert to string and strip whitespace
        doi = str(doi).strip()

        # Extract DOI from URLs
        if 'doi.org/' in doi:
            doi = doi.split('doi.org/')[-1]
        elif 'http://' in doi or 'https://' in doi:
            match = re.search(r'(10\.\d+/.+)$', doi)
            if match:
                doi = match.group(1)

        # Clean the DOI
        old_doi = None
        while old_doi != doi:
            old_doi = doi
            doi = re.sub(r'v\d+(?:\.full)?$', '', doi)  # Remove version numbers
            doi = re.sub(r'\.full$', '', doi)  # Remove standalone .full
            doi = re.sub(r'\.(?:svg|pdf|html)$', '', doi)  # Remove file extensions
            doi = re.sub(r'[\[\(\{\]\)\}]+$', '', doi)  # Remove trailing brackets
            doi = re.sub(r'[\.:\-/\\]+$', '', doi)  # Remove trailing punctuation
            doi = doi.split('?')[0].split('#')[0]  # Remove query parameters
            doi = doi.strip()

        # Add proper DOI URL prefix if it's a bare DOI
        if doi.startswith('10.'):
            doi = f'https://doi.org/{doi}'

        return doi

    def is_preprint(self, url: str) -> bool:
        """Check if URL is from a preprint server"""
        return any(domain in url.lower() for domain in self.preprint_domains)

    def _extract_doi(self, url: str) -> Optional[str]:
        """Extract DOI from URL"""
        if not url:
            return None
            
        if 'doi.org' in url:
            doi = url.split('doi.org/')[-1]
            return re.sub(r'[)\]\.]+$', '', doi)
            
        return None

    async def check_publication_status(self, url: str) -> PreprintResult:
        """Check if a preprint has been published in a peer-reviewed venue"""
        try:
            result = PreprintResult(original_url=url)

            # Identify preprint type and ID
            preprint_type, preprint_id = self._identify_preprint(url)
            if not preprint_type or not preprint_id:
                result.error = "Could not identify preprint type or ID"
                return result

            # Check publication status based on preprint type
            checker_methods = {
                'arxiv': self._check_arxiv,
                'biorxiv': self._check_biorxiv,
                'chemrxiv': self._check_chemrxiv
            }

            if checker := checker_methods.get(preprint_type):
                published_doi, published_url = await checker(preprint_id)
                if published_doi and published_url:
                    result.published_doi = published_doi
                    result.published_url = published_url
                    result.title = await self._get_doi_title(published_doi)
                    result.publication_status = "published"

            return result

        except Exception as e:
            self.logger.error(f"Error checking publication status for {url}: {str(e)}")
            result.error = str(e)
            return result

    def _identify_preprint(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        """Identify preprint type and extract identifier from URL"""
        if not url:
            return None, None

        url = url.lower().strip()

        # Check each preprint type's patterns
        for preprint_type, patterns in self.preprint_patterns.items():
            # Check DOI pattern
            if match := re.search(patterns['doi'], url):
                return preprint_type, match.group(1)

            # Check URL pattern
            if match := re.search(patterns['url'], url):
                return preprint_type, match.group(1)

        return None, None

    async def _search_crossref_for_title(self, title: str, preprint_doi: Optional[str] = None) -> Optional[str]:
        """Search Crossref for a paper by title with exact matching"""
        try:
            # First try: Direct title query
            works = self.crossref.works(query=title, select='DOI,title', limit=20)

            if works and 'message' in works and 'items' in works['message']:
                title_lower = title.lower().strip()
                for item in works['message']['items']:
                    if 'title' in item and item['title']:
                        result_title = item['title'][0].lower().strip()
                        if title_lower == result_title:
                            if not preprint_doi or item['DOI'].lower() != preprint_doi.lower():
                                return item['DOI']

            # Second try: Quoted title for exact phrase matching
            works = self.crossref.works(query=f'"{title}"', select='DOI,title', limit=5)

            if works and 'message' in works and 'items' in works['message']:
                for item in works['message']['items']:
                    if 'title' in item and item['title']:
                        result_title = item['title'][0].lower().strip()
                        if title_lower == result_title:
                            if not preprint_doi or item['DOI'].lower() != preprint_doi.lower():
                                return item['DOI']

            return None

        except Exception as e:
            self.logger.error(f"Error searching Crossref for title {title}: {str(e)}")
            return None

    async def _check_arxiv(self, arxiv_id: str) -> Tuple[Optional[str], Optional[str]]:
        """Check if an arXiv paper has been published"""
        try:
            async with httpx.AsyncClient(timeout=self.config.timeout) as client:
                response = await client.get(
                    f"http://export.arxiv.org/api/query?id_list={arxiv_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                
                # Parse XML response (simplified for example)
                if 'doi>' in response.text:
                    doi = response.text.split('<doi>', 1)[1].split('</doi>', 1)[0]
                    return doi, f"https://doi.org/{doi}"
                
                # If no DOI in metadata, search by title
                if '<title>' in response.text:
                    title = response.text.split('<title>', 1)[1].split('</title>', 1)[0]
                    if doi := await self._search_crossref_for_title(title, f"arXiv:{arxiv_id}"):
                        return doi, f"https://doi.org/{doi}"

            return None, None

        except Exception as e:
            self.logger.error(f"Error checking arXiv publication {arxiv_id}: {str(e)}")
            return None, None

    async def _check_biorxiv(self, biorxiv_id: str) -> Tuple[Optional[str], Optional[str]]:
        """Check if a bioRxiv paper has been published"""
        try:
            biorxiv_doi = f"10.1101/{biorxiv_id}"

            async with httpx.AsyncClient(timeout=self.config.timeout) as client:
                response = await client.get(
                    f"https://api.biorxiv.org/details/biorxiv/{biorxiv_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get('collection') and data['collection']:
                    paper_data = data['collection'][0]
                    if published_doi := paper_data.get('published_doi'):
                        return published_doi, f"https://doi.org/{published_doi}"

            # Fallback to title search
            if title := await self._get_doi_title(biorxiv_doi):
                if doi := await self._search_crossref_for_title(title, biorxiv_doi):
                    return doi, f"https://doi.org/{doi}"

            return None, None

        except Exception as e:
            self.logger.error(f"Error checking bioRxiv publication {biorxiv_id}: {str(e)}")
            return None, None

    async def _check_chemrxiv(self, chemrxiv_id: str) -> Tuple[Optional[str], Optional[str]]:
        """Check if a chemRxiv paper has been published"""
        try:
            chemrxiv_doi = f"10.26434/chemrxiv-{chemrxiv_id}"

            if title := await self._get_doi_title(chemrxiv_doi):
                if doi := await self._search_crossref_for_title(title, chemrxiv_doi):
                    return doi, f"https://doi.org/{doi}"

            return None, None

        except Exception as e:
            self.logger.error(f"Error checking chemRxiv publication {chemrxiv_id}: {str(e)}")
            return None, None

    async def _get_doi_title(self, doi: str) -> Optional[str]:
        """Get title for a DOI using Crossref"""
        try:
            works = self.crossref.works(ids=[doi])
            if works and isinstance(works, dict) and 'message' in works:
                message = works['message']
                if 'title' in message and message['title']:
                    return message['title'][0]
            return None
        except Exception as e:
            self.logger.error(f"Error getting title for DOI {doi}: {str(e)}")
            return None

    @backoff.on_exception(backoff.expo,
                         (httpx.HTTPError, TimeoutError),
                         max_tries=3)
    async def get_citations(self, url: str) -> Optional[int]:
        """Get citation count using Crossref"""
        try:
            doi = self._extract_doi(url)
            if not doi:
                return None

            doi = unquote(doi)
            actual_doi = '10.' + doi.split('10.')[1]
            actual_doi = actual_doi.replace('%2F', '/')
            return counts.citation_count(doi=actual_doi)

        except Exception as e:
            self.logger.error(f"Error getting citations for DOI {doi}: {str(e)}")
            return None

    @backoff.on_exception(backoff.expo,
                         (httpx.HTTPError, TimeoutError),
                         max_tries=3)
    async def get_journal_info(self, url: str) -> Optional[Dict[str, str]]:
        """Get journal information from DOI using Crossref"""
        try:
            doi = self._extract_doi(url)
            if not doi:
                return None

            works = self.crossref.works(ids=[doi])
            if works and isinstance(works, dict) and 'message' in works:
                message = works['message']
                journal_title = None
                if 'container-title' in message and message['container-title']:
                    journal_title = message['container-title'][0]
                return {
                    'journal': journal_title,
                    'issn': message.get('ISSN', [None])[0] if message.get('ISSN') else None,
                    'issn-type': message.get('issn-type', [])
                }
            return None
        except Exception as e:
            self.logger.error(f"Error getting journal info for DOI {doi}: {str(e)}")
            return None

    async def get_impact_factor(self, journal_info: Dict[str, str]) -> Optional[float]:
        """Get journal impact factor using paperscraper"""
        try:
            journal_name = journal_info.get('journal')
            if not journal_name or self._is_excluded_journal(journal_name):
                return None

            # Check cache first
            cached_if = self._get_cached_impact_factor(journal_name)
            if cached_if is not None:
                return cached_if

            # First try exact match
            results = self.impactor.search(journal_name, threshold=100)
            if results:
                self._cache_impact_factor(journal_name, results[0]['factor'])
                return results[0]['factor']

            return None

        except Exception as e:
            self.logger.error(f"Error getting impact factor: {str(e)}")
            return None

    @lru_cache(maxsize=1000)
    def _get_cached_impact_factor(self, journal: str) -> Optional[float]:
        """Get impact factor from cache"""
        return self._impact_factor_cache.get(journal)

    def _cache_impact_factor(self, journal: str, impact_factor: float) -> None:
        """Cache impact factor for a journal"""
        self._impact_factor_cache[journal] = impact_factor

    def _is_excluded_journal(self, journal: str) -> bool:
        """
        Check if journal should be excluded from impact factor lookup.
        
        Args:
            journal: Name of the journal to check
            
        Returns:
            bool: True if journal should be excluded, False otherwise
        """
        excluded_terms = [
            'arxiv', 
            'preprint', 
            'bioRxiv', 
            'medRxiv', 
            'chemrxiv', 
            'github', 
            'blog', 
            'zenodo'
        ]
        return any(term.lower() in journal.lower() for term in excluded_terms)

    @backoff.on_exception(backoff.expo, 
                         (TimeoutError, httpx.HTTPError),
                         max_tries=3)
    async def _update_journal_info(self, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update journal information for an entry.
        
        Args:
            entry_data: Entry data dictionary
            
        Returns:
            Dict[str, Any]: Updated entry data
        """
        try:
            url = entry_data.get('publication_url')
            if not url:
                return entry_data

            journal_info = await self.get_journal_info(url)
            if not journal_info or not journal_info.get('journal'):
                return entry_data

            # Update journal name if not present
            if not entry_data.get('journal'):
                entry_data['journal'] = journal_info['journal']

            # Try to get impact factor if not present
            if not entry_data.get('impact_factor'):
                impact_factor = await self.get_impact_factor(journal_info)
                if impact_factor is not None:
                    entry_data['impact_factor'] = impact_factor

            return entry_data

        except Exception as e:
            self.logger.error(f"Error updating journal info: {str(e)}")
            return entry_data

    @backoff.on_exception(backoff.expo, 
                         (TimeoutError, httpx.HTTPError),
                         max_tries=3)
    async def _update_publication_info(self, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update all publication-related information for an entry.
        
        Args:
            entry_data: Entry data dictionary
            
        Returns:
            Dict[str, Any]: Updated entry data
        """
        try:
            url = entry_data.get('publication_url')
            if not url:
                return entry_data

            # Normalize DOI first
            normalized_url = self.normalize_doi(url)
            if not normalized_url:
                return entry_data

            entry_data['publication_url'] = normalized_url

            # Check if it's a preprint and handle accordingly
            if self.is_preprint(normalized_url):
                preprint_result = await self.check_publication_status(normalized_url)
                if preprint_result.publication_status == "published":
                    entry_data['publication_url'] = preprint_result.published_url
                    self.logger.info(
                        f"Updated preprint to published version: {preprint_result.published_url}"
                    )
                    normalized_url = preprint_result.published_url

            # Only process non-preprint publications
            if not self.is_preprint(normalized_url):
                # Update citations
                citations = await self.get_citations(normalized_url)
                if citations is not None:
                    entry_data['citations'] = citations

                # Update journal info
                entry_data = await self._update_journal_info(entry_data)

            return entry_data

        except Exception as e:
            self.logger.error(f"Error updating publication info: {str(e)}")
            return entry_data

    async def process_entries(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process a list of entries and update their publication information.
        
        Args:
            entries: List of entry data dictionaries
            
        Returns:
            List[Dict[str, Any]]: Updated entries
        """
        try:
            updated_entries = []
            for entry in entries:
                if entry.get('publication_url'):
                    entry = await self._update_publication_info(entry)
                updated_entries.append(entry)
            return updated_entries

        except Exception as e:
            self.logger.error(f"Error processing entries: {str(e)}")
            return entries

class RepositoryService:
    """Handle repository-related API calls"""

    def __init__(self, config: Config):
        self.config = config
        self.headers = {
            "User-Agent": f"PublicationManager/1.0 (mailto:{config.email})"
        }
        if config.github_token:
            self.headers["Authorization"] = f"token {config.github_token}"
        self.logger = logging.getLogger(self.__class__.__name__)

    async def process_repository_batch(self, urls: List[str]) -> List[Optional[Repository]]:
        """Process a batch of repository URLs in parallel"""
        with ProcessPoolExecutor() as executor:
            # Create partial function with self.config
            fetch_func = partial(self.get_repository_data_sync, self.config)
            # Process URLs in parallel
            results = list(executor.map(fetch_func, urls))
        return results

    @staticmethod
    def get_repository_data_sync(config: Config, url: str) -> Optional[Repository]:
        """Synchronous version of get_repository_data for multiprocessing"""
        if not url or 'github.com' not in url:
            return None

        try:
            repo_path = RepositoryService._extract_repo_path(url)
            if not repo_path:
                return None

            headers = {
                "User-Agent": f"PublicationManager/1.0 (mailto:{config.email})"
            }
            if config.github_token:
                headers["Authorization"] = f"token {config.github_token}"

            # Use synchronous requests here
            response = requests.get(
                f"https://api.github.com/repos/{repo_path}",
                headers=headers,
                timeout=config.timeout
            )
            response.raise_for_status()
            data = response.json()

            # Get last commit synchronously
            commit_response = requests.get(
                f"https://api.github.com/repos/{repo_path}/commits",
                headers=headers,
                timeout=config.timeout
            )
            commit_response.raise_for_status()
            commit_data = commit_response.json()
            last_commit = commit_data[0]["commit"]["committer"]["date"] if commit_data else None

            return Repository(
                url=url,
                stars=data.get('stargazers_count', 0),
                last_commit=last_commit,
                last_commit_ago=RepositoryService._calculate_time_ago(last_commit)
            )
        except Exception as e:
            logging.error(f"Error fetching repository data: {str(e)}")
            return None

    async def get_repository_data(self, url: str) -> Optional[Repository]:
        """Fetch repository data"""
        if not url or 'github.com' not in url:
            return None

        try:
            repo_path = self._extract_repo_path(url)
            if not repo_path:
                return None

            async with httpx.AsyncClient(timeout=self.config.timeout) as client:
                response = await client.get(
                    f"https://api.github.com/repos/{repo_path}",
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()

                return Repository(
                    url=url,
                    stars=data.get('stargazers_count', 0),
                    last_commit=await self._get_last_commit(repo_path),
                    last_commit_ago=self._calculate_time_ago(
                        await self._get_last_commit(repo_path)
                    )
                )
        except Exception as e:
            self.logger.error(f"Error fetching repository data: {str(e)}")
            return None

    @staticmethod
    def _extract_repo_path(url: str) -> Optional[str]:
        """Extract repository path from GitHub URL"""
        try:
            parts = url.split("github.com/")[1].split("/")
            return f"{parts[0]}/{parts[1]}"
        except Exception:
            return None

    async def _get_last_commit(self, repo_path: str) -> Optional[str]:
        """Get repository's last commit date"""
        try:
            async with httpx.AsyncClient(timeout=self.config.timeout) as client:
                response = await client.get(
                    f"https://api.github.com/repos/{repo_path}/commits",
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()
                if data and isinstance(data, list) and data:
                    return data[0]["commit"]["committer"]["date"]
        except Exception:
            return None
        return None

    @staticmethod
    def _calculate_time_ago(date_str: Optional[str]) -> Optional[str]:
        """Calculate time elapsed since date"""
        if not date_str:
            return None
        try:
            commit_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            diff = now - commit_date
            months = diff.days // 30
            return f"{months} months ago"
        except Exception:
            return None


class DataProcessor:
    """Process and validate publication data"""

    def __init__(
        self,
        publication_service: PublicationService,
        repository_service: RepositoryService
    ):
        self.publication_service = publication_service
        self.repository_service = repository_service
        self.console = Console()

    async def process_entries(
        self,
        raw_entries: List[Dict[str, Any]]
    ) -> Tuple[List[Entry], ProcessingResult]:
        """Process raw data into validated entries"""
        results = ProcessingResult()
        processed_entries = []

        with Progress() as progress:
            task = progress.add_task(
                "Processing entries...",
                total=len(raw_entries)
            )

            for raw_entry in raw_entries:
                try:
                    entry = Entry.from_dict(raw_entry)
                    processed_entries.append(entry)
                    results.successful_entries += 1
                except Exception as e:
                    results.failed_entries += 1
                    results.add_error(
                        raw_entry.get('name', 'Unknown'),
                        str(e)
                    )
                finally:
                    progress.update(task, advance=1)

        results.total_entries = len(raw_entries)
        return processed_entries, results