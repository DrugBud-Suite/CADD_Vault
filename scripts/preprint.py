"""
preprint.py
Handles tracking and validation of preprint publications across different platforms.
"""

import re
import logging
from typing import Optional, Tuple, Dict
import requests
from services import APIServices
import backoff
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


class PreprintTracker:
    """Handles tracking preprints and their publication status across different platforms."""

    def __init__(self, api_services: APIServices):
        """
        Initialize the PreprintTracker.
        
        Args:
            api_services: Consolidated API services instance
        """
        self.api = api_services
        self.logger = logging.getLogger(__name__)

        # Configure preprint patterns
        self.preprint_patterns = {
            'arxiv': {
                'doi': r'10\.48550/arxiv\.(.+?)(?:v\d+)?$',
                'url': r'arxiv\.org/(?:abs|pdf)/(\d+\.\d+)',
                'id': r'(\d+\.\d+)'
            },
            'chemrxiv': {
                'doi': r'10\.26434/chemrxiv[.-](.+?)(?:/|$)',
                'url':
                r'chemrxiv\.org/(?:engage/)?(?:api/)?(?:download|viewer)?[^/]*/(\d+|[A-Za-z0-9-]+)',
                'id': r'([A-Za-z0-9-]+)'
            },
            'biorxiv': {
                'doi': r'10\.1101/(.+?)(?:/|$)',
                'url': r'biorxiv\.org/content/([^/]+)',
                'id': r'(\d{4}\.\d{2}\.\d{2}\.\d+)'
            }
        }

    def check_publication_status(self, url: str) -> PreprintResult:
        """
        Check if a preprint has been published in a peer-reviewed venue.
        
        Args:
            url: URL or DOI of the preprint
            
        Returns:
            PreprintResult: Container with publication status and details
        """
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
                published_doi, published_url = checker(preprint_id)

                if published_doi and published_url:
                    result.published_doi = published_doi
                    result.published_url = published_url
                    result.title = self.api.get_doi_title(published_doi)
                    result.publication_status = "published"

            return result

        except Exception as e:
            self.logger.error(
                f"Error checking publication status for {url}: {str(e)}")
            result.error = str(e)
            return result

    def _identify_preprint(self,
                           url: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Identify preprint type and extract identifier from URL.
        
        Args:
            url: Preprint URL or DOI
            
        Returns:
            Tuple[Optional[str], Optional[str]]: (preprint_type, preprint_id)
        """
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

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.RequestException, TimeoutError),
                          max_tries=3,
                          max_time=30)
    def _search_crossref_for_title(
            self,
            title: str,
            preprint_doi: Optional[str] = None) -> Optional[str]:
        """
        Search Crossref for a paper by title with exact matching.
        
        Args:
            title: Paper title to search for
            preprint_doi: Original preprint DOI to exclude from results
            
        Returns:
            Optional[str]: Published DOI if found
        """
        try:
            # First try: Direct title query
            results = self.api.crossref.works(query=title,
                                              select='DOI,title',
                                              limit=20)

            if results and 'message' in results and 'items' in results[
                    'message']:
                title_lower = title.lower().strip()
                for item in results['message']['items']:
                    if 'title' in item and item['title']:
                        result_title = item['title'][0].lower().strip()
                        if title_lower == result_title:
                            if not preprint_doi or item['DOI'].lower(
                            ) != preprint_doi.lower():
                                return item['DOI']

            # Second try: Quoted title for exact phrase matching
            results = self.api.crossref.works(query=f'"{title}"',
                                              select='DOI,title',
                                              limit=5)

            if results and 'message' in results and 'items' in results[
                    'message']:
                for item in results['message']['items']:
                    if 'title' in item and item['title']:
                        result_title = item['title'][0].lower().strip()
                        if title_lower == result_title:
                            if not preprint_doi or item['DOI'].lower(
                            ) != preprint_doi.lower():
                                return item['DOI']

            return None

        except Exception as e:
            self.logger.error(
                f"Error searching Crossref for title {title}: {str(e)}")
            return None

    def _check_arxiv(self,
                     arxiv_id: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Check if an arXiv paper has been published.
        
        Args:
            arxiv_id: arXiv identifier
            
        Returns:
            Tuple[Optional[str], Optional[str]]: (published_doi, published_url)
        """
        try:
            paper = self.api.get_arxiv_paper(arxiv_id)
            if not paper:
                return None, None

            # Check if paper has DOI in metadata
            if paper.doi:
                return paper.doi, f"https://doi.org/{paper.doi}"

            # Search Crossref by title
            if paper.title:
                self.logger.info(
                    f"Searching for published version of arXiv paper: {paper.title}"
                )
                if doi := self._search_crossref_for_title(
                        paper.title, f"arXiv:{arxiv_id}"):
                    return doi, f"https://doi.org/{doi}"

            return None, None

        except Exception as e:
            self.logger.error(
                f"Error checking arXiv publication {arxiv_id}: {str(e)}")
            return None, None

    def _check_biorxiv(self,
                       biorxiv_id: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Check if a bioRxiv paper has been published.
        
        Args:
            biorxiv_id: bioRxiv identifier
            
        Returns:
            Tuple[Optional[str], Optional[str]]: (published_doi, published_url)
        """
        try:
            biorxiv_doi = f"10.1101/{biorxiv_id}"

            # Try bioRxiv API first
            api_url = f"https://api.biorxiv.org/details/biorxiv/{biorxiv_id}"
            response = requests.get(api_url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get('collection') and data['collection']:
                    paper_data = data['collection'][0]
                    if published_doi := paper_data.get('published_doi'):
                        return published_doi, f"https://doi.org/{published_doi}"

            # Fallback to title search
            if title := self.api.get_doi_title(biorxiv_doi):
                self.logger.info(
                    f"Searching for published version of bioRxiv paper: {title}"
                )
                if doi := self._search_crossref_for_title(title, biorxiv_doi):
                    return doi, f"https://doi.org/{doi}"

            return None, None

        except Exception as e:
            self.logger.error(
                f"Error checking bioRxiv publication {biorxiv_id}: {str(e)}")
            return None, None

    def _check_chemrxiv(
            self, chemrxiv_id: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Check if a chemRxiv paper has been published.
        
        Args:
            chemrxiv_id: chemRxiv identifier
            
        Returns:
            Tuple[Optional[str], Optional[str]]: (published_doi, published_url)
        """
        try:
            chemrxiv_doi = f"10.26434/chemrxiv-{chemrxiv_id}"

            if title := self.api.get_doi_title(chemrxiv_doi):
                self.logger.info(
                    f"Searching for published version of chemRxiv paper: {title}"
                )
                if doi := self._search_crossref_for_title(title, chemrxiv_doi):
                    return doi, f"https://doi.org/{doi}"

            return None, None

        except Exception as e:
            self.logger.error(
                f"Error checking chemRxiv publication {chemrxiv_id}: {str(e)}")
            return None, None
