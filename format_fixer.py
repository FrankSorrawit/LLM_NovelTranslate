#!/usr/bin/env python3
"""
Text Format Fixer
Fixes line length and UTF-8 encoding issues for translated novels
"""

import os
import re
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class TextFormatter:
    def __init__(self):
        self.max_line_length = 80  # Characters per line for Notepad
        
    def wrap_text_lines(self, text: str, max_length: int = 80) -> str:
        """Wrap long lines to fit in Notepad properly"""
        lines = text.split('\n')
        wrapped_lines = []
        
        for line in lines:
            if len(line) <= max_length:
                wrapped_lines.append(line)
            else:
                # Split long lines at word boundaries
                words = line.split(' ')
                current_line = ""
                
                for word in words:
                    if len(current_line + " " + word) <= max_length:
                        if current_line:
                            current_line += " " + word
                        else:
                            current_line = word
                    else:
                        if current_line:
                            wrapped_lines.append(current_line)
                        current_line = word
                
                if current_line:
                    wrapped_lines.append(current_line)
        
        return '\n'.join(wrapped_lines)
    
    def fix_txt_format(self, input_file: str, output_file: str):
        """Fix TXT file formatting for better readability"""
        print(f"Fixing TXT format: {input_file} -> {output_file}")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Wrap long lines
        formatted_content = self.wrap_text_lines(content, self.max_line_length)
        
        # Add proper paragraph spacing
        formatted_content = re.sub(r'\n\n+', '\n\n', formatted_content)
        
        # Save with proper UTF-8 encoding
        with open(output_file, 'w', encoding='utf-8-sig') as f:  # UTF-8 with BOM for Windows
            f.write(formatted_content)
        
        print(f"✅ Fixed TXT saved: {output_file}")

def main():
    """Fix both translated novels"""
    formatter = TextFormatter()
    
    novels = [
        {
            'input': 'matriarch_translated.txt',
            'output': 'matriarch_translated_fixed.txt'
        },
        {
            'input': 'viridescent_translated.txt',
            'output': 'viridescent_translated_fixed.txt'
        }
    ]
    
    print("=== FIXING TRANSLATION FORMATS ===\n")
    
    for novel in novels:
        if os.path.exists(novel['input']):
            formatter.fix_txt_format(novel['input'], novel['output'])
            print()
        else:
            print(f"❌ File not found: {novel['input']}\n")
    
    print("=== FORMAT FIXING COMPLETE ===")

if __name__ == "__main__":
    main()