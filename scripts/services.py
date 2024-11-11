"""
services.py
Consolidated API services for external integrations including Crossref, arXiv, and GitHub.
"""

import os
from typing import Optional, Tuple, Dict, Any, List
import requests
import re
from datetime import datetime, timezone
import arxiv
from github import Github
from habanero import Crossref, counts
from urllib.parse import unquote
import backoff
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging


class APIServices:
    """
    Consolidated API services for external integrations.
    Handles all external API calls with proper error handling and rate limiting.
    """

    def __init__(self,
                 email: str,
                 github_token: str,
                 max_workers: int = 5,
                 timeout: int = 30):
        """
        Initialize API services with necessary credentials.
        
        Args:
            email: Email for API identification
            github_token: GitHub authentication token
            max_workers: Maximum number of concurrent workers for batch operations
            timeout: Default timeout for API requests in seconds
        """
        self.email = email
        self.timeout = timeout
        self.max_workers = max_workers
        self.headers = {'User-Agent': f'PrePrintTracker/1.0 (mailto:{email})'}

        # Initialize API clients
        self.crossref = Crossref(mailto=email)
        self.github = Github(github_token) if github_token else None
        self.arxiv_client = arxiv.Client(page_size=1,
                                         delay_seconds=3,
                                         num_retries=5)

        # Configure logging
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.RequestException, TimeoutError),
                          max_tries=5,
                          max_time=300)
    def get_doi_title(self, doi: str) -> Optional[str]:
        """
        Fetch paper title from DOI with retry logic.
        
        Args:
            doi: DOI string to look up
            
        Returns:
            Optional[str]: Paper title if found, None otherwise
        """
        try:
            if not doi:
                return None

            # Clean DOI
            if 'doi.org' in doi:
                doi = doi.split('doi.org/')[-1]
            doi = re.sub(r'[)\]\.]+$', '', doi)

            # Make API request
            url = f'https://api.crossref.org/works/{doi}'
            response = requests.get(url,
                                    headers=self.headers,
                                    timeout=self.timeout)

            if response.status_code == 200:
                data = response.json()
                if 'message' in data and 'title' in data['message']:
                    return data['message']['title'][0]

            self.logger.warning(f"No title found for DOI: {doi}")
            return None

        except Exception as e:
            self.logger.error(f"Error fetching title for DOI {doi}: {str(e)}")
            return None

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.RequestException, TimeoutError),
                          max_tries=5,
                          max_time=300)
    def get_citations(self, doi: str) -> Optional[int]:
        """
        Fetch citation count for a DOI with retry logic.
        
        Args:
            doi: DOI string to look up
            
        Returns:
            Optional[int]: Citation count if found, None otherwise
        """
        if 'doi' not in str(doi).lower():
            return None

        try:
            doi = unquote(doi)
            actual_doi = '10.' + doi.split('10.')[1]
            actual_doi = actual_doi.replace('%2F', '/')
            return counts.citation_count(doi=actual_doi)

        except Exception as e:
            self.logger.error(
                f"Citation fetch error for DOI: {doi}. Error: {str(e)}")
            return None

    def get_arxiv_paper(self, arxiv_id: str) -> Optional[arxiv.Result]:
        """
        Fetch paper details from arXiv.
        
        Args:
            arxiv_id: arXiv paper identifier
            
        Returns:
            Optional[arxiv.Result]: arXiv paper details if found, None otherwise
        """
        try:
            search = arxiv.Search(id_list=[arxiv_id])
            return next(self.arxiv_client.results(search))

        except Exception as e:
            self.logger.error(
                f"Error fetching arXiv paper {arxiv_id}: {str(e)}")
            return None

    def extract_arxiv_id(self, url: str) -> Optional[str]:
        """
        Extract arXiv ID from various URL formats.
        
        Args:
            url: URL potentially containing an arXiv ID
            
        Returns:
            Optional[str]: Extracted arXiv ID if found, None otherwise
        """
        patterns = [
            r'arxiv\.org/abs/(\d+\.\d+)', r'arxiv\.org/pdf/(\d+\.\d+)',
            r'/(\d+\.\d+)$', r'arXiv:(\d+\.\d+)',
            r'10\.48550/arxiv\.(.+?)(?:v\d+)?$'
        ]

        for pattern in patterns:
            if match := re.search(pattern, url):
                return match.group(1)
        return None

    def get_github_data(
            self,
            url: str) -> Tuple[Optional[int], Optional[str], Optional[str]]:
        """
        Fetch GitHub repository data including stars and commit information.
        
        Args:
            url: GitHub repository URL
            
        Returns:
            Tuple[Optional[int], Optional[str], Optional[str]]: 
            (star count, last commit date, time since last commit)
        """
        if not url or 'github.com' not in url:
            return None, None, None

        if not self.github:
            self.logger.error("GitHub token not configured")
            return None, None, None

        try:
            # Clean URL and extract repo identifier
            url = url.replace('.git', '')
            match = re.match(r'https://github\.com/([^/]+)/([^/?#]+)', url)
            if not match:
                return None, None, None

            repo_identifier = f"{match.group(1)}/{match.group(2)}"
            repo = self.github.get_repo(repo_identifier)

            # Get repository stats
            stars = repo.stargazers_count
            last_commit = repo.get_commits()[0].commit.committer.date
            last_commit = last_commit.replace(tzinfo=timezone.utc)
            formatted_date = last_commit.strftime('%m/%Y')

            # Calculate time since last commit
            time_delta = datetime.now(timezone.utc) - last_commit
            time_delta_months = time_delta.days // 30

            return stars, formatted_date, f"{time_delta_months} months ago"

        except Exception as e:
            self.logger.error(
                f"GitHub data fetch error for URL: {url}. Error: {str(e)}")
            return None, None, None

    def batch_process_citations(self,
                                dois: List[str]) -> Dict[str, Optional[int]]:
        """
        Process multiple DOIs concurrently to get citation counts.
        
        Args:
            dois: List of DOIs to process
            
        Returns:
            Dict[str, Optional[int]]: Dictionary mapping DOIs to their citation counts
        """
        results = {}

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_doi = {
                executor.submit(self.get_citations, doi): doi
                for doi in dois if doi
            }

            for future in as_completed(future_to_doi):
                doi = future_to_doi[future]
                try:
                    citation_count = future.result()
                    results[doi] = citation_count
                except Exception as e:
                    self.logger.error(
                        f"Error processing citations for {doi}: {str(e)}")
                    results[doi] = None

        return results

    def batch_process_github_data(
        self, urls: List[str]
    ) -> Dict[str, Tuple[Optional[int], Optional[str], Optional[str]]]:
        """
        Process multiple GitHub repository URLs concurrently.
        
        Args:
            urls: List of GitHub repository URLs to process
            
        Returns:
            Dict[str, Tuple]: Dictionary mapping URLs to their repository data
        """
        results = {}

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {
                executor.submit(self.get_github_data, url): url
                for url in urls if url and 'github.com' in url
            }

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    stars, last_commit, time_ago = future.result()
                    results[url] = (stars, last_commit, time_ago)
                except Exception as e:
                    self.logger.error(
                        f"Error processing GitHub data for {url}: {str(e)}")
                    results[url] = (None, None, None)

        return results

    def normalize_doi(self, doi: str) -> Optional[str]:
        """
        Normalize DOI format for consistency.
        
        Args:
            doi: DOI string to normalize
            
        Returns:
            Optional[str]: Normalized DOI if valid, None otherwise
        """
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
            doi = re.sub(r'v\d+(?:\.full)?$', '',
                         doi)  # Remove version numbers
            doi = re.sub(r'\.full$', '', doi)  # Remove standalone .full
            doi = re.sub(r'\.(?:svg|pdf|html)$', '',
                         doi)  # Remove file extensions
            doi = re.sub(r'[\[\(\{\]\)\}]+$', '',
                         doi)  # Remove trailing brackets
            doi = re.sub(r'[\.:\-/\\]+$', '',
                         doi)  # Remove trailing punctuation
            doi = doi.split('?')[0].split('#')[0]  # Remove query parameters
            doi = doi.strip()

        # Add proper DOI URL prefix if it's a bare DOI
        if doi.startswith('10.'):
            doi = f'https://doi.org/{doi}'

        return doi

    def validate_url(self, url: str) -> bool:
        """
        Validate if a URL is accessible.
        
        Args:
            url: URL to validate
            
        Returns:
            bool: True if URL is accessible, False otherwise
        """
        try:
            response = requests.head(url,
                                     timeout=self.timeout,
                                     allow_redirects=True)
            return response.status_code == 200
        except Exception:
            return False
