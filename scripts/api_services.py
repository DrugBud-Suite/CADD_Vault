import requests
from github import Github
from habanero import Crossref, counts
from datetime import datetime, timezone
import arxiv
from config import EMAIL, GITHUB_TOKEN, HEADERS, DEFAULT_TIMEOUT
import re
from urllib.parse import unquote


class CrossrefService:

    def __init__(self):
        self.crossref = Crossref(mailto=EMAIL)

    def get_doi_title(self, doi):
        """Fetch paper title from DOI."""
        try:
            if 'doi.org' in doi:
                doi = doi.split('doi.org/')[-1]
            doi = re.sub(r'[)\]\.]+$', '', doi)

            url = f'https://api.crossref.org/works/{doi}'
            response = requests.get(url,
                                    headers=HEADERS,
                                    timeout=DEFAULT_TIMEOUT)

            if response.status_code == 200:
                data = response.json()
                if 'message' in data and 'title' in data['message']:
                    return data['message']['title'][0]
            return None
        except Exception as e:
            print(f"Error fetching title for DOI {doi}: {str(e)}")
            return None

    def fetch_citations(self, doi):
        """Fetch citation count for a DOI."""
        if 'doi' not in str(doi).lower():
            return None
        try:
            doi = unquote(doi)
            actual_doi = '10.' + doi.split('10.')[1]
            actual_doi = actual_doi.replace('%2F', '/')
            return counts.citation_count(doi=actual_doi)
        except Exception as e:
            print(f"Citation fetch error for DOI: {doi}. Error: {str(e)}")
            return None


class ArxivService:

    def __init__(self):
        self.client = arxiv.Client(page_size=1, delay_seconds=3, num_retries=5)

    def get_paper(self, arxiv_id):
        """Fetch paper details from arXiv."""
        try:
            search = arxiv.Search(id_list=[arxiv_id])
            return next(self.client.results(search))
        except Exception as e:
            print(f"Error fetching arXiv paper {arxiv_id}: {str(e)}")
            return None

    @staticmethod
    def extract_arxiv_id(url):
        """Extract arXiv ID from URL."""
        patterns = [
            r'arxiv\.org/abs/(\d+\.\d+)', r'arxiv\.org/pdf/(\d+\.\d+)',
            r'/(\d+\.\d+)$', r'arXiv:(\d+\.\d+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None


class GitHubService:

    def __init__(self):
        if not GITHUB_TOKEN:
            raise ValueError("GitHub token not found in environment variables")
        self.github = Github(GITHUB_TOKEN)

    def get_repository_data(self, url):
        """Fetch GitHub repository data."""
        if not url or 'github.com' not in url:
            return None, None, None

        try:
            # Clean URL and get repo identifier
            url = url.replace('.git', '')
            match = re.match(r'https://github\.com/([^/]+)/([^/?#]+)', url)
            if not match:
                return None, None, None

            repo_identifier = f"{match.group(1)}/{match.group(2)}"
            repo = self.github.get_repo(repo_identifier)

            # Get repository data
            stars = repo.stargazers_count
            last_commit = repo.get_commits()[0].commit.committer.date
            last_commit = last_commit.replace(tzinfo=timezone.utc)
            formatted_date = last_commit.strftime('%m/%Y')
            time_delta = datetime.now(timezone.utc) - last_commit
            time_delta_months = time_delta.days // 30

            return stars, formatted_date, f"{time_delta_months} months ago"
        except Exception as e:
            print(f"GitHub data fetch error for URL: {url}. Error: {str(e)}")
            return None, None, None
