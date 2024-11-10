import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import os
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from api_services import CrossrefService, GitHubService, ArxivService
from preprint_tracker import PrePrintTracker
from config import normalize_doi
import re
import backoff
import requests


@dataclass
class ProcessingStats:
    """Statistics for data processing operations"""
    total_rows: int = 0
    dois_normalized: int = 0
    dois_failed: int = 0
    descriptions_added: int = 0
    descriptions_failed: int = 0
    preprints_checked: int = 0
    publications_found: int = 0
    publications_failed: int = 0
    arxiv_titles_found: int = 0
    arxiv_titles_failed: int = 0
    doi_titles_found: int = 0
    doi_titles_failed: int = 0

    def report(self, operation: str) -> None:
        """Print a report for the specified operation"""
        if operation == "doi_normalization":
            print("\nDOI Normalization Results:")
            print(
                f"Total DOIs processed: {self.dois_normalized + self.dois_failed}"
            )
            print(f"Successfully normalized: {self.dois_normalized}")
            print(f"Failed to normalize: {self.dois_failed}")

        elif operation == "description_filling":
            print("\n=== Description Filling Summary ===")
            print(f"ArXiv papers:")
            print(f"  - Successfully filled: {self.arxiv_titles_found}")
            print(f"  - Failed to fill: {self.arxiv_titles_failed}")
            print(f"DOI papers:")
            print(f"  - Successfully filled: {self.doi_titles_found}")
            print(f"  - Failed to fill: {self.doi_titles_failed}")
            print(
                f"Total descriptions added: {self.arxiv_titles_found + self.doi_titles_found}"
            )
            print(
                f"Total failures: {self.arxiv_titles_failed + self.doi_titles_failed}"
            )

        elif operation == "preprint_checking":
            print("\nPreprint Publication Check Results:")
            print(f"Total preprints checked: {self.preprints_checked}")
            print(f"Published versions found: {self.publications_found}")
            print(f"Failed to find publications: {self.publications_failed}")


class DataProcessor:

    def __init__(self):
        self.crossref_service = CrossrefService()
        self.github_service = GitHubService()
        self.arxiv_service = ArxivService()
        self.preprint_tracker = PrePrintTracker()
        self.stats = ProcessingStats()
        self.max_workers = 5

    def get_publication_title(self, publication_url: str) -> Optional[str]:
        """Get publication title with detailed logging."""
        if not publication_url:
            return None

        print(f"\nAttempting to fetch title for: {publication_url}")

        try:
            # Handle arXiv papers (including DOI-style arXiv URLs)
            if 'arxiv' in publication_url.lower():
                arxiv_id = None
                if '10.48550/arxiv.' in publication_url.lower():
                    arxiv_id = publication_url.lower().split(
                        '10.48550/arxiv.')[-1].strip()
                    arxiv_id = re.sub(r'v\d+$', '', arxiv_id)
                elif 'arxiv.org' in publication_url.lower():
                    arxiv_id = self.arxiv_service.extract_arxiv_id(
                        publication_url)

                if arxiv_id:
                    print(f"Extracted arXiv ID: {arxiv_id}")
                    paper = self.arxiv_service.get_paper(arxiv_id)
                    if paper:
                        print(
                            f"✓ Successfully retrieved arXiv title: {paper.title}"
                        )
                        return paper.title
                    print("✗ Failed to retrieve arXiv paper")
                else:
                    print("✗ Could not extract arXiv ID from URL")

            # Handle DOIs and journal URLs
            else:
                normalized_doi = normalize_doi(publication_url)
                if normalized_doi and 'doi.org/' in normalized_doi:
                    doi = normalized_doi.split('doi.org/')[-1]
                    print(f"Normalized DOI: {doi}")

                    title = self.crossref_service.get_doi_title(doi)
                    if title:
                        print(f"✓ Successfully retrieved DOI title: {title}")
                        return title
                    print("✗ Failed to retrieve DOI title")

        except Exception as e:
            print(f"✗ Error fetching title: {str(e)}")

        return None

    def _process_single_doi(self, entry: Tuple[str, str]) -> Optional[str]:
        """Process a single DOI entry with exponential backoff retry."""
        idx, publication = entry
        if not publication or not str(publication).strip():
            return None

        try:
            normalized = normalize_doi(publication)
            if normalized != publication:
                self.stats.dois_normalized += 1
                return normalized
        except Exception as e:
            print(f"Error normalizing DOI for entry {idx}: {str(e)}")
            self.stats.dois_failed += 1
        return None

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.RequestException, TimeoutError),
                          max_tries=5,
                          max_time=300)
    def _fill_single_description(
            self, entry: Tuple[str, str, str, str]) -> Optional[str]:
        """Process a single entry for description filling with retry logic."""
        idx, entry_name, publication, current_desc = entry
        if not publication or str(current_desc).strip():
            return None

        print(f"\nProcessing entry: {entry_name}")
        try:
            title = self.get_publication_title(publication)
            if title:
                if 'arxiv' in publication.lower():
                    self.stats.arxiv_titles_found += 1
                else:
                    self.stats.doi_titles_found += 1
                print(f"✓ Found title: {title}")
                time.sleep(1)  # Increased rate limiting
                return title
            else:
                if 'arxiv' in publication.lower():
                    self.stats.arxiv_titles_failed += 1
                else:
                    self.stats.doi_titles_failed += 1
                print(f"✗ Failed to get title")
        except Exception as e:
            print(f"Error processing entry {entry_name}: {str(e)}")
        return None

    @backoff.on_exception(backoff.expo,
                          (requests.exceptions.RequestException, TimeoutError),
                          max_tries=5,
                          max_time=300)
    def _check_single_preprint(
            self, entry: Tuple[str, str]) -> Optional[Tuple[str, str]]:
        """Check publication status for a single preprint with retry logic."""
        idx, publication = entry
        if not publication:
            return None

        try:
            doi, url = self.preprint_tracker.check_published_version(
                publication)
            if doi and doi.lower() != publication.lower():
                self.stats.publications_found += 1
                time.sleep(1)  # Increased rate limiting
                return url
            self.stats.publications_failed += 1
        except Exception as e:
            print(f"Error checking publication: {str(e)}")
            self.stats.publications_failed += 1
        return None

    def process_data(self, input_file: str, output_csv: str,
                     output_excel: str):
        """Main processing function with parallel processing for each major step."""
        try:
            # Load initial data
            print("\n=== Loading Data ===")
            df = pd.read_excel(input_file, dtype=str)
            df.fillna('', inplace=True)
            for col in df.columns:
                df[col] = df[col].astype(str).str.strip()

            # Step 1: DOI Normalization
            print("\n=== Step 1: DOI Normalization ===")
            publication_mask = df['PUBLICATION'].notna(
            ) & df['PUBLICATION'].str.strip().ne('')
            publication_entries = list(
                zip(df[publication_mask].index,
                    df[publication_mask]['PUBLICATION']))

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                normalized_dois = list(
                    executor.map(self._process_single_doi,
                                 publication_entries))

            # Update normalized DOIs
            for idx, doi in zip(df[publication_mask].index, normalized_dois):
                if doi:
                    df.at[idx, 'PUBLICATION'] = doi

            self.stats.report("doi_normalization")
            df.to_excel(input_file, index=False)

            # Step 2: Description Filling
            print("\n=== Step 2: Description Filling ===")
            empty_desc_mask = df['DESCRIPTION'].fillna('').str.strip() == ''
            desc_entries = list(
                zip(df[empty_desc_mask].index,
                    df[empty_desc_mask]['ENTRY NAME'],
                    df[empty_desc_mask]['PUBLICATION'],
                    df[empty_desc_mask]['DESCRIPTION']))

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                new_descriptions = list(
                    executor.map(self._fill_single_description, desc_entries))

            # Update descriptions
            for idx, desc in zip(df[empty_desc_mask].index, new_descriptions):
                if desc:
                    df.at[idx, 'DESCRIPTION'] = desc

            self.stats.report("description_filling")
            df.to_excel(input_file, index=False)

            # Step 3: Preprint Publication Check
            print("\n=== Step 3: Preprint Publication Check ===")
            preprint_mask = df['PUBLICATION'].str.contains(
                r'10\.48550/arxiv\.|10\.26434/chemrxiv[.-]|10\.1101/',
                case=False,
                na=False)
            preprint_entries = list(
                zip(df[preprint_mask].index, df[preprint_mask]['PUBLICATION']))

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                published_urls = list(
                    executor.map(self._check_single_preprint,
                                 preprint_entries))

            # Update published versions
            for idx, url in zip(df[preprint_mask].index, published_urls):
                if url:
                    df.at[idx, 'PUBLICATION'] = url

            self.stats.report("preprint_checking")
            df.to_excel(input_file, index=False)

            # Step 4: GitHub Data Processing (existing implementation)
            print("\n=== Step 4: Processing GitHub Data ===")
            github_mask = df['CODE'].str.contains('github.com', na=False)
            urls = df[github_mask]['CODE'].tolist()

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                github_results = list(
                    executor.map(self.github_service.get_repository_data,
                                 urls))
                citation_results = list(
                    executor.map(self.crossref_service.fetch_citations,
                                 df['PUBLICATION']))

            # Update DataFrame with GitHub and citation data
            results_df = pd.DataFrame(
                github_results,
                columns=['GITHUB_STARS', 'LAST_COMMIT', 'LAST_COMMIT_AGO'],
                index=df[github_mask].index)
            df.update(results_df)
            df['CITATIONS'] = citation_results

            # Final sort and save
            print("\n=== Final Processing and Save ===")
            df.sort_values(
                by=['FOLDER1', 'CATEGORY1', 'SUBCATEGORY1', 'SUBSUBCATEGORY1'],
                inplace=True,
                na_position='first')

            df.to_csv(output_csv, index=False)
            df.to_excel(output_excel, index=False)
            print("\nSaved final results:")
            print(f"CSV: {output_csv}")
            print(f"Excel: {output_excel}")

            print("\n✓ Processing complete!")
            return df

        except Exception as e:
            print(f"\n✗ Error during data processing: {str(e)}")
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
