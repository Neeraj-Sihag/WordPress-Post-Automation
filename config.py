"""
Configuration settings for WordPress automation.
"""
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class PostConfig:
    """Configuration for a single post."""
    title: str
    content: str
    category: Optional[str] = None
    tags: Optional[str] = None
    media_index: Optional[int] = None  # Index of image in media library
    status: str = "draft"
    
    def __post_init__(self):
        """Validate post configuration after initialization."""
        if not self.title:
            raise ValueError("Post title is required")
        if not self.content:
            raise ValueError("Post content is required")
        if self.status not in ["draft", "publish", "private"]:
            raise ValueError(f"Invalid post status: {self.status}")
        if self.media_index is not None and not isinstance(self.media_index, int):
            raise ValueError("Media index must be an integer")

@dataclass
class WordPressConfig:
    """WordPress site configuration settings."""
    url: str = "http://your-wordpress-site.com"
    username: str = "your_username"
    password: str = "your_password"
    input_dir: str = "topost"
    processed_dir: str = "processed"
    failed_dir: str = "failed"
    
    # Browser settings
    headless: bool = False
    implicit_wait: int = 10
    page_load_timeout: int = 15
    
    def get_admin_url(self) -> str:
        """Get WordPress admin URL."""
        return f"{self.url}/wp-admin"
    
    def get_new_post_url(self) -> str:
        """Get URL for creating new post with classic editor."""
        return f"{self.get_admin_url()}/post-new.php?classic-editor"
    
    def create_directories(self):
        """Create necessary directories if they don't exist."""
        for directory in [self.input_dir, self.processed_dir, self.failed_dir]:
            os.makedirs(directory, exist_ok=True)

def load_config() -> WordPressConfig:
    """
    Load configuration from environment variables.
    """
    return WordPressConfig(
        url=os.getenv('WP_URL', 'https://writeyourwebsitehere.tld'),
        username=os.getenv('WP_USER', 'writeusernamehere'),
        password=os.getenv('WP_PASS', 'writepasswordhere'),
        input_dir=os.getenv('WP_INPUT_DIR', 'topost'),
        processed_dir=os.getenv('WP_PROCESSED_DIR', 'processed'),
        failed_dir=os.getenv('WP_FAILED_DIR', 'failed')
    )

if __name__ == "__main__":
    # Test configuration loading
    config = load_config()
    print(f"WordPress URL: {config.url}")
    print(f"Admin URL: {config.get_admin_url()}")
    print(f"New Post URL: {config.get_new_post_url()}")