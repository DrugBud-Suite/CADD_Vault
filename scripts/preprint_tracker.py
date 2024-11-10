from typing import Optional, Tuple
import requests
import re
from config import calculate_similarity, normalize_doi
from api_services import CrossrefService, ArxivService
import time


class PrePrintTracker:

    def __init__(self):
        self.crossref_service = CrossrefService()
        self.arxiv_service = ArxivService()
        self.similarity_threshold = 0.8

    def identify_preprint(self,
                          url: str) -> Tuple[Optional[str], Optional[str]]:
        """
		Identify preprint type and extract identifier from URL.
		Returns tuple of (preprint_type, preprint_id).
		"""
        if not url:
            return None, None

        url = url.lower().strip()

        # Handle DOI-style URLs
        patterns = {
            'arxiv': r'10\.48550/arxiv\.(.+?)(?:v\d+)?$',
            'chemrxiv': r'10\.26434/chemrxiv[.-](.+?)(?:/|$)',
            'biorxiv': r'10\.1101/(.+?)(?:/|$)'
        }

        for preprint_type, pattern in patterns.items():
            if match := re.search(pattern, url):
                return preprint_type, match.group(1)

        # Handle traditional URLs
        if 'arxiv.org' in url:
            arxiv_id = self.arxiv_service.extract_arxiv_id(url)
            return 'arxiv', arxiv_id
        elif 'chemrxiv.org' in url:
            match = re.search(r'chemrxiv[^/]*/(\d+|[A-Za-z0-9-]+)/?$', url)
            return 'chemrxiv', match.group(1) if match else None
        elif 'biorxiv.org' in url:
            match = re.search(r'biorxiv\.org/content/([^/]+)/?$', url)
            return 'biorxiv', match.group(1) if match else None

        return None, None

    def check_published_version(
            self, preprint_url: str) -> Tuple[Optional[str], Optional[str]]:
        """
		Check if a preprint has been published.
		Returns tuple of (doi, url) if found, (None, None) otherwise.
		"""
        preprint_type, preprint_id = self.identify_preprint(preprint_url)
        if not preprint_id:
            return None, None

        checkers = {
            'arxiv': self._check_arxiv_publication,
            'chemrxiv': self._check_chemrxiv_publication,
            'biorxiv': self._check_biorxiv_publication
        }

        checker = checkers.get(preprint_type)
        if not checker:
            return None, None

        return checker(preprint_id)

    def _search_crossref_simple(
            self,
            title: str,
            preprint_doi: Optional[str] = None) -> Optional[str]:
        """
		Simplified Crossref search focusing on exact title matches.
		"""
        try:
            # Strategy 1: Direct title query
            results = self.crossref_service.crossref.works(
                query=title,  # Simple direct query
                select='DOI,title',  # Only get what we need
                limit=20  # Get more results since we're being less specific
            )

            if results and 'message' in results and 'items' in results[
                    'message']:
                # First try exact matches (case-insensitive)
                title_lower = title.lower()
                for item in results['message']['items']:
                    if 'title' in item and item['title']:
                        result_title = item['title'][0].lower()
                        if title_lower == result_title:
                            if not preprint_doi or item['DOI'].lower(
                            ) != preprint_doi.lower():
                                print(f"Found exact match: {item['DOI']}")
                                return item['DOI']

                # Then try fuzzy matches
                for item in results['message']['items']:
                    if 'title' in item and item['title']:
                        similarity = calculate_similarity(
                            title, item['title'][0])
                        if similarity >= self.similarity_threshold:
                            if not preprint_doi or item['DOI'].lower(
                            ) != preprint_doi.lower():
                                print(
                                    f"Found similar match (score: {similarity:.2f}): {item['DOI']}"
                                )
                                return item['DOI']

            # Strategy 2: Try with quoted title
            results = self.crossref_service.crossref.works(
                query=f'"{title}"',  # Exact phrase matching
                select='DOI,title',
                limit=5)

            if results and 'message' in results and 'items' in results[
                    'message']:
                for item in results['message']['items']:
                    if 'title' in item and item['title']:
                        if not preprint_doi or item['DOI'].lower(
                        ) != preprint_doi.lower():
                            print(
                                f"Found match with quoted search: {item['DOI']}"
                            )
                            return item['DOI']

            # Strategy 3: Split title into key terms
            key_terms = ' '.join(title.split()[:6])  # Use first 6 words
            results = self.crossref_service.crossref.works(query=key_terms,
                                                           select='DOI,title',
                                                           limit=20)

            if results and 'message' in results and 'items' in results[
                    'message']:
                for item in results['message']['items']:
                    if 'title' in item and item['title']:
                        similarity = calculate_similarity(
                            title, item['title'][0])
                        if similarity >= self.similarity_threshold:
                            if not preprint_doi or item['DOI'].lower(
                            ) != preprint_doi.lower():
                                print(
                                    f"Found match with key terms (score: {similarity:.2f}): {item['DOI']}"
                                )
                                return item['DOI']

            print("No matching publication found")
            return None

        except Exception as e:
            print(f"Error searching Crossref: {str(e)}")
            return None

    def _check_arxiv_publication(
            self, arxiv_id: str) -> Tuple[Optional[str], Optional[str]]:
        """Check arXiv paper publication status."""
        try:
            paper = self.arxiv_service.get_paper(arxiv_id)
            if not paper:
                return None, None

            # Check if paper has DOI in metadata
            if paper.doi:
                return paper.doi, f"https://doi.org/{paper.doi}"

            # Search Crossref by title only
            if paper.title:
                print(f"\nSearching for published version of: {paper.title}")
                doi = self._search_crossref_simple(paper.title,
                                                   f"arXiv:{arxiv_id}")
                if doi:
                    return doi, f"https://doi.org/{doi}"

            return None, None

        except Exception as e:
            print(f"Error checking arXiv publication {arxiv_id}: {str(e)}")
            return None, None

    def _check_biorxiv_publication(
            self, biorxiv_id: str) -> Tuple[Optional[str], Optional[str]]:
        """Check bioRxiv paper publication status."""
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
            title = self.crossref_service.get_doi_title(biorxiv_doi)
            if title:
                print(f"\nSearching for published version of: {title}")
                doi = self._search_crossref_simple(title, biorxiv_doi)
                if doi:
                    return doi, f"https://doi.org/{doi}"

            return None, None

        except Exception as e:
            print(f"Error checking bioRxiv publication {biorxiv_id}: {str(e)}")
            return None, None

    def _check_chemrxiv_publication(
            self, chemrxiv_id: str) -> Tuple[Optional[str], Optional[str]]:
        """Check chemRxiv paper publication status."""
        try:
            chemrxiv_doi = f"10.26434/chemrxiv-{chemrxiv_id}"
            title = self.crossref_service.get_doi_title(chemrxiv_doi)

            if title:
                print(f"\nSearching for published version of: {title}")
                doi = self._search_crossref_simple(title, chemrxiv_doi)
                if doi:
                    return doi, f"https://doi.org/{doi}"

            return None, None

        except Exception as e:
            print(
                f"Error checking chemRxiv publication {chemrxiv_id}: {str(e)}")
            return None, None
