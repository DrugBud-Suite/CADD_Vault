"""
Data models for the publication manager.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl, validator


class Publication(BaseModel):
    """Publication data model"""
    url: Optional[str] = None
    citations: Optional[int] = Field(default=0, ge=0)
    journal: Optional[str] = None
    impact_factor: Optional[float] = Field(default=0.0, ge=0.0)

    @validator('url')
    def validate_url(cls, v):
        """Validate and clean URL"""
        if v and isinstance(v, str):
            v = v.strip()
            if v.startswith('http'):
                return v
        return None


class Repository(BaseModel):
    """Repository data model"""
    url: Optional[str] = None
    stars: Optional[int] = Field(default=0, ge=0)
    last_commit: Optional[str] = None
    last_commit_ago: Optional[str] = None

    @validator('url')
    def validate_url(cls, v):
        """Validate and clean URL"""
        if v and isinstance(v, str):
            v = v.strip()
            if v.startswith('http'):
                return v
        return None

class WebServer(BaseModel):
    """Webserver data model"""
    url: str
    status: str = "online"  # Default to online

class Entry(BaseModel):
    """Main entry combining all data"""
    name: str = Field(..., min_length=1)
    description: Optional[str] = Field(default="")
    folder: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    subcategory: Optional[str] = None
    subsubcategory: Optional[str] = None
    repository: Optional[Repository] = None
    publication: Optional[Publication] = None
    webserver: Optional[WebServer] = None
    link_url: Optional[str] = None
    page_icon: Optional[str] = None

    @validator('folder', 'category')
    def validate_path_component(cls, v):
        """Ensure folder and category names are valid path components"""
        if v and isinstance(v, str):
            v = v.strip()
            if '/' in v or '\\' in v:
                raise ValueError('Cannot contain path separators')
        return v

    @classmethod
    def from_dict(cls, data: Dict) -> 'Entry':
        """Create Entry from dictionary data"""
        # Create Repository if URL exists
        repository = None
        if data.get('repository_url'):
            repository = Repository(
                url=data['repository_url'],
                stars=data.get('stars', 0),
                last_commit=data.get('last_commit'),
                last_commit_ago=data.get('last_commit_ago')
            )

        # Create Publication if URL exists
        publication = None
        if data.get('publication_url'):
            publication = Publication(
                url=data['publication_url'],
                citations=data.get('citations', 0),
                journal=data.get('journal'),
                impact_factor=data.get('impact_factor', 0.0)
            )

        # Create WebServer if URL exists
        webserver = None
        if data.get('webserver_url'):
            webserver = WebServer(
                url=data['webserver_url']
            )

        return cls(
            name=data['name'],
            description=data['description'],
            folder=data['folder'],
            category=data['category'],
            subcategory=data.get('subcategory'),
            subsubcategory=data.get('subsubcategory'),
            repository=repository,
            publication=publication,
            webserver=webserver,
            link_url=data.get('link_url'),
            page_icon=data.get('page_icon')
        )


class ProcessingResult(BaseModel):
    """Results from processing entries"""
    total_entries: int = 0
    successful_entries: int = 0
    failed_entries: int = 0
    skipped_entries: int = 0
    errors: Dict[str, List[str]] = Field(default_factory=dict)
    warnings: Dict[str, List[str]] = Field(default_factory=dict)

    def add_error(self, entry_name: str, error_message: str) -> None:
        """Add an error message for a specific entry"""
        if entry_name not in self.errors:
            self.errors[entry_name] = []
        self.errors[entry_name].append(error_message)

    def add_warning(self, entry_name: str, warning_message: str) -> None:
        """Add a warning message for a specific entry"""
        if entry_name not in self.warnings:
            self.warnings[entry_name] = []
        self.warnings[entry_name].append(warning_message)


class Config(BaseModel):
    """Application configuration"""
    input_file: Path
    output_dir: Path
    template_dir: Path
    email: str
    github_token: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3
    max_workers: int = 5
    keep_files: List[str] = Field(
        default_factory=lambda: ['CONTRIBUTING.md', 'index.md', 'LogoV1.png', 'images']
    )

    @validator('input_file')
    def validate_input_file(cls, v):
        if not v.exists():
            raise ValueError(f'Input file does not exist: {v}')
        return v

    @validator('template_dir')
    def validate_template_dir(cls, v):
        if not v.exists():
            raise ValueError(f'Template directory does not exist: {v}')
        return v