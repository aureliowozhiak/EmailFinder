from extract import search_files
from transform import process_and_filter_emails
from db import load_emails_to_db
import argparse
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def run_email_finder(queries, search_engine='google'):
    """Main function to orchestrate the email finding process"""
    logging.info("Starting email finder process")
    
    # Step 1: Search and download files
    for query in queries:
        logging.info(f"Searching for: {query}")
        max_retries = 3
        for attempt in range(max_retries):
            try:
                search_files(query, engine=search_engine)
                break
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    logging.error(f"Failed after {max_retries} attempts for: {query}")
    
    # Step 2: Process downloaded files and extract emails
    logging.info("Processing downloaded files")
    process_and_filter_emails()
    
    # Step 3: Load emails into database
    logging.info("Loading emails into database")
    new_emails = load_emails_to_db()
    logging.info(f"Added {new_emails} new emails to database")

def main():
    parser = argparse.ArgumentParser(description='Email Finder Tool')
    parser.add_argument('--queries', nargs='+', help='List of search queries', required=True)
    parser.add_argument('--engine', choices=['google', 'duckduckgo'], default='google',
                      help='Search engine to use (default: google)')
    
    args = parser.parse_args()
    
    setup_logging()
    run_email_finder(args.queries, args.engine)

if __name__ == "__main__":
    main()
