import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Common configuration
EMAIL = os.getenv('EMAIL', 'your@email.com')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
DEFAULT_TIMEOUT = 30  # seconds

HEADERS = {'User-Agent': f'PrePrintTracker/1.0 (mailto:{EMAIL})'}


def normalize_doi(doi):
    """
    Comprehensive DOI normalization function.
    Handles all cases of DOI cleaning and normalization in one place.
    """
    if not doi:
        return doi

    # Convert to string and strip whitespace
    doi = str(doi).strip()

    # Handle DOI URLs first
    if 'doi.org/' in doi:
        doi = doi.split('doi.org/')[-1]
    elif 'http://' in doi or 'https://' in doi:
        doi = doi.split('/')[-1]

    # Clean the DOI
    doi = re.sub(r'v\d+(?:\.full)?$', '',
                 doi)  # Remove version numbers (v1, v2.full, etc.)
    doi = re.sub(r'\.full$', '', doi)  # Remove standalone .full
    doi = re.sub(r'\.(?:svg|pdf|html)$', '', doi)  # Remove file extensions
    doi = re.sub(r'[\[\(\{\]\)\}]+$', '', doi)  # Remove trailing brackets
    doi = re.sub(r'[\.:\-]+$', '', doi)  # Remove trailing punctuation

    # Remove any query parameters or fragments
    doi = doi.split('?')[0].split('#')[0]

    # Clean up any remaining whitespace
    doi = doi.strip()

    # Add proper DOI URL prefix if it's a bare DOI
    if doi.startswith('10.') and not doi.startswith('https://doi.org/'):
        doi = f'https://doi.org/{doi}'

    return doi


def calculate_similarity(text1, text2):
    """Calculate text similarity using token overlap."""
    words1 = set(re.findall(r'\w+', text1.lower()))
    words2 = set(re.findall(r'\w+', text2.lower()))
    intersection = len(words1.intersection(words2))
    shorter_len = min(len(words1), len(words2))
    return intersection / shorter_len if shorter_len > 0 else 0
