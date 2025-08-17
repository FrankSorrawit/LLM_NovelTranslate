#!/usr/bin/env python3
"""
Dual Novel Translation System
Handles translation of two complete novels with chunking, merging, and chapter splitting
"""

import json
import os
import re
import time
from pathlib import Path
from typing import List, Dict, Tuple
from openai import AzureOpenAI
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class DualNovelTranslator:
    def __init__(self, config_path: str = "config.json"):
        """Initialize the translator with configuration"""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # Setup Azure OpenAI client
        self.client = AzureOpenAI(
            azure_endpoint=self.config["azure_openai"]["endpoint"],
            api_key=self.config["azure_openai"]["api_key"],
            api_version=self.config["azure_openai"]["api_version"]
        )
        
        self.deployment_name = self.config["azure_openai"]["deployment_name"]
        self.chunk_size = 8000  # Safe word count for GPT-4o
        self.delay = self.config["translation_settings"]["delay_between_chapters"]
        
        # Novel configurations
        self.novels = {
            "matriarch": {
                "file": "Raw/Ill-Be-a-Matriarch-in-This-Life-Complete.txt",
                "title": "I'll Be a Matriarch in This Life",
                "folder": "Matriarch_Translation",
                "background": self._get_matriarch_background()
            },
            "viridescent": {
                "file": "Raw/The-Viridescent-Crown.txt", 
                "title": "The Viridescent Crown",
                "folder": "Viridescent_Translation",
                "background": self._get_viridescent_background()
            }
        }
    
    def _get_matriarch_background(self) -> str:
        """Background context for I'll Be a Matriarch in This Life"""
        return """
        NOVEL BACKGROUND - I'll Be a Matriarch in This Life:
        
        Genre: Romance, Fantasy, Reincarnation, Noble Society
        Setting: Medieval fantasy world with noble houses and political intrigue
        
        Main Character: Florentia (Tia) - A modern woman reincarnated as a child in a noble family
        Goal: To become the matriarch of her family and change their fate
        
        Key Elements:
        - Reincarnation/Time travel themes
        - Noble family politics and inheritance
        - Business and economic strategies
        - Romance subplot
        - Family relationships and loyalty
        - Medieval fantasy setting with magic elements
        
        Tone: Strategic, intelligent, with romantic and family-focused elements
        Translation Style: Maintain formal noble speech patterns, preserve character relationships and political nuances
        """
    
    def _get_viridescent_background(self) -> str:
        """Background context for The Viridescent Crown"""
        return """
        NOVEL BACKGROUND - The Viridescent Crown:
        
        Genre: Romance, Fantasy, Royal Court, Political Intrigue
        Setting: Fantasy kingdom with royal court politics and magical elements
        
        Main Character: Ran - A woman navigating royal court politics and romance
        Goal: Survival and finding her place in the dangerous royal court
        
        Key Elements:
        - Royal court intrigue and politics
        - Romance with multiple potential interests
        - Magic and fantasy world-building
        - Power struggles and conspiracies
        - Character growth and adaptation
        - Complex relationships and alliances
        
        Tone: Dramatic, romantic, with political tension
        Translation Style: Maintain royal/court language formality, preserve romantic tension and political complexity
        """

    def split_into_chunks(self, text: str, max_words: int = 8000) -> List[str]:
        """Split text into chunks of approximately max_words"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_count = 0
        
        for word in words:
            current_chunk.append(word)
            current_count += 1
            
            if current_count >= max_words:
                # Try to find a good break point (paragraph or sentence)
                chunk_text = ' '.join(current_chunk)
                last_paragraph = chunk_text.rfind('\n\n')
                last_sentence = chunk_text.rfind('. ')
                
                if last_paragraph > len(chunk_text) * 0.8:
                    break_point = last_paragraph + 2
                elif last_sentence > len(chunk_text) * 0.8:
                    break_point = last_sentence + 2
                else:
                    break_point = len(chunk_text)
                
                chunks.append(chunk_text[:break_point])
                remaining = chunk_text[break_point:].strip()
                current_chunk = remaining.split() if remaining else []
                current_count = len(current_chunk)
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

    def translate_chunk(self, chunk: str, novel_key: str, chunk_num: int, total_chunks: int) -> str:
        """Translate a single chunk using Azure OpenAI"""
        novel_info = self.novels[novel_key]
        
        system_prompt = f"""You are a professional translator specializing in romance fantasy novels. 
        
        {novel_info['background']}
        
        Translate the following text from English to Thai while:
        1. Maintaining the original meaning and emotional tone
        2. Preserving character names and relationships
        3. Adapting cultural references appropriately for Thai readers
        4. Keeping the narrative flow and style consistent
        5. Maintaining proper formatting and paragraph structure
        
        This is chunk {chunk_num} of {total_chunks} from "{novel_info['title']}".
        Ensure continuity with the overall story context."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Translate this text to Thai:\n\n{chunk}"}
                ],
                max_tokens=4000,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error translating chunk {chunk_num}: {str(e)}")
            return f"[Translation Error for chunk {chunk_num}]"

    def translate_novel(self, novel_key: str) -> str:
        """Translate entire novel by chunks and merge"""
        novel_info = self.novels[novel_key]
        print(f"\n=== Translating {novel_info['title']} ===")
        
        # Read the novel
        with open(novel_info['file'], 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split into chunks
        chunks = self.split_into_chunks(content, self.chunk_size)
        print(f"Split into {len(chunks)} chunks")
        
        # Translate each chunk
        translated_chunks = []
        for i, chunk in enumerate(chunks, 1):
            print(f"Translating chunk {i}/{len(chunks)}...")
            translated = self.translate_chunk(chunk, novel_key, i, len(chunks))
            translated_chunks.append(translated)
            
            # Save progress
            progress_file = f"{novel_key}_translation_progress.json"
            with open(progress_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'completed_chunks': i,
                    'total_chunks': len(chunks),
                    'translated_chunks': translated_chunks
                }, f, ensure_ascii=False, indent=2)
            
            if i < len(chunks):  # Don't delay after last chunk
                time.sleep(self.delay)
        
        # Merge all chunks
        full_translation = '\n\n'.join(translated_chunks)
        return full_translation

    def save_as_txt_and_pdf(self, content: str, novel_key: str):
        """Save translated content as both TXT and PDF"""
        novel_info = self.novels[novel_key]
        base_name = f"{novel_key}_translated"
        
        # Save as TXT
        txt_path = f"{base_name}.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved TXT: {txt_path}")
        
        # Save as PDF
        pdf_path = f"{base_name}.pdf"
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Create custom style for Thai text
        thai_style = ParagraphStyle(
            'ThaiStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            leading=16,
            spaceAfter=12
        )
        
        story = []
        story.append(Paragraph(f"<b>{novel_info['title']} (Thai Translation)</b>", styles['Title']))
        story.append(Spacer(1, 0.2*inch))
        
        # Split content into paragraphs and add to PDF
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para.strip(), thai_style))
                story.append(Spacer(1, 0.1*inch))
        
        doc.build(story)
        print(f"Saved PDF: {pdf_path}")

    def translate_both_novels(self):
        """Main method to translate both novels completely"""
        print("=== DUAL NOVEL TRANSLATION SYSTEM ===")
        print("Novels to translate:")
        for key, info in self.novels.items():
            print(f"- {info['title']} ({info['file']})")
        
        results = {}
        
        for novel_key in self.novels.keys():
            try:
                # Translate the novel
                translated_content = self.translate_novel(novel_key)
                
                # Save as TXT and PDF
                self.save_as_txt_and_pdf(translated_content, novel_key)
                
                results[novel_key] = {
                    'status': 'completed',
                    'word_count': len(translated_content.split())
                }
                
                print(f"\n✅ Completed {self.novels[novel_key]['title']}")
                print(f"   - Words: {results[novel_key]['word_count']}")
                
            except Exception as e:
                print(f"\n❌ Error translating {self.novels[novel_key]['title']}: {str(e)}")
                results[novel_key] = {'status': 'failed', 'error': str(e)}
        
        # Save final report
        with open('translation_report.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print("\n=== TRANSLATION COMPLETE ===")
        print("Check translation_report.json for detailed results")
        return results

if __name__ == "__main__":
    translator = DualNovelTranslator()
    translator.translate_both_novels()