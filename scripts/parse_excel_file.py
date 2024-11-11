"""
parse_excel_file.py
Entry point for the research paper data processing system.
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from services import APIServices
from processor import DataProcessor


def setup_logging(log_file: str = "processing.log"):
    """Configure logging settings"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ])


def validate_paths(input_file: str, output_csv: str, output_excel: str):
    """Validate input and output file paths"""
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Ensure output directories exist
    for output_path in [output_csv, output_excel]:
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)


def main():
    """Main execution function"""
    try:
        # Load environment variables
        load_dotenv()

        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)

        # File paths
        script_dir = Path(__file__).parent
        input_file = script_dir / '../cadd_vault_data.xlsx'
        output_csv = script_dir / '../processed_cadd_vault_data.csv'
        output_excel = script_dir / '../cadd_vault_data.xlsx'

        # Validate paths
        validate_paths(input_file, output_csv, output_excel)

        # Initialize services
        api_services = APIServices(
            email=os.getenv('EMAIL', 'your@email.com'),
            github_token=os.getenv('GITHUB_TOKEN', None)
        )

        # Initialize and run processor
        logger.info("\n=== Starting Data Processing ===")
        logger.info(f"Input file: {input_file}")
        logger.info(f"Output CSV: {output_csv}")
        logger.info(f"Output Excel: {output_excel}")

        processor = DataProcessor(api_services)
        processor.process_data(
            str(input_file),
            str(output_csv),
            str(output_excel)
        )

        logger.info("\n=== Processing Complete ===")

    except Exception as e:
        logger.error(f"\n✗ Error during execution: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()