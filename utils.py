"""
Utility functions for WordPress automation.
Includes decorators, logging, and error handling.
"""
import os
import time
import logging
import functools
from typing import Callable, Any
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchElementException
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wordpress_automation.log'),
        logging.StreamHandler()
    ]
)

def retry_on_failure(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator to retry a function on failure.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except (TimeoutException, 
                       StaleElementReferenceException,
                       ElementClickInterceptedException,
                       NoSuchElementException) as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logging.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}"
                            f"\nRetrying in {delay} seconds..."
                        )
                        time.sleep(delay)
                    continue
                except Exception as e:
                    logging.error(f"Unexpected error in {func.__name__}: {str(e)}")
                    raise e
                    
            logging.error(
                f"All {max_attempts} attempts failed for {func.__name__}: {str(last_exception)}"
            )
            raise last_exception
            
        return wrapper
    return decorator

def log_action(action_description: str):
    """
    Decorator to log actions with timing information.
    
    Args:
        action_description: Description of the action being performed
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            logging.info(f"Starting: {action_description}")
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logging.info(
                    f"Completed: {action_description} "
                    f"(Duration: {duration:.2f} seconds)"
                )
                return result
            except Exception as e:
                duration = time.time() - start_time
                logging.error(
                    f"Failed: {action_description} "
                    f"(Duration: {duration:.2f} seconds) - Error: {str(e)}"
                )
                raise
                
        return wrapper
    return decorator

def wait_for_element(driver, by, value, timeout=10, condition="presence"):
    """
    Wait for an element with custom conditions.
    
    Args:
        driver: Selenium WebDriver instance
        by: By locator strategy
        value: Locator value
        timeout: Maximum time to wait
        condition: Type of wait condition ("presence", "clickable", "visible")
    """
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    conditions = {
        "presence": EC.presence_of_element_located,
        "clickable": EC.element_to_be_clickable,
        "visible": EC.visibility_of_element_located
    }
    
    wait_condition = conditions.get(condition, EC.presence_of_element_located)
    wait = WebDriverWait(driver, timeout)
    
    try:
        element = wait.until(wait_condition((by, value)))
        return element
    except TimeoutException:
        logging.error(
            f"Timeout waiting for element: {value} "
            f"(condition: {condition})"
        )
        raise

def safe_click(driver, element, timeout=3):
    """
    Safely click an element with retries and scroll into view.
    
    Args:
        driver: Selenium WebDriver instance
        element: Element to click
        timeout: Maximum time to wait between attempts
    """
    max_attempts = 3
    
    for attempt in range(max_attempts):
        try:
            # Scroll element into view
            driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                element
            )
            time.sleep(0.5)
            
            # Try to click
            element.click()
            return True
            
        except (ElementClickInterceptedException, StaleElementReferenceException) as e:
            if attempt == max_attempts - 1:
                logging.error(f"Failed to click element after {max_attempts} attempts")
                raise
            logging.warning(f"Click attempt {attempt + 1} failed, retrying...")
            time.sleep(timeout / max_attempts)

def ensure_dir_exists(directory):
    """
    Ensure a directory exists, create if it doesn't.
    
    Args:
        directory: Path to directory
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")

def move_file(source, destination):
    """
    Safely move a file with logging.
    
    Args:
        source: Source file path
        destination: Destination file path
    """
    try:
        ensure_dir_exists(os.path.dirname(destination))
        os.rename(source, destination)
        logging.info(f"Moved file: {source} -> {destination}")
    except Exception as e:
        logging.error(f"Failed to move file {source}: {str(e)}")
        raise

def clean_text(text):
    """
    Clean and normalize text content.
    
    Args:
        text: Text to clean
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    # Remove unsafe characters
    text = text.replace("\u0000", "")  # Null character
    
    # Strip quotes from ends if present
    text = text.strip('"\'')
    
    return text

def is_valid_url(url):
    """
    Basic URL validation.
    
    Args:
        url: URL to validate
    """
    import re
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(pattern.match(url))

# Commonly used error messages
ERROR_MESSAGES = {
    "login_failed": "Failed to login to WordPress",
    "element_not_found": "Element not found: {element}",
    "timeout": "Operation timed out: {operation}",
    "invalid_input": "Invalid input provided: {input}",
    "file_not_found": "File not found: {file}",
    "unknown_error": "An unknown error occurred: {error}"
}

def format_error(error_key, **kwargs):
    """
    Format error message with parameters.
    
    Args:
        error_key: Key in ERROR_MESSAGES
        **kwargs: Parameters to format the message
    """
    message = ERROR_MESSAGES.get(error_key, ERROR_MESSAGES["unknown_error"])
    return message.format(**kwargs)
