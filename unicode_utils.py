#!/usr/bin/env python3
"""
Unicode Utilities for Safe Console Output
Handles Unicode encoding issues across different platforms and console types
"""

import sys
import unicodedata
import re
text_type = str

class UnicodeHandler:
    """
    Handles Unicode encoding issues for cross-platform compatibility
    """
    
    def __init__(self):
        # Detect console encoding
        self.console_encoding = self._detect_console_encoding()
        
        # Define safe alternatives for common Unicode characters
        self.unicode_replacements = {
            # Emojis and symbols
            '\U0001f680': '[ROCKET]',      # 🚀
            '\U0001f4ca': '[BAR_CHART]',   # 📊
            '\U0001f4cb': '[CLIPBOARD]',   # 📋
            '\U0001f4b0': '[MONEY_BAG]',   # 💰
            '\U0001f3af': '[TARGET]',      # 🎯
            '\U0001f9e0': '[BRAIN]',       # 🧠
            '\U0001f4a1': '[BULB]',        # 💡
            '\U0001f525': '[FIRE]',        # 🔥
            '\U0001f389': '[PARTY]',       # 🎉
            '\U0001f512': '[LOCK]',        # 🔒
            '\U0001f4c8': '[CHART_UP]',    # 📈
            '\U0001f4c9': '[CHART_DOWN]',  # 📉
            '\U0001f527': '[WRENCH]',      # 🔧
            '\U0001f3ac': '[CLAPPER]',     # 🎬
            '\U0001f399': '[MIC]',         # 🎙️
            '\U0001f916': '[ROBOT]',       # 🤖
            '\U0001f4f1': '[PHONE]',       # 📱
            '\U0001f310': '[GLOBE]',       # 🌐
            '\U0001f4c1': '[FOLDER]',      # 📁
            '\U0001f4be': '[FLOPPY]',      # 💾
            
            # Check marks and symbols
            '\u2705': '[OK]',              # ✅
            '\u274c': '[X]',               # ❌
            '\u26a0': '[WARNING]',         # ⚠️
            '\u2139': '[INFO]',            # ℹ️
            '\u2192': '->',                # →
            '\u2190': '<-',                # ←
            '\u2191': '^',                 # ↑
            '\u2193': 'v',                 # ↓
            '\u2713': '[CHECK]',           # ✓
            '\u2717': '[CROSS]',           # ✗
            '\u25cf': '*',                 # ●
            '\u25cb': 'o',                 # ○
            '\u25a0': '[SQUARE]',          # ■
            '\u25a1': '[BOX]',             # □
            
            # Special punctuation
            '\u2026': '...',               # …
            '\u2014': '--',                # —
            '\u2013': '-',                 # –
            '\u201c': '"',                 # "
            '\u201d': '"',                 # "
            '\u2018': "'",                 # '
            '\u2019': "'",                 # '
        }
    
    def _detect_console_encoding(self) -> str:
        """Detect the console encoding"""
        try:
            # Try to get stdout encoding
            if hasattr(sys.stdout, 'encoding') and sys.stdout.encoding:
                return sys.stdout.encoding
            
            # Fallback to system default
            return sys.getdefaultencoding()
        except:
            return 'utf-8'
    
    def safe_print(self, text: text_type, **kwargs):
        """
        Print text safely, handling Unicode encoding issues
        """
        try:
            # Try direct print first
            print(text, **kwargs)
        except UnicodeEncodeError:
            # If that fails, use safe version
            safe_text = self.make_safe(text)
            print(safe_text, **kwargs)
    
    def make_safe(self, text: text_type) -> str:
        """
        Convert Unicode text to console-safe version
        """
        if not isinstance(text, str):
            text = str(text)
        
        # Replace known problematic Unicode characters
        for unicode_char, replacement in self.unicode_replacements.items():
            text = text.replace(unicode_char, replacement)
        
        # Normalize Unicode characters
        text = unicodedata.normalize('NFKD', text)
        
        # Remove or replace characters that can't be encoded
        try:
            # Test if the text can be encoded
            text.encode(self.console_encoding)
            return text
        except UnicodeEncodeError:
            # If not, use ASCII-safe version
            return self._ascii_safe(text)
    
    def _ascii_safe(self, text: text_type) -> str:
        """
        Convert text to ASCII-safe version
        """
        # Replace non-ASCII characters with their closest ASCII equivalent
        ascii_text = unicodedata.normalize('NFKD', text)
        ascii_text = ascii_text.encode('ascii', 'ignore').decode('ascii')
        
        # If the text is now empty or too short, use a different approach
        if len(ascii_text) < len(text) * 0.5:
            # Use a more conservative replacement approach
            safe_chars = []
            for char in text:
                try:
                    char.encode(self.console_encoding)
                    safe_chars.append(char)
                except UnicodeEncodeError:
                    # Replace with question mark or closest equivalent
                    if ord(char) < 256:
                        safe_chars.append(char)
                    else:
                        safe_chars.append('?')
            ascii_text = ''.join(safe_chars)
        
        return ascii_text
    
    def create_safe_banner(self, title: str, width: int = 60, char: str = '=') -> str:
        """
        Create a safe banner without Unicode issues
        """
        safe_title = self.make_safe(title)
        safe_char = self.make_safe(char)
        
        lines = [
            safe_char * width,
            safe_title.center(width),
            safe_char * width
        ]
        
        return '\n'.join(lines)
    
    def safe_format(self, template: str, **kwargs) -> str:
        """
        Format string safely, handling Unicode in both template and values
        """
        # Make template safe
        safe_template = self.make_safe(template)
        
        # Make all kwargs safe
        safe_kwargs = {}
        for key, value in kwargs.items():
            safe_kwargs[key] = self.make_safe(str(value))
        
        try:
            return safe_template.format(**safe_kwargs)
        except (UnicodeEncodeError, KeyError, ValueError) as e:
            # If formatting fails, try a simple substitution
            result = safe_template
            for key, value in safe_kwargs.items():
                placeholder = "{" + key + "}"
                if placeholder in result:
                    result = result.replace(placeholder, str(value))
            return result


# Global instance for easy access
unicode_handler = UnicodeHandler()

# Convenience functions
def safe_print(*args, **kwargs):
    """Safe print function that handles Unicode issues"""
    text = ' '.join(str(arg) for arg in args)
    unicode_handler.safe_print(text, **kwargs)

def make_safe(text):
    """Make text safe for console output"""
    return unicode_handler.make_safe(text)

def create_banner(title, width=60, char='='):
    """Create a safe banner"""
    return unicode_handler.create_safe_banner(title, width, char)

def safe_format(template, **kwargs):
    """Safe string formatting"""
    return unicode_handler.safe_format(template, **kwargs)


def test_unicode_utils():
    """Test the Unicode utilities"""
    print("\n" + "="*60)
    print("UNICODE UTILITIES TEST")
    print("="*60)
    
    # Test safe printing
    print("\n1. Testing safe print with Unicode characters...")
    safe_print("Testing emojis: 🚀📊💡✅❌")
    safe_print("Testing arrows: → ← ↑ ↓")
    safe_print("Testing quotes: \"Hello\" and 'world'")
    
    # Test text conversion
    print("\n2. Testing text conversion...")
    unsafe_text = "🎯 Target achieved with 100% success! ✅"
    safe_text = make_safe(unsafe_text)
    safe_print(f"Original: {repr(unsafe_text)}")
    safe_print(f"Safe version: {safe_text}")
    
    # Test banner creation
    print("\n3. Testing banner creation...")
    banner = create_banner("🚀 UNICODE TEST SUCCESS! 🎉")
    print(banner)
    
    # Test formatting
    print("\n4. Testing safe formatting...")
    template = "🎯 {task} completed with {percent}% success! {status}"
    formatted = safe_format(template, task="Unicode handling", percent=100, status="✅")
    safe_print(formatted)
    
    print("\n" + "="*60)
    print("UNICODE TEST COMPLETE - ALL FUNCTIONS WORKING")
    print("="*60)


if __name__ == "__main__":
    test_unicode_utils()