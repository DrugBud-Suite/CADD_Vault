"""
Main entry point for the publication manager application.
"""

import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
from rich.console import Console
from rich.logging import RichHandler
from dotenv import load_dotenv
import os

from models import Config, Entry, ProcessingResult
from services import PublicationService, RepositoryService, DataProcessor
from generator import MarkdownGenerator

console = Console()

def setup_logging():
    """Configure logging with rich handler"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("habanero").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine.Engine").setLevel(logging.WARNING)
    logging.getLogger("backoff").setLevel(logging.WARNING)
    logging.getLogger("paperscraper").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(__file__).parent.parent.resolve()

def load_excel_data(file_path: Path) -> List[Dict[str, Any]]:
    """Load and validate Excel data"""
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        console.print(f"[green]Loaded {len(df)} rows from Excel file")
        
        # Map Excel columns to our expected format
        column_mapping = {
            'ENTRY NAME': 'name',
            'DESCRIPTION': 'description',
            'FOLDER1': 'folder',
            'CATEGORY1': 'category',
            'SUBCATEGORY1': 'subcategory',
            'SUBSUBCATEGORY1': 'subsubcategory',
            'CODE': 'repository_url',
            'PUBLICATION': 'publication_url',
            'WEBSERVER': 'webserver_url',
            'LINK': 'link_url',
            'PAGE_ICON': 'page_icon',
            'CITATIONS': 'citations',
            'GITHUB_STARS': 'stars',
            'LAST_COMMIT': 'last_commit',
            'JOURNAL': 'journal',
            'JIF': 'impact_factor'
        }
        
        # Rename columns
        df = df.rename(columns=column_mapping)
        
        # Clean up the data
        for col in df.columns:
            if df[col].dtype == object:  # For string columns
                df[col] = df[col].apply(lambda x: str(x).strip() if pd.notna(x) else '')
            
        # Convert numeric columns properly
        numeric_columns = ['citations', 'stars', 'impact_factor']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col] = df[col].fillna(0)
        
        # Filter out completely empty rows
        df = df.dropna(subset=['name', 'description', 'folder', 'category'], how='all')
        
        # Convert to dictionary records
        records = df.to_dict('records')
        
        console.print(f"[green]Successfully processed {len(records)} valid entries")
        return records
        
    except Exception as e:
        console.print(f"[red]Error loading Excel file: {str(e)}")
        raise

def create_config() -> Config:
    """Create configuration with default paths and environment variables"""
    project_root = get_project_root()
    
    # Load environment variables from .env file
    load_dotenv(project_root / '.env')
    
    return Config(
        input_file=project_root / 'cadd_vault_data.xlsx',
        output_dir=project_root / 'docs',
        template_dir=project_root / 'templates',
        email=os.getenv('EMAIL', 'default@email.com'),
        github_token=os.getenv('GITHUB_TOKEN')
    )

def display_results(result: ProcessingResult):
    """Display processing results"""
    console.print("\n[bold]Processing Results:[/bold]")
    console.print(f"Total entries: {result.total_entries}")
    console.print(f"Successfully processed: {result.successful_entries}")
    console.print(f"Failed: {result.failed_entries}")
    console.print(f"Skipped: {result.skipped_entries}")
    
    if result.errors:
        console.print("\n[red]Errors:[/red]")
        for entry, errors in result.errors.items():
            for error in errors:
                console.print(f"  {entry}: {error}")
    
    if result.warnings:
        console.print("\n[yellow]Warnings:[/yellow]")
        for entry, warnings in result.warnings.items():
            for warning in warnings:
                console.print(f"  {entry}: {warning}")

async def process_data(config: Config) -> tuple[List[Entry], ProcessingResult]:
    """Process data using services"""
    try:
        # Initialize services
        publication_service = PublicationService(config)
        repository_service = RepositoryService(config)
        processor = DataProcessor(publication_service, repository_service)
        
        # Load raw data
        df = pd.read_excel(config.input_file)
        raw_data = load_excel_data(config.input_file)
        
        # Define reverse mapping for updating DataFrame
        reverse_mapping = {
            'citations': 'CITATIONS',
            'journal': 'JOURNAL',
            'impact_factor': 'JIF',
            'stars': 'GITHUB_STARS',
            'last_commit': 'LAST_COMMIT'
        }
        
        # Process entries and update dataframe
        entries = []
        for idx, entry_data in enumerate(raw_data):
            # Handle publication data
            if pub_url := entry_data.get('publication_url'):
                # First normalize the DOI
                normalized_url = publication_service.normalize_doi(pub_url)
                entry_data['publication_url'] = normalized_url
                df.at[idx, 'PUBLICATION'] = normalized_url
                
                # Check if it's a preprint and if it has been published
                if publication_service.is_preprint(normalized_url):
                    preprint_result = await publication_service.check_publication_status(normalized_url)
                    if preprint_result.publication_status == "published":
                        # Update to the published version
                        entry_data['publication_url'] = preprint_result.published_url
                        df.at[idx, 'PUBLICATION'] = preprint_result.published_url
                        logging.info(f"Updated preprint {entry_data['name']} to published version: {preprint_result.published_url}")
                        normalized_url = preprint_result.published_url

                # Only process non-preprint publications
                if not publication_service.is_preprint(normalized_url):
                    # Always fetch citations
                    citations = await publication_service.get_citations(normalized_url)
                    if citations is not None:
                        df.at[idx, reverse_mapping['citations']] = citations
                        entry_data['citations'] = citations
                        logging.info(f"Updated citations for {entry_data['name']}: {citations}")
                    
                    # Only fetch journal if the field is empty
                    current_journal = df.at[idx, reverse_mapping['journal']]
                    if pd.isna(current_journal):
                        journal_info = await publication_service.get_journal_info(normalized_url)
                        if journal_info and journal_info.get('journal'):
                            df.at[idx, reverse_mapping['journal']] = journal_info['journal']
                            entry_data['journal'] = journal_info['journal']
                            logging.info(f"Updated journal for {entry_data['name']}: {journal_info['journal']}")
                            
                            # If we got a new journal name, try to get its impact factor
                            impact_factor = await publication_service.get_impact_factor(journal_info)
                            if impact_factor is not None:
                                df.at[idx, reverse_mapping['impact_factor']] = impact_factor
                                entry_data['impact_factor'] = impact_factor
                                logging.info(f"Updated impact factor for {entry_data['name']}: {impact_factor}")
                    else:
                        # If we have a journal name but no impact factor, try to get it
                        if pd.isna(df.at[idx, reverse_mapping['impact_factor']]):
                            impact_factor = await publication_service.get_impact_factor({'journal': current_journal})
                            if impact_factor is not None:
                                df.at[idx, reverse_mapping['impact_factor']] = impact_factor
                                entry_data['impact_factor'] = impact_factor
                                logging.info(f"Updated impact factor for {entry_data['name']}: {impact_factor}")
            
            # Fetch repository data
            if repo_url := entry_data.get('repository_url'):
                repo_data = await repository_service.get_repository_data(repo_url)
                if repo_data:
                    df.at[idx, reverse_mapping['stars']] = repo_data.stars
                    df.at[idx, reverse_mapping['last_commit']] = repo_data.last_commit
                    entry_data['stars'] = repo_data.stars
                    entry_data['last_commit'] = repo_data.last_commit
                    entry_data['last_commit_ago'] = repo_data.last_commit_ago
            
            entries.append(entry_data)
        
        # Save updated Excel file
        df.to_excel(config.input_file, index=False)
        
        return await processor.process_entries(entries)
        
    except Exception as e:
        console.print(f"[red]Error processing data: {e}")
        raise

def main():
    """Main execution function"""
    try:
        # Setup logging
        setup_logging()
        
        # Create configuration
        config = create_config()
        
        # Process data
        console.print("[bold]Starting data processing...[/bold]")
        entries, processing_result = asyncio.run(process_data(config))
        
        if entries:
            # Generate documentation
            console.print("\n[bold]Generating documentation...[/bold]")
            generator = MarkdownGenerator(config)
            generation_result = generator.generate(entries)
            
            # Display results
            display_results(processing_result)
            console.print(
                f"\n[green]Documentation generated successfully in {config.output_dir}[/green]"
            )
        else:
            console.print("[red]No valid entries to process[/red]")
            raise SystemExit(1)
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)

if __name__ == "__main__":
    main()