import pandas as pd
import os
import shutil
import requests
import re
import yaml
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import logging
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class ProcessingConfig:
    docs_dir: Path
    readme_path: Path
    keep_files: Set[str] = frozenset(
        {'CONTRIBUTING.md', 'index.md', 'LogoV1.png', 'images'})
    timeout: int = 10
    max_workers: int = 10


class UrlValidator:

    def __init__(self, timeout: int):
        self.timeout = timeout
        self.session = requests.Session()

    @lru_cache(maxsize=1000)
    def check_url(self, url: str) -> str:
        """Check if a URL is accessible. Results are cached."""
        try:
            response = self.session.head(url,
                                         timeout=self.timeout,
                                         allow_redirects=True)
            return "online" if response.status_code == 200 else "offline"
        except requests.RequestException:
            return "offline"


class GithubUrlProcessor:

    @staticmethod
    def clean_url(url: str) -> Optional[str]:
        """Clean and validate GitHub URLs."""
        # Remove trailing slashes and .git extension
        url = url.rstrip('/')
        url = url.replace('.git', '')

        # Try to match the GitHub URL pattern
        match = re.match(r'https?://github\.com/([^/]+/[^/?#]+)', url)
        return match.group(1) if match else None


class BadgeGenerator:

    @staticmethod
    def github_badges(repo_path: str, url: str) -> str:
        """Generate GitHub-specific badges."""
        return (
            f"\t[![Code](https://img.shields.io/github/stars/{repo_path}?"
            f"style=for-the-badge&logo=github)]({url}) "
            f"[![Last Commit](https://img.shields.io/github/last-commit/{repo_path}?"
            f"style=for-the-badge&logo=github)]({url}) ")

    @staticmethod
    def publication_badge(url: str, citations: str) -> str:
        """Generate publication badge."""
        logo = 'arxiv' if 'rxiv' in url else 'bookstack'
        return (
            f"[![Publication](https://img.shields.io/badge/Publication-"
            f"Citations:{citations}-blue?style=for-the-badge&logo={logo})]({url}) "
        )

    @staticmethod
    def status_badge(url: str, status: str, badge_type: str) -> str:
        """Generate status badge for webserver or link."""
        if status == 'online':
            return (
                f"[![{badge_type}](https://img.shields.io/badge/{badge_type}-online-"
                f"brightgreen?style=for-the-badge&logo=cachet&logoColor=65FF8F)]({url}) "
            )
        return (
            f"[![{badge_type}](https://img.shields.io/badge/{badge_type}-offline-"
            f"red?style=for-the-badge&logo=xamarin&logoColor=red)]({url}) ")


class MarkdownWriter:

    def __init__(self, url_validator: UrlValidator,
                 badge_generator: BadgeGenerator):
        self.url_validator = url_validator
        self.badge_generator = badge_generator

    def update_file(self, file_path: Path, content: str,
                    headers: Dict[str, str]) -> None:
        """Update a Markdown file with new content and headers."""
        header_written = self._check_existing_headers(file_path, headers)

        with open(file_path,
                  'a+' if file_path.exists() else 'w',
                  encoding='utf-8') as f:
            # Only write page icon if it exists and isn't NaN
            if not header_written['icon'] and headers.get(
                    'page_icon') and pd.notna(headers['page_icon']):
                f.write(f"---\nicon: {headers['page_icon']}\n---\n\n")

            # Write subcategory header only if it exists and isn't NaN
            if not header_written['subcategory'] and headers.get(
                    'subcategory') and pd.notna(headers['subcategory']):
                f.write(f"\n## **{headers['subcategory']}**\n")

            # Write subsubcategory header only if it exists and isn't NaN
            if not header_written['subsubcategory'] and headers.get(
                    'subsubcategory') and pd.notna(headers['subsubcategory']):
                f.write(f"### **{headers['subsubcategory']}**\n")

            f.write(content)

    def _check_existing_headers(self, file_path: Path,
                                headers: Dict[str, str]) -> Dict[str, bool]:
        """Check which headers already exist in the file."""
        if not file_path.exists():
            return {
                'icon': False,
                'subcategory': False,
                'subsubcategory': False
            }

        content = file_path.read_text(encoding='utf-8')
        return {
            'icon':
            "---" in content,
            'subcategory':
            (headers.get('subcategory') and pd.notna(headers['subcategory'])
             and f"## **{headers['subcategory']}**" in content),
            'subsubcategory':
            (headers.get('subsubcategory')
             and pd.notna(headers['subsubcategory'])
             and f"### **{headers['subsubcategory']}**" in content)
        }


class DocumentationGenerator:

    def __init__(self, config: ProcessingConfig):
        self.config = config
        self.url_validator = UrlValidator(config.timeout)
        self.badge_generator = BadgeGenerator()
        self.markdown_writer = MarkdownWriter(self.url_validator,
                                              self.badge_generator)
        self.validation_stats = {
            'processed': 0,
            'skipped_no_entry_name': 0,
            'skipped_no_folder': 0,
            'skipped_no_category': 0,
            'missing_subcategory': 0,
            'missing_subsubcategory': 0
        }

    def generate(self, df: pd.DataFrame) -> Tuple[int, int, int]:
        """Generate documentation from DataFrame."""
        self._clear_directory()

        # Validate required fields first
        valid_entries = self._validate_dataframe(df)

        with ThreadPoolExecutor(
                max_workers=self.config.max_workers) as executor:
            list(
                executor.map(self._process_folder,
                             valid_entries.groupby('FOLDER1')))

        self._report_statistics()

        return (len(df['PUBLICATION'].dropna()), len(df['CODE'].dropna()),
                len(df['WEBSERVER'].dropna()))

    def _clear_directory(self) -> None:
        """Clear the docs directory except for specified files."""
        try:
            if not self.config.docs_dir.exists():
                logging.warning(
                    f"Documentation directory {self.config.docs_dir} does not exist. Creating it."
                )
                self.config.docs_dir.mkdir(parents=True)
                return

            for item in os.listdir(self.config.docs_dir):
                if item not in self.config.keep_files:
                    path = self.config.docs_dir / item
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
        except Exception as e:
            logging.error(f"Error clearing directory: {str(e)}")
            raise

    def _validate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate DataFrame and log issues with entries."""
        valid_entries = df.copy()

        # Check for missing required fields
        for idx, row in df.iterrows():
            if pd.isna(row['ENTRY NAME']):
                logging.warning(
                    f"Row {idx}: Entry skipped - missing ENTRY NAME")
                self.validation_stats['skipped_no_entry_name'] += 1
                valid_entries = valid_entries.drop(idx)
                continue

            if pd.isna(row['FOLDER1']):
                logging.warning(
                    f"Row {idx}: Entry '{row['ENTRY NAME']}' skipped - missing FOLDER1"
                )
                self.validation_stats['skipped_no_folder'] += 1
                valid_entries = valid_entries.drop(idx)
                continue

            if pd.isna(row['CATEGORY1']):
                logging.warning(
                    f"Row {idx}: Entry '{row['ENTRY NAME']}' skipped - missing CATEGORY1"
                )
                self.validation_stats['skipped_no_category'] += 1
                valid_entries = valid_entries.drop(idx)
                continue

            # Log missing optional fields
            if pd.isna(row['SUBCATEGORY1']):
                self.validation_stats['missing_subcategory'] += 1

            if pd.isna(row['SUBSUBCATEGORY1']):
                self.validation_stats['missing_subsubcategory'] += 1

            self.validation_stats['processed'] += 1

        return valid_entries

    def _report_statistics(self) -> None:
        """Report statistics about processed and skipped entries."""
        logging.info("\nDocumentation Generation Statistics:")
        logging.info(
            f"Total entries processed: {self.validation_stats['processed']}")
        logging.info(
            f"Entries skipped due to missing ENTRY NAME: {self.validation_stats['skipped_no_entry_name']}"
        )
        logging.info(
            f"Entries skipped due to missing FOLDER1: {self.validation_stats['skipped_no_folder']}"
        )
        logging.info(
            f"Entries skipped due to missing CATEGORY1: {self.validation_stats['skipped_no_category']}"
        )
        logging.info(
            f"Entries with missing SUBCATEGORY1: {self.validation_stats['missing_subcategory']}"
        )
        logging.info(
            f"Entries with missing SUBSUBCATEGORY1: {self.validation_stats['missing_subsubcategory']}"
        )

    def _process_folder(self, folder_group: Tuple[str, pd.DataFrame]) -> None:
        """Process a folder of documentation entries."""
        folder, group = folder_group
        folder_path = self.config.docs_dir / folder
        folder_path.mkdir(exist_ok=True)

        for _, row in group.iterrows():
            self._process_entry(folder_path, row)

    def _process_entry(self, folder_path: Path, row: pd.Series) -> None:
        """Process a single documentation entry."""
        file_path = folder_path / f"{row['CATEGORY1']}.md"
        content = self._generate_entry_content(row)

        headers = {
            'page_icon':
            row['PAGE_ICON'] if pd.notna(row['PAGE_ICON']) else None,
            'subcategory':
            row['SUBCATEGORY1'] if pd.notna(row['SUBCATEGORY1']) else None,
            'subsubcategory':
            row['SUBSUBCATEGORY1']
            if pd.notna(row['SUBSUBCATEGORY1']) else None
        }

        self.markdown_writer.update_file(file_path, content, headers)

    def _generate_entry_content(self, row: pd.Series) -> str:
        """Generate content for a documentation entry."""
        content = [
            f"- **{row['ENTRY NAME']}**: {row['DESCRIPTION'] if pd.notna(row['DESCRIPTION']) else ''}  \n\t"
        ]

        if pd.notna(row['CODE']):
            content.append(self._generate_code_badge(row['CODE']))

        if pd.notna(row['PUBLICATION']):
            citations = str(int(row['CITATIONS'])) if pd.notna(
                row['CITATIONS']) else 'N/A'
            content.append(
                self.badge_generator.publication_badge(row['PUBLICATION'],
                                                       citations))

        for field in ['WEBSERVER', 'LINK']:
            if pd.notna(row[field]):
                status = self.url_validator.check_url(row[field])
                content.append(
                    self.badge_generator.status_badge(row[field], status,
                                                      field.capitalize()))

        content.append('\n')  # Add single newline at the end
        return ''.join(content)

    def _generate_code_badge(self, code_url: str) -> str:
        """Generate appropriate badge for code repository."""
        if 'github.com' in code_url and 'gist' not in code_url:
            if repo_path := GithubUrlProcessor.clean_url(code_url):
                try:
                    return self.badge_generator.github_badges(
                        repo_path, code_url)
                except Exception as e:
                    logging.warning(
                        f"Failed to generate GitHub badges for {code_url}: {str(e)}"
                    )
        # Fallback to a simple badge
        return f"[![Code](https://img.shields.io/badge/Code-Repository-blue?style=for-the-badge)]({code_url}) "


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    script_dir = Path(__file__).parent
    config = ProcessingConfig(docs_dir=script_dir.parent / 'docs',
                              readme_path=script_dir.parent / 'README.md')

    try:
        df = pd.read_csv(script_dir.parent / 'processed_cadd_vault_data.csv')
        generator = DocumentationGenerator(config)
        totals = generator.generate(df)

        # Update index and README files with totals
        for file_path in [config.docs_dir / 'index.md', config.readme_path]:
            if not file_path.exists():
                logging.error(f"{file_path} does not exist.")
                continue

            content = file_path.read_text(encoding='utf-8').splitlines()
            if len(content) < 28:
                logging.error(f"{file_path} has insufficient lines.")
                continue

            start_line = 4 if file_path.name == 'index.md' else 25
            content[start_line:start_line + 3] = [
                f"Number of publications: {totals[0]}  ",
                f"Number of code repositories: {totals[1]}  ",
                f"Number of webserver links: {totals[2]}  "
            ]

            file_path.write_text('\n'.join(content), encoding='utf-8')

        logging.info("Documentation generation completed successfully.")

    except Exception as e:
        logging.error(f"Error during documentation generation: {str(e)}")
        raise


if __name__ == "__main__":
    main()
