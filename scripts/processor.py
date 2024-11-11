# processor.py
"""
processor.py
Main data processing logic for handling research paper data.
"""

import pandas as pd
import logging
from typing import Dict, Optional, List, Tuple
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from services import APIServices
from preprint import PreprintTracker
import threading
from pathlib import Path


@dataclass
class ProcessingStats:
    """Track statistics for data processing operations"""
    total_rows: int = 0
    processed_rows: int = 0
    failed_rows: int = 0
    citations_found: int = 0
    github_processed: int = 0
    preprints_checked: int = 0
    dois_normalized: int = 0

    def __post_init__(self):
        self._lock = threading.Lock()

    def increment(self, field: str):
        """Thread-safe increment of statistics"""
        with self._lock:
            current_value = getattr(self, field)
            setattr(self, field, current_value + 1)

    def report(self):
        """Generate processing report"""
        return {
            "Total Rows": self.total_rows,
            "Successfully Processed": self.processed_rows,
            "Failed": self.failed_rows,
            "Citations Retrieved": self.citations_found,
            "GitHub Repos Processed": self.github_processed,
            "Preprints Checked": self.preprints_checked,
            "DOIs Normalized": self.dois_normalized
        }


class DataProcessor:
    """Handles the processing of research paper data including citations, GitHub stats, and preprint tracking."""

    def __init__(self, api_services: APIServices, max_workers: int = 5):
        """
        Initialize the data processor.
        
        Args:
            api_services: Consolidated API services instance
            max_workers: Maximum number of concurrent workers
        """
        self.api = api_services
        self.max_workers = max_workers
        self.preprint_tracker = PreprintTracker(api_services)
        self.stats = ProcessingStats()
        self.logger = logging.getLogger(__name__)

    def process_data(self, input_file: str, output_csv: str,
                     output_excel: str) -> pd.DataFrame:
        """
        Main processing function that handles all data processing steps.
        
        Args:
            input_file: Path to input Excel file
            output_csv: Path to output CSV file
            output_excel: Path to output Excel file
            
        Returns:
            pd.DataFrame: Processed data
        """
        try:
            # Load and prepare data
            self.logger.info("Loading data...")
            df = pd.read_excel(input_file, dtype=str)
            df.fillna('', inplace=True)
            self.stats.total_rows = len(df)

            # Clean and normalize data
            df = self._clean_dataframe(df)

            # Process in stages
            df = self._process_dois(df)
            df = self._check_preprints(df)
            df = self._process_github_data(df)
            df = self._process_citations(df)

            # Sort and save results
            df = self._sort_and_save(df, output_csv, output_excel)

            # Report processing statistics
            self._report_results()

            return df

        except Exception as e:
            self.logger.error(f"Error during data processing: {str(e)}")
            raise

    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and normalize DataFrame columns"""
        try:
            # Strip whitespace from all string columns
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].astype(str).str.strip()

            # Normalize column names
            df.columns = [col.upper() for col in df.columns]

            # Ensure required columns exist
            required_columns = {
                'ENTRY NAME', 'PUBLICATION', 'CODE', 'DESCRIPTION', 'FOLDER1',
                'CATEGORY1'
            }
            missing_columns = required_columns - set(df.columns)
            if missing_columns:
                raise ValueError(
                    f"Missing required columns: {missing_columns}")

            return df

        except Exception as e:
            self.logger.error(f"Error cleaning DataFrame: {str(e)}")
            raise

    def _process_dois(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process and normalize DOIs"""
        try:
            dois = df[df['PUBLICATION'].notna()]['PUBLICATION']
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_doi = {
                    executor.submit(self.api.normalize_doi, doi): idx
                    for idx, doi in dois.items()
                }

                for future in as_completed(future_to_doi):
                    try:
                        idx = future_to_doi[future]
                        normalized_doi = future.result()
                        if normalized_doi:
                            df.at[idx, 'PUBLICATION'] = normalized_doi
                            self.stats.increment('dois_normalized')
                    except Exception as e:
                        self.logger.error(
                            f"Error normalizing DOI at index {idx}: {str(e)}")

            return df

        except Exception as e:
            self.logger.error(f"Error processing DOIs: {str(e)}")
            raise

    def _process_github_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process GitHub repository data"""
        try:
            github_mask = df['CODE'].str.contains('github.com', na=False)
            github_urls = df[github_mask]['CODE']

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_url = {
                    executor.submit(self.api.get_github_data, url): idx
                    for idx, url in github_urls.items()
                }

                for future in as_completed(future_to_url):
                    try:
                        idx = future_to_url[future]
                        stars, last_commit, time_ago = future.result()
                        if any(x is not None
                               for x in (stars, last_commit, time_ago)):
                            df.at[idx, 'GITHUB_STARS'] = stars
                            df.at[idx, 'LAST_COMMIT'] = last_commit
                            df.at[idx, 'LAST_COMMIT_AGO'] = time_ago
                            self.stats.increment('github_processed')
                    except Exception as e:
                        self.logger.error(
                            f"Error processing GitHub data at index {idx}: {str(e)}"
                        )

            return df

        except Exception as e:
            self.logger.error(f"Error processing GitHub data: {str(e)}")
            raise

    def _process_citations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process citation data"""
        try:
            dois = df[df['PUBLICATION'].notna()]['PUBLICATION']
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_doi = {
                    executor.submit(self.api.get_citations, doi): idx
                    for idx, doi in dois.items()
                }

                for future in as_completed(future_to_doi):
                    try:
                        idx = future_to_doi[future]
                        citations = future.result()
                        if citations is not None:
                            df.at[idx, 'CITATIONS'] = citations
                            self.stats.increment('citations_found')
                    except Exception as e:
                        self.logger.error(
                            f"Error processing citations at index {idx}: {str(e)}"
                        )

            return df

        except Exception as e:
            self.logger.error(f"Error processing citations: {str(e)}")
            raise

    def _check_preprints(self, df: pd.DataFrame) -> pd.DataFrame:
        """Check preprint publication status"""
        try:
            preprint_mask = df['PUBLICATION'].str.contains(
                r'10\.48550/arxiv\.|10\.26434/chemrxiv[.-]|10\.1101/',
                case=False,
                na=False)
            preprints = df[preprint_mask]['PUBLICATION']

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_preprint = {
                    executor.submit(
                        self.preprint_tracker.check_publication_status, url):
                    idx
                    for idx, url in preprints.items()
                }

                for future in as_completed(future_to_preprint):
                    try:
                        idx = future_to_preprint[future]
                        result = future.result()
                        if result.published_url:
                            df.at[idx, 'PUBLICATION'] = result.published_url
                            self.stats.increment('preprints_checked')
                    except Exception as e:
                        self.logger.error(
                            f"Error checking preprint at index {idx}: {str(e)}"
                        )

            return df

        except Exception as e:
            self.logger.error(f"Error checking preprints: {str(e)}")
            raise

    def _sort_and_save(self, df: pd.DataFrame, output_csv: str,
                       output_excel: str) -> pd.DataFrame:
        """Sort and save processed data"""
        try:
            # Sort by specified columns
            sort_columns = [
                'FOLDER1', 'CATEGORY1', 'SUBCATEGORY1', 'SUBSUBCATEGORY1'
            ]
            df = df.sort_values(by=sort_columns, na_position='first')

            # Save to CSV and Excel
            df.to_csv(output_csv, index=False)
            df.to_excel(output_excel, index=False)

            self.logger.info(
                f"Saved processed data to {output_csv} and {output_excel}")
            return df

        except Exception as e:
            self.logger.error(f"Error saving processed data: {str(e)}")
            raise

    def _report_results(self):
        """Generate and log processing report"""
        report = self.stats.report()
        self.logger.info("\nProcessing Results:")
        for key, value in report.items():
            self.logger.info(f"{key}: {value}")
