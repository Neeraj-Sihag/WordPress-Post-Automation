"""
Content block handlers for different types of WordPress content.
Converts block syntax to HTML.
"""
import re
from typing import Dict, List, Optional

class BlockHandler:
    @staticmethod
    def paragraph(content: str) -> str:
        """Convert paragraph block to HTML."""
        # Convert markdown links to HTML
        content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', content)
        return f"<p>{content}</p>"

    @staticmethod
    def heading(content: str, level: str = "2") -> str:
        """Convert heading block to HTML."""
        return f"<h{level}>{content}</h{level}>"

    @staticmethod
    def list(content: str, list_type: str = "unordered") -> str:
        """Convert list block to HTML."""
        tag = "ul" if list_type == "unordered" else "ol"
        items = []
        
        for line in content.split('\n'):
            if line.strip():
                # Remove leading markers (-, 1., etc.)
                item = re.sub(r'^[-\d\s.]+', '', line).strip()
                items.append(f"<li>{item}</li>")
                
        return f"<{tag}>\n{''.join(items)}\n</{tag}>"

    @staticmethod
    def quote(content: str) -> str:
        """Convert quote block to HTML."""
        return f"<blockquote>{content}</blockquote>"

    @staticmethod
    def code(content: str) -> str:
        """Convert code block to HTML."""
        return f"<pre><code>{content}</code></pre>"

    @staticmethod
    def embed(content: str) -> str:
        """Convert embed block to WordPress embed shortcode."""
        return f"[embed]{content}[/embed]"

class BlockParser:
    def __init__(self):
        self.handler = BlockHandler()
        
    def parse_block(self, block_text: str) -> Optional[str]:
        """Parse a single content block and return HTML."""
        if not block_text.strip():
            return None
            
        # Extract block type and attributes
        match = re.match(r'\[(\w+)(?:\s+([^\]]+))?\](.*?)\[/\1\]', 
                        block_text, re.DOTALL)
        
        if not match:
            return None
            
        block_type, attrs_str, content = match.groups()
        
        # Parse attributes
        attrs = {}
        if attrs_str:
            for attr in attrs_str.split():
                if '=' in attr:
                    key, value = attr.split('=')
                    attrs[key] = value

        # Process block based on type
        content = content.strip()
        
        if block_type == 'paragraph':
            return self.handler.paragraph(content)
        elif block_type == 'heading':
            return self.handler.heading(content, attrs.get('level', '2'))
        elif block_type == 'list':
            return self.handler.list(content, attrs.get('type', 'unordered'))
        elif block_type == 'quote':
            return self.handler.quote(content)
        elif block_type == 'code':
            return self.handler.code(content)
        elif block_type == 'embed':
            return self.handler.embed(content)
            
        return None

    def parse_blocks(self, content: str) -> str:
        """Parse all content blocks in a string."""
        blocks = []
        current_block = []
        
        for line in content.split('\n'):
            if line.strip().startswith('[') and not line.strip().startswith('[/'):
                if current_block:
                    parsed = self.parse_block('\n'.join(current_block))
                    if parsed:
                        blocks.append(parsed)
                    current_block = []
                current_block.append(line)
            elif current_block:
                current_block.append(line)
                
        # Process last block
        if current_block:
            parsed = self.parse_block('\n'.join(current_block))
            if parsed:
                blocks.append(parsed)
                
        return '\n\n'.join(blocks)
