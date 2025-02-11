"""
generator.py
Markdown documentation generator using templates and maintaining directory structure.
"""

import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from jinja2 import Environment, FileSystemLoader, select_autoescape
from models import Config, Entry, ProcessingResult
from rich.console import Console
from rich.progress import Progress


class MarkdownGenerator:
    """Generate markdown documentation from processed entries"""

    def __init__(self, config: Config):
        self.config = config
        self.console = Console()
        self.logger = logging.getLogger(__name__)
        
        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(config.template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self.env.filters['format_date'] = lambda d: d.strftime('%Y-%m-%d') if d else 'N/A'
        self.env.filters['stars_display'] = lambda s: f"{s:,}" if s else 'N/A'

    def generate(self, entries: List[Entry]) -> ProcessingResult:
        """Generate markdown files from processed entries"""
        result = ProcessingResult()
        
        try:
            self._prepare_output_directory()
            
            with Progress() as progress:
                task = progress.add_task(
                    "Generating documentation...",
                    total=len(entries)
                )
                
                # Group entries by folder and category
                grouped_entries = self._group_entries(entries)
                
                # Generate documentation for each group
                for folder, categories in grouped_entries.items():
                    for category, entries_list in categories.items():
                        try:
                            self._generate_category_page(
                                folder,
                                category,
                                entries_list
                            )
                            result.successful_entries += len(entries_list)
                        except Exception as e:
                            self.logger.error(
                                f"Error generating {folder}/{category}: {str(e)}"
                            )
                            result.add_error(f"{folder}/{category}", str(e))
                            result.failed_entries += len(entries_list)
                        finally:
                            progress.update(task, advance=len(entries_list))
                
                # Generate index page
                self._generate_index_page(entries)
                
            result.total_entries = len(entries)
            return result
            
        except Exception as e:
            self.logger.error(f"Documentation generation failed: {str(e)}")
            result.add_error("general", str(e))
            return result

    def _prepare_output_directory(self):
        """Prepare output directory while preserving specified files"""
        output_dir = self.config.output_dir
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Remove existing files except those in keep_files
        for item in output_dir.iterdir():
            if item.name not in self.config.keep_files:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()

    def _group_entries(self, entries: List[Entry]) -> Dict[str, Dict[str, List[Entry]]]:
        """Group entries by folder and category"""
        grouped = {}
        for entry in entries:
            if entry.folder not in grouped:
                grouped[entry.folder] = {}
            if entry.category not in grouped[entry.folder]:
                grouped[entry.folder][entry.category] = []
            grouped[entry.folder][entry.category].append(entry)
        return grouped

    def _generate_category_page(
        self,
        folder: str,
        category: str,
        entries: List[Entry]
    ):
        """Generate markdown page for a category"""
        template = self.env.get_template('category.md.j2')
        
        # Sort entries by subcategory and name
        sorted_entries = sorted(
            entries,
            key=lambda x: (x.subcategory or '', x.subsubcategory or '', x.name)
        )
        
        content = template.render(
            category=category,
            entries=sorted_entries,
            generation_date=datetime.utcnow(),
            config=self.config
        )
        
        # Ensure folder exists
        output_path = self.config.output_dir / folder
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Write content to file
        output_file = output_path / f"{category}.md"
        output_file.write_text(content, encoding='utf-8')

    def _generate_index_page(self, entries: List[Entry]):
        """Generate main index page with statistics"""
        template = self.env.get_template('index.md.j2')
        
        # Get unique folders and their categories
        folders = sorted({e.folder for e in entries})
        folder_categories = {
            folder: sorted({e.category for e in entries if e.folder == folder})
            for folder in folders
        }
        
        stats = {
            'total_entries': len(entries),
            'publication_count': sum(1 for e in entries if e.publication),
            'repository_count': sum(1 for e in entries if e.repository),
            'webserver_count': sum(1 for e in entries if e.webserver),  # Now using webserver attribute
            'folders': len(folders),
            'categories': len({(e.folder, e.category) for e in entries}),
            'last_updated': datetime.utcnow()
        }
        
        content = template.render(
            stats=stats,
            folders=folders,
            folder_categories=folder_categories,
            config=self.config
        )
        
        index_file = self.config.output_dir / 'index.md'
        index_file.write_text(content, encoding='utf-8')