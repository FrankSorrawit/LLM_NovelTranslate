#!/usr/bin/env python3
"""
Translation Starter Script
Interactive script to choose which novels to translate
"""

import os
import sys
from dual_novel_translator import DualNovelTranslator

def main():
    print("=" * 60)
    print("           DUAL NOVEL TRANSLATION SYSTEM")
    print("=" * 60)
    print()
    print("Available novels:")
    print("1. I'll Be a Matriarch in This Life (405,953 words)")
    print("2. The Viridescent Crown (342,077 words)")
    print("3. Both novels (748,030 words total)")
    print("4. Exit")
    print()
    
    while True:
        choice = input("Select option (1-4): ").strip()
        
        if choice == "4":
            print("Goodbye!")
            sys.exit(0)
        
        if choice in ["1", "2", "3"]:
            break
        
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
    
    # Initialize translator
    translator = DualNovelTranslator()
    
    if choice == "1":
        print("\n🚀 Starting translation of 'I'll Be a Matriarch in This Life'...")
        print("Estimated time: ~1.5 hours")
        print("Estimated cost: ~$12")
        
        if input("\nProceed? (y/n): ").lower().startswith('y'):
            translate_single_novel(translator, "matriarch")
    
    elif choice == "2":
        print("\n🚀 Starting translation of 'The Viridescent Crown'...")
        print("Estimated time: ~1 hour")
        print("Estimated cost: ~$10")
        
        if input("\nProceed? (y/n): ").lower().startswith('y'):
            translate_single_novel(translator, "viridescent")
    
    elif choice == "3":
        print("\n🚀 Starting translation of BOTH novels...")
        print("Estimated time: ~3-4 hours")
        print("Estimated cost: ~$22")
        print("\nThis will translate both novels sequentially.")
        
        if input("\nProceed? (y/n): ").lower().startswith('y'):
            translator.translate_both_novels()

def translate_single_novel(translator, novel_key):
    """Translate a single novel"""
    try:
        print(f"\n=== Translating {translator.novels[novel_key]['title']} ===")
        
        # Translate the novel
        translated_content = translator.translate_novel(novel_key)
        
        # Save as TXT and PDF
        translator.save_as_txt_and_pdf(translated_content, novel_key)
        
        print(f"\n✅ Translation completed!")
        print(f"   - Novel: {translator.novels[novel_key]['title']}")
        print(f"   - Output files: {novel_key}_translated.txt and {novel_key}_translated.pdf")
        
    except Exception as e:
        print(f"\n❌ Translation failed: {str(e)}")

if __name__ == "__main__":
    main()