#!/usr/bin/env python3
"""
Thai PDF Font Fixer
Creates PDFs with proper Thai font support to avoid black boxes
"""

import os
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER

class ThaiPDFCreator:
    def __init__(self):
        self.setup_thai_fonts()
        
    def setup_thai_fonts(self):
        """Setup Thai fonts for PDF generation"""
        print("Setting up Thai fonts...")
        
        # Try to use system fonts first
        self.thai_font = None
        
        # Common Thai fonts on Windows
        windows_fonts = [
            "C:/Windows/Fonts/tahoma.ttf",
            "C:/Windows/Fonts/tahomabd.ttf", 
            "C:/Windows/Fonts/cordia.ttf",
            "C:/Windows/Fonts/cordiau.ttf",
            "C:/Windows/Fonts/angsana.ttf",
            "C:/Windows/Fonts/browalia.ttf"
        ]
        
        for font_path in windows_fonts:
            if os.path.exists(font_path):
                try:
                    font_name = Path(font_path).stem
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    self.thai_font = font_name
                    print(f"✅ Registered Thai font: {font_name}")
                    break
                except Exception as e:
                    print(f"Failed to register {font_path}: {e}")
                    continue
        
        if not self.thai_font:
            print("❌ No Thai fonts found, using Helvetica")
            self.thai_font = 'Helvetica'  # Fallback
    
    def create_thai_pdf_simple(self, text_content: str, output_file: str, title: str):
        """Create PDF using simple text approach with Thai font"""
        print(f"Creating Thai PDF (Simple): {output_file}")
        
        doc = SimpleDocTemplate(
            output_file, 
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Create styles with Thai font
        styles = getSampleStyleSheet()
        
        # Title style
        title_style = ParagraphStyle(
            'ThaiTitle',
            parent=styles['Title'],
            fontName=self.thai_font,
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            spaceAfter=30
        )
        
        # Body style for Thai text
        thai_style = ParagraphStyle(
            'ThaiBody',
            parent=styles['Normal'],
            fontName=self.thai_font,
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceAfter=12,
            wordWrap='LTR'
        )
        
        story = []
        
        # Add title
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 0.5*inch))
        
        # Process content in smaller chunks to avoid issues
        paragraphs = text_content.split('\n\n')
        
        for i, para in enumerate(paragraphs):
            if para.strip():
                # Clean the paragraph
                clean_para = para.strip().replace('\n', ' ')
                
                # Split very long paragraphs
                if len(clean_para) > 1000:
                    sentences = clean_para.split('. ')
                    current_chunk = ""
                    
                    for sentence in sentences:
                        if len(current_chunk + sentence) < 800:
                            current_chunk += sentence + ". "
                        else:
                            if current_chunk:
                                story.append(Paragraph(current_chunk.strip(), thai_style))
                            current_chunk = sentence + ". "
                    
                    if current_chunk:
                        story.append(Paragraph(current_chunk.strip(), thai_style))
                else:
                    story.append(Paragraph(clean_para, thai_style))
                
                # Add page break every 50 paragraphs to manage memory
                if i > 0 and i % 50 == 0:
                    story.append(PageBreak())
        
        try:
            doc.build(story)
            print(f"✅ Thai PDF created successfully: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to create PDF: {e}")
            return False

def main():
    """Create Thai-compatible PDFs for both novels"""
    creator = ThaiPDFCreator()
    
    novels = [
        {
            'input': 'matriarch_translated_fixed.txt',
            'title': "I'll Be a Matriarch in This Life (การแปลภาษาไทย)",
            'output': 'matriarch_thai_font.pdf'
        },
        {
            'input': 'viridescent_translated_fixed.txt', 
            'title': "The Viridescent Crown (การแปลภาษาไทย)",
            'output': 'viridescent_thai_font.pdf'
        }
    ]
    
    print("=== CREATING THAI FONT PDFs ===\n")
    
    for novel in novels:
        if os.path.exists(novel['input']):
            print(f"Processing: {novel['title']}")
            
            # Read content
            with open(novel['input'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create PDF
            creator.create_thai_pdf_simple(content, novel['output'], novel['title'])
            
            print(f"✅ Completed: {novel['output']}\n")
        else:
            print(f"❌ File not found: {novel['input']}\n")
    
    print("=== THAI PDF CREATION COMPLETE ===")
    print("\nNew Thai-compatible PDF files:")
    print("- matriarch_thai_font.pdf")
    print("- viridescent_thai_font.pdf")
    print("\nThese PDFs should display Thai characters correctly!")

if __name__ == "__main__":
    main()