"""
Parser for WordPress post files.
Handles metadata extraction and content block parsing.
"""
import re
from typing import Optional, Dict, List, Tuple
from config import PostConfig

class PostParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def parse_file(self) -> PostConfig:
        """Parse the post file and return PostConfig."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Split metadata and content sections
        parts = content.split("# --- Content ---")
        if len(parts) != 2:
            raise ValueError(f"Invalid file format in {self.file_path}. Missing content delimiter.")
            
        metadata = self._parse_metadata(parts[0])
        processed_content = self._parse_content(parts[1])
        
        return PostConfig(
            title=metadata.get('title', '').strip('"'),
            content=processed_content,
            category=metadata.get('category', '').strip('"'),
            tags=metadata.get('tags', '').strip('"'),
            media_index=self._parse_media_index(metadata.get('featured_image', '')),
            status=metadata.get('status', 'draft').strip('"')
        )
    
    def _parse_metadata(self, metadata_text: str) -> Dict[str, str]:
        """Parse metadata section into dictionary."""
        metadata = {}
        for line in metadata_text.strip().split('\n'):
            if ':' in line and not line.startswith('#'):
                key, value = line.split(':', 1)
                # Remove comments and clean up value
                value = value.split('#')[0].strip()
                metadata[key.strip()] = value
        return metadata
    
    def _parse_media_index(self, media_value: str) -> Optional[int]:
        """Parse media index from featured_image value."""
        try:
            media_value = media_value.strip('"')
            if media_value.isdigit():
                return int(media_value)
            return None
        except:
            return None
    
    def _parse_content(self, content_text: str) -> str:
        """Parse content blocks into HTML."""
        processed_content = []
        current_block = []
        in_block = False
        block_type = None
        
        for line in content_text.split('\n'):
            line = line.strip()
            
            # Skip comments
            if line.startswith('#'):
                continue
                
            # Check for block start
            if line.startswith('[') and ']' in line:
                if in_block:  # Process previous block if exists
                    processed_content.append(
                        self._process_block(block_type, current_block)
                    )
                    current_block = []
                
                block_type = self._get_block_type(line)
                in_block = True
                continue
                
            # Check for block end
            if line.startswith('[/'):
                if in_block:
                    processed_content.append(
                        self._process_block(block_type, current_block)
                    )
                    current_block = []
                    in_block = False
                continue
                
            # Add content to current block
            if in_block and line:
                current_block.append(line)
        
        # Process any remaining block
        if in_block and current_block:
            processed_content.append(
                self._process_block(block_type, current_block)
            )
        
        # Filter out None values and join with double newlines
        return '\n\n'.join([p for p in processed_content if p])
    
    def _get_block_type(self, line: str) -> tuple[str, Dict[str, str]]:
        """Extract block type and attributes from block start line."""
        match = re.match(r'\[(\w+)(?:\s+([^\]]+))?\]', line)
        if not match:
            return ('paragraph', {})
            
        block_type = match.group(1)
        attrs_str = match.group(2) or ''
        
        # Parse attributes
        attrs = {}
        for attr in attrs_str.split():
            if '=' in attr:
                key, value = attr.split('=')
                attrs[key] = value
                
        return (block_type, attrs)
    
    def _process_block(self, block_info: tuple[str, Dict[str, str]], lines: List[str]) -> str:
        """Convert block content to HTML."""
        block_type, attrs = block_info
        content = '\n'.join(lines)
        
        if block_type == 'paragraph':
            # Convert markdown links to HTML
            content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', content)
            return f"<p>{content}</p>"
            
        elif block_type == 'heading':
            level = attrs.get('level', '2')
            return f"<h{level}>{content}</h{level}>"
            
        elif block_type == 'list':
            list_type = attrs.get('type', 'unordered')
            tag = 'ul' if list_type == 'unordered' else 'ol'
            items = []
            for line in content.split('\n'):
                if line.strip():
                    # Remove leading markers (-, 1., etc.)
                    item = re.sub(r'^[-\d\s.]+', '', line).strip()
                    items.append(f"<li>{item}</li>")
            return f"<{tag}>\n{''.join(items)}\n</{tag}>"
            
        elif block_type == 'quote':
            return f"<blockquote>{content}</blockquote>"
            
        elif block_type == 'code':
            return f"<pre><code>{content}</code></pre>"
            
        elif block_type == 'embed':
            return f"[embed]{content}[/embed]"
            
        return content

# Example usage when run directly
if __name__ == "__main__":
    # Test parser
    parser = PostParser("topost/post1.txt")
    post_config = parser.parse_file()
    print(f"Title: {post_config.title}")
    print(f"Media Index: {post_config.media_index}")
    print("Content preview:", post_config.content[:200])