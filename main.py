"""
Main script for WordPress post automation.
"""
import os
import sys
import time
import logging
from typing import Optional
from selenium.common.exceptions import WebDriverException

from config import WordPressConfig, PostConfig, load_config
from parser import PostParser
from wordpress_actions import WordPressAutomator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wordpress_automation.log'),
        logging.StreamHandler()
    ]
)

def process_files(automator: WordPressAutomator, input_dir: str) -> tuple[int, int]:
    """Process all .txt files in the input directory."""
    success_count = 0
    failure_count = 0
    
    try:
        files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
        
        if not files:
            logging.info("No .txt files found to process")
            return success_count, failure_count
            
        logging.info(f"Found {len(files)} files to process")
        
        for filename in files:
            file_path = os.path.join(input_dir, filename)
            logging.info(f"Processing {filename}")
            
            try:
                # Parse the file
                parser = PostParser(file_path)
                post_config = parser.parse_file()
                
                # Create the post
                if automator.create_post(post_config):
                    success_count += 1
                    processed_path = os.path.join('processed', filename)
                    os.rename(file_path, processed_path)
                    logging.info(f"Successfully processed {filename}")
                else:
                    failure_count += 1
                    failed_path = os.path.join('failed', filename)
                    os.rename(file_path, failed_path)
                    logging.error(f"Failed to create post from {filename}")
                
            except Exception as e:
                logging.error(f"Error processing {filename}: {str(e)}")
                failed_path = os.path.join('failed', filename)
                os.rename(file_path, failed_path)
                failure_count += 1
                
    except Exception as e:
        logging.error(f"Error during batch processing: {str(e)}")
        
    return success_count, failure_count

def main():
    try:
        # Print GitHub username and repo URL
        print("Developed by: Neeraj Sihag")
        print("GitHub Repository: https://github.com/Neeraj-Sihag/wordpress-post-automation")
        
        # Load configuration
        config = load_config()
        
        # Create necessary directories
        config.create_directories()
        
        # Initialize automator
        automator = WordPressAutomator(config)
        
        try:
            # Setup browser and login
            logging.info("Setting up browser...")
            automator.setup_browser()
            
            logging.info("Logging into WordPress...")
            if not automator.login():
                logging.error("Failed to login to WordPress")
                return 1
                
            # Process files
            logging.info("Starting file processing...")
            success_count, failure_count = process_files(automator, config.input_dir)
            
            # Log summary
            total = success_count + failure_count
            logging.info("\nProcessing Summary:")
            logging.info(f"Total files processed: {total}")
            logging.info(f"Successful: {success_count}")
            logging.info(f"Failed: {failure_count}")
            
            if failure_count > 0:
                logging.warning(
                    "Some files failed processing. "
                    "Check the 'failed' directory and logs for details."
                )
                
            return 0 if failure_count == 0 else 1
            
        finally:
            # Keep browser open for debugging
            input("Press Enter to close the browser...")
            automator.cleanup()
            
    except KeyboardInterrupt:
        logging.info("\nOperation cancelled by user")
        return 1
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return 1

if __name__ == "__main__":
    try:
        logging.info("Starting WordPress automation")
        exit_code = main()
        
        if exit_code == 0:
            logging.info("WordPress automation completed successfully")
        else:
            logging.warning("WordPress automation completed with errors")
            
        sys.exit(exit_code)
        
    except Exception as e:
        logging.critical(f"Critical error: {str(e)}")
        sys.exit(1)
