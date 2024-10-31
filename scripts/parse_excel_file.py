import pandas as pd
import requests
import openpyxl
import re
import os
from habanero import counts, Crossref
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from github import Github
import doi as doilib
from urllib.parse import unquote
from dotenv import load_dotenv
import arxiv
import time
import json

# Load environment variables
load_dotenv()


class DataProcessor:

    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        if not self.github_token:
            raise ValueError("GitHub token not found in environment variables")
        self.crossref = Crossref(mailto=os.getenv('EMAIL', 'your@email.com'))
        self.semantic_scholar_headers = {
            'User-Agent': 'Mozilla/5.0 Academic Paper Tracker'
        }
        self.arxiv_client = arxiv.Client()

    @staticmethod
    def load_data(file_path):
        """Load and clean data from Excel file."""
        df = pd.read_excel(file_path, dtype=str)
        df.fillna('', inplace=True)
        for col in df.columns:
            df[col] = df[col].astype(str).str.strip()
        return df

    @staticmethod
    def normalize_doi(doi):
        """Normalize DOI format."""
        doi = doi.strip().rstrip(')').replace(' ', '')
        if doi.startswith('10.') and not doi.startswith('https://doi.org/'):
            doi = f'https://doi.org/{doi}'
        return doi

    def check_published_version(self, arxiv_id):
        """
        Check if an arXiv paper has been published using multiple sources.
        Returns (published_doi, published_url) if found, (None, None) if not.
        """
        try:
            # First check arXiv metadata for DOI
            search = arxiv.Search(id_list=[arxiv_id])
            paper = next(self.arxiv_client.results(search))
            if hasattr(paper, 'doi') and paper.doi:
                return paper.doi, f"https://doi.org/{paper.doi}"

            # Check Semantic Scholar
            semantic_url = f"https://api.semanticscholar.org/v1/paper/arXiv:{arxiv_id}"
            response = requests.get(semantic_url,
                                    headers=self.semantic_scholar_headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('doi'):
                    return data['doi'], f"https://doi.org/{data['doi']}"

            # Check Crossref as last resort
            try:
                title = paper.title.lower()
                authors = [
                    author.name.split()[-1].lower() for author in paper.authors
                ]
                results = self.crossref.works(
                    query=title, select=['DOI', 'title', 'author'], limit=5)

                for item in results['items']:
                    if 'title' in item and 'author' in item:
                        item_title = item['title'][0].lower() if isinstance(
                            item['title'], list) else item['title'].lower()
                        item_authors = [
                            author.get('family', '').lower()
                            for author in item['author']
                        ]

                        # Check if titles are similar and at least one author matches
                        if (self._similar_titles(title, item_title)
                                and any(author in item_authors
                                        for author in authors)):
                            return item[
                                'DOI'], f"https://doi.org/{item['DOI']}"
            except Exception as crossref_error:
                print(
                    f"Crossref lookup failed for {arxiv_id}: {str(crossref_error)}"
                )

            return None, None

        except Exception as e:
            print(
                f"Error checking publication status for arXiv:{arxiv_id}: {str(e)}"
            )
            return None, None

    @staticmethod
    def _similar_titles(title1, title2):
        """
        Check if two titles are similar enough to be considered the same paper.
        Uses a simple similarity metric based on shared words.
        """
        words1 = set(re.findall(r'\w+', title1.lower()))
        words2 = set(re.findall(r'\w+', title2.lower()))
        intersection = len(words1.intersection(words2))
        shorter_len = min(len(words1), len(words2))
        if shorter_len == 0:
            return False
        similarity = intersection / shorter_len
        return similarity > 0.8

    def fill_empty_descriptions(self, df):
        """Fill empty descriptions with arXiv titles."""
        empty_desc_mask = df['DESCRIPTION'].str.strip() == ''
        arxiv_mask = df['PUBLICATION'].str.contains('arxiv',
                                                    case=False,
                                                    na=False)
        rows_to_update = df[empty_desc_mask & arxiv_mask]

        print(
            f"Found {len(rows_to_update)} empty descriptions with arXiv links")

        for idx, row in rows_to_update.iterrows():
            arxiv_id = self.extract_arxiv_id(row['PUBLICATION'])
            if arxiv_id:
                search = arxiv.Search(id_list=[arxiv_id])
                try:
                    paper = next(self.arxiv_client.results(search))
                    df.at[idx, 'DESCRIPTION'] = paper.title
                    print(f"Updated description for {row['PUBLICATION']}")
                except Exception as e:
                    print(
                        f"Error fetching title for {row['PUBLICATION']}: {str(e)}"
                    )
            time.sleep(1)  # Rate limiting

        return df

    def update_published_papers(self, df):
        """Update arXiv papers with their published versions if available."""
        arxiv_mask = df['PUBLICATION'].str.contains('arxiv',
                                                    case=False,
                                                    na=False)
        arxiv_papers = df[arxiv_mask]

        updates = 0
        for idx, row in arxiv_papers.iterrows():
            arxiv_id = self.extract_arxiv_id(row['PUBLICATION'])
            if not arxiv_id:
                continue

            published_doi, published_url = self.check_published_version(
                arxiv_id)
            if published_doi:
                old_url = df.at[idx, 'PUBLICATION']
                df.at[idx, 'PUBLICATION'] = published_url
                updates += 1
                print(
                    f"Updated paper {arxiv_id} to published version: {published_url}"
                )
                print(f"Old URL: {old_url}")

            time.sleep(1)  # Rate limiting

        print(f"Updated {updates} papers to their published versions")
        return df

    @staticmethod
    def extract_arxiv_id(url):
        """Extract arXiv ID from URL or string."""
        arxiv_patterns = [
            r'arxiv\.org/abs/(\d+\.\d+)', r'arxiv\.org/pdf/(\d+\.\d+)',
            r'/(\d+\.\d+)$', r'arXiv:(\d+\.\d+)'
        ]

        for pattern in arxiv_patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    @staticmethod
    def fetch_citations(doi):
        """Fetch citation count for a DOI."""
        if 'doi' not in doi.lower():
            return None
        try:
            doi = unquote(doi)
            actual_doi = doi.split('10.')[1]
            actual_doi = '10.' + actual_doi
            actual_doi = actual_doi.replace('%2F', '/')
            return counts.citation_count(doi=actual_doi)
        except Exception as e:
            print(f"Citation fetch error for DOI: {doi}. Error: {str(e)}")
            return None

    def get_github_data(self, url_token):
        """Fetch GitHub repository data."""
        url, _ = url_token
        if pd.isna(url) or 'github.com' not in url:
            return None, None, None

        repo_identifier = self._clean_github_url(url)
        if not repo_identifier:
            return None, None, None

        try:
            g = Github(self.github_token)
            repo = g.get_repo(repo_identifier)
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

    @staticmethod
    def _clean_github_url(url):
        """Clean and validate GitHub URL."""
        url = url.replace('.git', '')
        match = re.match(r'https://github\.com/([^/]+)/([^/?#]+)', url)
        return f"{match.group(1)}/{match.group(2)}" if match else None

    def process_data(self, input_file, output_csv, output_excel):
        """Main processing function."""
        try:
            # Load and prepare data
            df = self.load_data(input_file)
            df['PUBLICATION'] = df['PUBLICATION'].apply(self.normalize_doi)

            # Update arXiv papers to published versions
            print("Checking for published versions of arXiv papers...")
            df = self.update_published_papers(df)

            # Fill empty descriptions with arXiv titles
            print("Filling empty descriptions...")
            df = self.fill_empty_descriptions(df)

            # Process GitHub data
            print("Processing GitHub data...")
            mask = df['CODE'].str.contains('github.com', na=False)
            urls = df[mask]['CODE'].tolist()
            tokens = [self.github_token] * len(urls)

            # Parallel processing
            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                github_results = list(
                    executor.map(self.get_github_data, zip(urls, tokens)))
                citation_results = list(
                    executor.map(self.fetch_citations, df['PUBLICATION']))

            # Update DataFrame with GitHub results
            results_df = pd.DataFrame(
                github_results,
                columns=['GITHUB_STARS', 'LAST_COMMIT', 'LAST_COMMIT_AGO'],
                index=df[mask].index)
            df.update(results_df)

            # Update citations
            df['CITATIONS'] = citation_results

            # Sort and save
            df.sort_values(
                by=['FOLDER1', 'CATEGORY1', 'SUBCATEGORY1', 'SUBSUBCATEGORY1'],
                inplace=True,
                na_position='first')
            df.to_csv(output_csv, index=False)
            df.to_excel(output_excel, index=False)

            print("Processing complete!")
            return df

        except Exception as e:
            print(f"Error during data processing: {str(e)}")
            raise


def main():
    # File paths
    input_file = '../cadd_vault_data.xlsx'
    output_csv = '../processed_cadd_vault_data.csv'
    output_excel = '../cadd_vault_data.xlsx'

    # Initialize and run processor
    processor = DataProcessor()
    processor.process_data(input_file, output_csv, output_excel)


if __name__ == "__main__":
    main()
