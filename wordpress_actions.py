"""
WordPress automation actions using Selenium.
Handles login, post creation, and all WordPress interactions.
"""
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config import WordPressConfig, PostConfig

class WordPressAutomator:
    def __init__(self, config: WordPressConfig):
        self.config = config
        self.driver = None
        self.wait = None

    def setup_browser(self):
        """Initialize and configure the browser."""
        try:
            service = Service(ChromeDriverManager().install())
            options = Options()
            if self.config.headless:
                options.add_argument('--headless')
            options.add_argument('--start-maximized')
            
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.implicitly_wait(self.config.implicit_wait)
            self.wait = WebDriverWait(self.driver, self.config.page_load_timeout)
            logging.info("Browser setup successful")
            
        except Exception as e:
            logging.error(f"Failed to setup browser: {str(e)}")
            raise

    def login(self) -> bool:
        """Log into WordPress admin panel."""
        try:
            self.driver.get(self.config.get_admin_url())
            
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "user_login"))
            )
            username_field.clear()
            username_field.send_keys(self.config.username)
            
            password_field = self.driver.find_element(By.ID, "user_pass")
            password_field.clear()
            password_field.send_keys(self.config.password)
            
            login_button = self.driver.find_element(By.ID, "wp-submit")
            login_button.click()
            
            # Wait for admin bar to confirm login
            self.wait.until(EC.presence_of_element_located((By.ID, "wpadminbar")))
            logging.info("Successfully logged into WordPress")
            return True
            
        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            return False

    def create_post(self, post_config: PostConfig) -> bool:
        """Create a new post with the given configuration."""
        try:
            # Navigate to new post page
            self.driver.get(self.config.get_new_post_url())
            time.sleep(2)

            # Set title
            title_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "title"))
            )
            title_field.clear()
            title_field.send_keys(post_config.title)

            # Switch to text mode and set content
            self._switch_to_text_mode()
            content_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "content"))
            )
            content_field.clear()
            content_field.send_keys(post_config.content)

            # Switch back to visual mode for better preview
            self._switch_to_visual_mode()

            # Set featured image if provided
            if post_config.media_index is not None:
                self.set_featured_image(post_config.media_index)

            # Set category if provided
            if post_config.category:
                self.set_category(post_config.category)

            # Set tags if provided
            if post_config.tags:
                self.set_tags(post_config.tags)

            # Publish or save as draft
            self.publish_post(post_config.status)
            
            # Final verification
            if post_config.status == "publish" and not self._is_post_published():
                logging.error("Failed to verify post publication")
                return False
                
            logging.info(f"Successfully created post: {post_config.title}")
            return True

        except Exception as e:
            logging.error(f"Failed to create post: {str(e)}")
            return False

    def _switch_to_text_mode(self):
        """Switch to text editor mode."""
        try:
            text_tab = self.wait.until(
                EC.element_to_be_clickable((By.ID, "content-html"))
            )
            text_tab.click()
            time.sleep(1)
        except Exception as e:
            logging.warning(f"Could not switch to text mode: {str(e)}")

    def _switch_to_visual_mode(self):
        """Switch to visual editor mode."""
        try:
            visual_tab = self.wait.until(
                EC.element_to_be_clickable((By.ID, "content-tmce"))
            )
            visual_tab.click()
            time.sleep(1)
        except Exception as e:
            logging.warning(f"Could not switch to visual mode: {str(e)}")

    def _close_all_modals(self):
        """Close any open modal windows."""
        try:
            close_buttons = self.driver.find_elements(
                By.CSS_SELECTOR, '.media-modal-close'
            )
            for button in close_buttons:
                try:
                    button.click()
                    time.sleep(0.5)
                except:
                    continue
        except:
            pass
    def set_featured_image(self, media_index: int):
        """Set featured image from media library."""
        try:
            # Click Set Featured Image button
            set_featured = self.wait.until(
                EC.element_to_be_clickable((By.ID, "set-post-thumbnail"))
            )
            
            # Scroll to button
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                set_featured
            )
            time.sleep(1)
            
            set_featured.click()
            time.sleep(2)

            # Wait for media modal
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "media-modal")))
            
            # Click Media Library tab if needed
            media_library_tab = self.driver.find_element(
                By.CSS_SELECTOR, '.media-menu-item:nth-child(2)'
            )
            media_library_tab.click()
            time.sleep(2)

            # Select image by index
            images = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.attachment-preview'))
            )
            
            if len(images) >= media_index:
                images[media_index - 1].click()
                time.sleep(1)

                # Set featured image
                set_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.media-button-select'))
                )
                set_button.click()
                time.sleep(2)
            else:
                logging.warning(f"Image index {media_index} not found in media library")

        except Exception as e:
            logging.warning(f"Failed to set featured image: {str(e)}")
        finally:
            self._close_all_modals()

    def set_category(self, category: str):
        """Set post category."""
        try:
            # Find and scroll to categories box
            category_area = self.wait.until(
                EC.presence_of_element_located((By.ID, "categorydiv"))
            )
            
            # Scroll to categories box
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                category_area
            )
            time.sleep(1)

            # Make sure categories section is expanded
            try:
                # Check if it's collapsed
                if 'closed' in category_area.get_attribute('class'):
                    # Find and click the toggle
                    toggle = category_area.find_element(By.CLASS_NAME, "handlediv")
                    toggle.click()
                    time.sleep(1)
                    
                    # Verify it's expanded
                    if 'closed' in category_area.get_attribute('class'):
                        # Try alternative method
                        self.driver.execute_script(
                            "arguments[0].classList.remove('closed');", 
                            category_area
                        )
                        time.sleep(1)
            except:
                logging.warning("Could not verify category section state")

            # Wait for category list to be visible
            category_list = self.wait.until(
                EC.presence_of_element_located((By.ID, "categorychecklist"))
            )
            
            # Scroll to category list
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                category_list
            )
            time.sleep(1)
            
            # Find and click category
            xpath = f"//label[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{category.lower()}')]/input[@type='checkbox']"
            checkbox = self.wait.until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            
            if not checkbox.is_selected():
                # Try regular click first
                try:
                    checkbox.click()
                except:
                    # Try JavaScript click if regular fails
                    self.driver.execute_script("arguments[0].click();", checkbox)
                time.sleep(0.5)
                
                # Verify selection
                if not checkbox.is_selected():
                    raise Exception("Failed to select category checkbox")

        except Exception as e:
            logging.warning(f"Failed to set category: {str(e)}")

    def set_tags(self, tags: str):
        """Set post tags quickly."""
        try:
            # Find tags field directly
            tags_field = self.driver.find_element(By.ID, "new-tag-post_tag")
            
            # Process all tags at once
            tags_field.clear()
            # Add comma if not present
            processed_tags = tags if ',' in tags else tags.replace(' ', ', ')
            tags_field.send_keys(processed_tags)
            tags_field.send_keys(Keys.RETURN)
            
            # Quick verify - just check if tag area contains new content
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".tagchecklist > span"))
                )
            except:
                # One retry with Add button if Enter key didn't work
                add_button = self.driver.find_element(By.CSS_SELECTOR, "input.tagadd")
                add_button.click()
            
            logging.info(f"Tags added: {tags}")

        except Exception as e:
            logging.error(f"Failed to set tags: {str(e)}")

    def _is_post_published(self) -> bool:
        """Check if post is currently published."""
        try:
            # Check for success message
            try:
                success_message = self.driver.find_element(By.CSS_SELECTOR, "#message.updated")
                if "Post published" in success_message.text:
                    return True
            except:
                pass

            # Check post status
            status_span = self.wait.until(
                EC.presence_of_element_located((By.ID, "post-status-display"))
            )
            return "Published" in status_span.text
        except:
            return False

    def _prepare_publish_status(self):
        """Prepare post for publishing by setting correct status."""
        try:
            status_span = self.wait.until(
                EC.presence_of_element_located((By.ID, "post-status-display"))
            )
            if "Draft" in status_span.text:
                # Click edit status
                edit_status = self.driver.find_element(
                    By.CSS_SELECTOR, "a.edit-post-status"
                )
                edit_status.click()
                time.sleep(0.5)
                
                # Select publish
                status_select = self.driver.find_element(By.ID, "post_status")
                for option in status_select.find_elements(By.TAG_NAME, "option"):
                    if option.text == "Published":
                        option.click()
                        break
                time.sleep(0.5)
                
                # Click OK
                ok_button = self.driver.find_element(
                    By.CSS_SELECTOR, "a.save-post-status"
                )
                ok_button.click()
                time.sleep(0.5)
        except:
            logging.warning("Could not modify post status directly")

    def _save_draft(self):
        """Save post as draft."""
        try:
            save_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "save-post"))
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                save_button
            )
            time.sleep(1)
            
            try:
                save_button.click()
            except:
                self.driver.execute_script("arguments[0].click();", save_button)
            
            time.sleep(2)
            
            # Verify save was successful
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#message.updated"))
                )
            except:
                logging.warning("Could not verify draft was saved")
                
        except Exception as e:
            logging.error(f"Failed to save draft: {str(e)}")
            raise

    def publish_post(self, status: str):
        """Publish or save the post."""
        try:
            # Close any open modals first
            self._close_all_modals()

            # Scroll to publish box
            publish_box = self.wait.until(
                EC.presence_of_element_located((By.ID, "submitdiv"))
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});",
                publish_box
            )
            time.sleep(1)

            if status == "publish":
                # Set up publish status if needed
                self._prepare_publish_status()

                # Check if already published
                if self._is_post_published():
                    logging.info("Post is already published")
                    return

                publish_attempts = 3
                for attempt in range(publish_attempts):
                    try:
                        # Find and click publish button
                        publish_button = self.wait.until(
                            EC.element_to_be_clickable((By.ID, "publish"))
                        )
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                            publish_button
                        )
                        time.sleep(1)

                        # Try different click methods
                        try:
                            publish_button.click()
                        except:
                            self.driver.execute_script("arguments[0].click();", publish_button)
                        
                        # Wait for publish to complete
                        time.sleep(3)
                        
                        # Verify publish was successful
                        if self._is_post_published():
                            logging.info("Post published successfully")
                            return
                        
                        if attempt < publish_attempts - 1:
                            logging.warning(f"Publish attempt {attempt + 1} unsuccessful, retrying...")
                            time.sleep(2)  # Wait before next attempt
                        
                    except Exception as e:
                        if attempt == publish_attempts - 1:
                            raise Exception(f"Failed to publish after {publish_attempts} attempts: {str(e)}")
                        logging.warning(f"Publish attempt {attempt + 1} failed: {str(e)}")
                        time.sleep(2)  # Wait before retry
            else:
                self._save_draft()

        except Exception as e:
            logging.error(f"Failed to {status} post: {str(e)}")
            raise

    def cleanup(self):
        """Clean up resources."""
        if self.driver:
            try:
                self.driver.quit()
                logging.info("Browser closed")
            except Exception as e:
                logging.warning(f"Error closing browser: {str(e)}")

    def wait_for_element(self, by, value, timeout=10, condition="presence"):
        """
        Wait for an element with custom conditions.
        
        Args:
            by: By locator type
            value: Locator value
            timeout: Maximum wait time
            condition: Type of wait condition ("presence", "clickable", "visible")
        """
        conditions = {
            "presence": EC.presence_of_element_located,
            "clickable": EC.element_to_be_clickable,
            "visible": EC.visibility_of_element_located
        }
        
        wait_condition = conditions.get(condition, EC.presence_of_element_located)
        try:
            element = WebDriverWait(self.driver, timeout).until(
                wait_condition((by, value))
            )
            return element
        except Exception as e:
            logging.error(f"Timeout waiting for element: {value} ({condition})")
            raise

    def safe_click(self, element, timeout=3, attempts=3):
        """
        Safely click an element with multiple attempts and scroll.
        
        Args:
            element: WebElement to click
            timeout: Time between attempts
            attempts: Number of click attempts
        """
        for attempt in range(attempts):
            try:
                # Scroll element into view
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                    element
                )
                time.sleep(1)
                
                # Try regular click
                try:
                    element.click()
                    return True
                except:
                    # Try JavaScript click
                    self.driver.execute_script("arguments[0].click();", element)
                    return True
                    
            except Exception as e:
                if attempt == attempts - 1:
                    logging.error(f"Failed to click element after {attempts} attempts")
                    raise
                logging.warning(f"Click attempt {attempt + 1} failed, retrying...")
                time.sleep(timeout / attempts)
        
        return False

    def scroll_to_element(self, element, position="center"):
        """
        Scroll element into view with specified position.
        
        Args:
            element: WebElement to scroll to
            position: Scroll position ("start", "center", "end")
        """
        try:
            self.driver.execute_script(
                f"arguments[0].scrollIntoView({{behavior: 'smooth', block: '{position}'}});",
                element
            )
            time.sleep(1)
        except Exception as e:
            logging.warning(f"Failed to scroll to element: {str(e)}")