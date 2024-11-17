# WordPress Post Automation

A Python-based automation tool for creating and publishing WordPress posts using the Classic Editor. This tool enables batch processing of posts from text files, handling content formatting, categories, tags, and featured images seamlessly.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.0%2B-green.svg)](https://www.selenium.dev/)
[![WordPress](https://img.shields.io/badge/wordpress-6.0%2B-blue.svg)](https://wordpress.org/)

## Features

- ✨ Batch processing of multiple posts from text files
- 🖼️ Automatic featured image assignment
- 🏷️ Category and tag management
- 📝 Support for diverse content blocks
- 📅 Scheduled publishing or draft-saving
- 🔄 Smart retry mechanism for failed operations
- 📊 Comprehensive error logging
- 🚀 Optimized performance

---

## Prerequisites

- Python 3.8 or higher
- WordPress site with the Classic Editor plugin enabled
- Chrome browser installed
- WordPress admin credentials

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Neeraj-Sihag/wordpress-post-automation.git
cd wordpress-post-automation
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables (or modify `config.py` directly):
```bash
export WP_URL="https://your-wordpress-site.com"
export WP_USER="your_username"
export WP_PASS="your_password"
```

---

## Directory Structure

```plaintext
wordpress_post_automation/
├── main.py                  # Main execution script
├── config.py                # Configuration settings
├── wordpress_actions.py     # Core WordPress automation interactions
├── parser.py                # Post file parser
├── content_blocks.py        # Content block management
├── topost                   # Directory for input post files
├── processed/               # Successfully processed posts
├── failed/                  # Failed posts
└── logs/                    # Logs directory
```

---

## Usage

1. **Prepare Post Files**  
   Place post files in the `topost` directory using the following format:

```plaintext
# --- Metadata ---
title: "Your Post Title"
description: "Post description"
slug: "post-slug"
featured_image: "2"            # Media library index
category: "Your Category"
tags: "Tag1, Tag2, Tag3"
author: "1"                    # WordPress user ID
status: "publish"             # publish/draft/private
publish_date: ""              # YYYY-MM-DD or blank for immediate

# --- Content ---
[paragraph]
Your content here with support for various blocks.
[/paragraph]

[heading level=2]
Section Title
[/heading]
```

2. **Run the Automation**  
   Use the following command to start the automation process:
```bash
python main.py
```

---

## Supported Content Blocks

The following content blocks are supported:

- `[paragraph]`: Regular text content
- `[heading level=1-6]`: Headings
- `[list type=ordered/unordered]`: Ordered and unordered lists
- `[quote]`: Blockquotes
- `[code]`: Code snippets
- `[embed]`: Media embeds
- `[image]`: Images
- `[table]`: Tables

---

## Configuration Options

You can customize the behavior of the script by editing `config.py`:

```python
class Config:
    BASE_URL = "https://your-wordpress-site.com"
    USERNAME = "your_username"
    PASSWORD = "your_password"
    INPUT_DIR = "topost"
    PROCESSED_DIR = "processed"
    FAILED_DIR = "failed"
    IMPLICIT_WAIT = 10
    PAGE_LOAD_TIMEOUT = 20
```

---

## Error Handling

1. **Retry Mechanism**  
   Failed actions are retried up to three times before moving the post file to the `failed/` directory.

2. **Logs**  
   All errors and detailed logs are saved in the `logs/wordpress_automation.log` file.  
   To monitor logs:
```bash
tail -f logs/wordpress_automation.log
```

3. **Post Status**  
   - Successfully processed files are moved to the `processed/` directory.
   - Failed files are moved to the `failed/` directory for review.

---

## Troubleshooting

### Common Issues

1. **Post Creation Fails**
   - Ensure WordPress credentials are correct.
   - Verify the Classic Editor plugin is active.
   - Check that categories exist in WordPress.

2. **Tags Not Added**
   - Ensure tags are separated by commas.
   - Verify tag format in the input file.

3. **Featured Image Issues**
   - Check the file path or media library index.
   - Verify media library permissions.

### Logs

Use logs to debug issues. Example:
```bash
cat logs/wordpress_automation.log
```

---

## Contributing

1. Fork the repository.
2. Create a new feature branch:
```bash
git checkout -b feature/AmazingFeature
```
3. Commit your changes:
```bash
git commit -m 'Add AmazingFeature'
```
4. Push to the branch:
```bash
git push origin feature/AmazingFeature
```
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/)
- [WordPress Classic Editor](https://wordpress.org/plugins/classic-editor/)
- [Python](https://www.python.org/)

---

## Author

**Neeraj Sihag**  
GitHub: [@Neeraj-Sihag](https://github.com/Neeraj-Sihag)

Project Link: [WordPress Post Automation](https://github.com/Neeraj-Sihag/wordpress-post-automation)

