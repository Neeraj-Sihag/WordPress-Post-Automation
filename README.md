# WordPress Post Automation Tool

A Python-powered automation system to streamline the process of creating and publishing WordPress posts. This tool supports batch uploads, handling metadata, content formatting, featured images, categories, and tags — all seamlessly integrated with the **WordPress Classic Editor**.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)  
[![Selenium](https://img.shields.io/badge/selenium-4.0%2B-green.svg)](https://www.selenium.dev/)  
[![WordPress](https://img.shields.io/badge/wordpress-6.0%2B-blue.svg)](https://wordpress.org/)

---

## Features

✨ **Batch Processing**: Automate multiple posts in one go.  
🖼️ **Featured Image Support**: Add images directly from the WordPress Media Library.  
🏷️ **Categories and Tags**: Automatically assign categories and tags.  
📝 **Content Blocks**: Supports headings, paragraphs, lists, quotes, and code blocks.  
📅 **Scheduling**: Publish immediately, save as a draft, or schedule for future dates.  
🔄 **Retry Mechanism**: Automatically handles transient errors.  
📊 **Comprehensive Logs**: Detailed logs for debugging and monitoring.  
🚀 **AI Prompt**: Use `aiprompt.txt` to generate content files with AI.  

---

## Prerequisites

1. **Python 3.8 or higher**  
2. **WordPress site with Classic Editor plugin enabled**  
3. **Google Chrome**  
4. **ChromeDriver** (managed automatically by `webdriver-manager`)  
5. **WordPress admin credentials**

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

3. Set up the configuration:
   - Edit `config.py` directly, or set environment variables:
     ```bash
     export WP_URL="https://your-wordpress-site.com"
     export WP_USER="your_username"
     export WP_PASS="your_password"
     ```

---

## How It Works

This tool processes `.txt` files in the `topost/` directory. Each file contains **metadata** and **content blocks**. The structure is designed to work seamlessly with WordPress automation.

### Post File Format
Every post file follows this structure:

```plaintext
# --- Metadata ---
title: "Your Post Title"
description: "Brief description of the post"
slug: "custom-slug"
featured_image: "1"             # Media library index
category: "Technology"
tags: "Python, Automation, WordPress"
author: "1"                     # WordPress user ID
status: "publish"               # Options: "publish", "draft", "private"
publish_date: "2024-11-17"      # Leave blank for immediate publishing

# --- Content ---
[paragraph]
This is an introduction paragraph for the post.
[/paragraph]

[heading level=2]
Main Heading
[/heading]

[list type=unordered]
- First item
- Second item
[/list]

[quote]
"Automation simplifies everything."
[/quote]
```

---

## Directory Structure

```plaintext
wordpress-post-automation/
├── main.py                  # Main execution script
├── config.py                # Configuration settings
├── wordpress_actions.py     # Core WordPress interactions
├── parser.py                # Text file parser
├── topost/                  # Directory for post files
│   ├── post1.txt
│   ├── post2.txt
├── processed/               # Successfully processed files
├── failed/                  # Failed processing files
├── logs/                    # Logs directory
├── aiprompt.txt             # AI prompt for generating post files
└── README.md                # Documentation
```

---

## Usage

1. **Prepare Post Files**: Add properly formatted `.txt` files to the `topost/` directory.  
2. **Run the Tool**:
   ```bash
   python main.py
   ```
3. **Monitor Progress**: Check logs for detailed insights. Processed files move to `processed/`, while failed files move to `failed/`.

---

## Supported Content Blocks

The tool supports a variety of WordPress content blocks:

- **Paragraphs**:
  ```plaintext
  [paragraph]
  Your paragraph content goes here.
  [/paragraph]
  ```

- **Headings (Levels 1-6)**:
  ```plaintext
  [heading level=2]
  Heading Text
  [/heading]
  ```

- **Lists**:
  - Unordered:
    ```plaintext
    [list type=unordered]
    - Item 1
    - Item 2
    [/list]
    ```
  - Ordered:
    ```plaintext
    [list type=ordered]
    1. First item
    2. Second item
    [/list]
    ```

- **Quotes**:
  ```plaintext
  [quote]
  "Your inspirational quote here."
  [/quote]
  ```

- **Code Blocks**:
  ```plaintext
  [code]
  def example_function():
      print("Hello, World!")
  [/code]
  ```

---

## Time Efficiency

This tool is optimized for both speed and reliability. The typical time taken per post is:

- **90 seconds**: For simple posts with minimal metadata and content blocks.  
- **120 seconds**: For complex posts with featured images, multiple categories, and tags.

Timings include comprehensive checks for metadata validation, content formatting, and automatic retries for transient issues.

We are actively improving performance in upcoming versions to further reduce the processing time without compromising reliability.

---

## AI Prompt Integration

The `aiprompt.txt` file is a specially designed prompt for generating properly formatted `.txt` files compatible with this automation tool. Paste the contents into any AI model to create post files effortlessly.

### Example Use Case:
1. Open `aiprompt.txt` in your editor.  
2. Copy and paste the contents into an AI system like ChatGPT.  
3. Provide your input (e.g., "Create a post about Python tips").  
4. Receive a perfectly formatted `.txt` file ready for automation.

---

## Error Handling

1. **Failed Posts**:
   - Moved to the `failed/` directory for review.
   - Logs include detailed error messages.

2. **Retries**:
   - Automatic retries for temporary issues, such as delayed UI rendering.

3. **Logs**:
   - Comprehensive logs are saved in the `logs/` directory for debugging and tracking.

---

## Contributing

We welcome contributions to improve the tool. Follow these steps:

1. Fork the repository.  
2. Create a feature branch (`git checkout -b feature/YourFeature`).  
3. Commit your changes (`git commit -m 'Add YourFeature'`).  
4. Push to your branch (`git push origin feature/YourFeature`).  
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Contact

Created by **Neeraj Sihag**.  
GitHub Repository: [WordPress Post Automation](https://github.com/Neeraj-Sihag/wordpress-post-automation)  

Feel free to reach out for feedback, feature suggestions, or collaboration opportunities!
