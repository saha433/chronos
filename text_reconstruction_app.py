#!/usr/bin/env python3

import os
import json
import time
from typing import List, Dict, Any
import google.generativeai as genai
import requests
from dotenv import load_dotenv


class TextReconstructionApp:
    
    def __init__(self):
        load_dotenv()
        
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        self.search_api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
        self.search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        
        if not self.search_api_key or not self.search_engine_id:
            raise ValueError("GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID required")
    
    def reconstruct_text_with_ai(self, input_text: str) -> str:
        prompt = f"""
        You are a text reconstruction expert. Please analyze and reconstruct the following text:

        Original text: "{input_text}"

        Please perform the following tasks:
        1. Expand all slang, abbreviations, and acronyms (e.g., "lol" → "laughing out loud", "brb" → "be right back")
        2. Explain the context and meaning of any colloquial expressions (e.g., "epic fail" → "a significant and embarrassing mistake or failure")
        3. Fill in any missing words or complete incomplete sentences to make the text coherent
        4. Maintain the original tone and intent while making the text clear and professional
        5. If the text appears to be a fragment of a larger conversation, provide context about what might have been discussed

        Return only the reconstructed text without any additional commentary or formatting.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Error calling Gemini API: {str(e)}")
    
    def search_contextual_sources(self, reconstructed_text: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        Step 3: Find contextual sources using web search.
        
        Args:
            reconstructed_text: The AI-reconstructed text to search for
            num_results: Number of search results to return
            
        Returns:
            List of dictionaries containing title, link, and snippet for each result
        """
        search_query = self._extract_search_terms(reconstructed_text)
        
        #Use Google Custom Search API
        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': self.search_api_key,
            'cx': self.search_engine_id,
            'q': search_query,
            'num': num_results
        }
        
        try:
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('items', []):
                results.append({
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', '')
                })
            
            return results
            
        except requests.RequestException as e:
            raise Exception(f"Error performing web search: {str(e)}")
    
    def _extract_search_terms(self, text: str) -> str:
        """
        Extract key terms from reconstructed text for better search results.
        
        Args:
            text: The reconstructed text
            
        Returns:
            String of key terms for searching
        """
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'was', 'are', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        words = text.lower().split()
        keywords = [word.strip('.,!?;:"') for word in words if word.lower() not in common_words and len(word) > 2]
       
        return ' '.join(keywords[:7])
    
    def generate_report(self, original_text: str, reconstructed_text: str, sources: List[Dict[str, str]]) -> str:
        """
        Step 4: Generate a structured reconstruction report.
        
        Args:
            original_text: The original input text
            reconstructed_text: The AI-reconstructed text
            sources: List of contextual sources from web search
            
        Returns:
            Formatted reconstruction report
        """
        report = f"""
{'='*80}
                    TEXT RECONSTRUCTION REPORT
{'='*80}

1. ORIGINAL FRAGMENT:
   "{original_text}"

2. AI-RECONSTRUCTED TEXT:
   {reconstructed_text}

3. CONTEXTUAL SOURCES:
"""
        
        if sources:
            for i, source in enumerate(sources, 1):
                report += f"""
   {i}. {source['title']}
      Link: {source['link']}
      Summary: {source['snippet']}
"""
        else:
            report += "   No contextual sources found."
        
        report += f"""
{'='*80}
Report generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}
"""
        
        return report
    
    def process_text(self, input_text: str) -> str:
        """
        Main orchestration function that performs the complete four-step process.
        
        Args:
            input_text: The original text to reconstruct
            
        Returns:
            Complete reconstruction report
        """
        print("Starting text reconstruction process...")
        
        # Step 1: Input validation
        if not input_text.strip():
            raise ValueError("Input text cannot be empty")
        
        print("Original text received:", input_text)
        
        # Step 2: AI Reconstruction
        print("🤖 Reconstructing text with AI...")
        reconstructed_text = self.reconstruct_text_with_ai(input_text)
        print("Text reconstructed successfully")
        
        # Step 3: Web Search
        print("Searching for contextual sources...")
        sources = self.search_contextual_sources(reconstructed_text)
        print(f"Found {len(sources)} contextual sources")
        
        # Step 4: Generate Report
        print("Generating final report...")
        report = self.generate_report(input_text, reconstructed_text, sources)
        print("Report generated successfully")
        
        return report


def main():
    """Main function to run the application."""
    print("🚀 Text Reconstruction Application")
    print("=" * 50)
    
    try:
        app = TextReconstructionApp()
        
        print("\nEnter the text you want to reconstruct:")
        print("(Example: 'lol, that was epic fail. brb')")
        input_text = input("\n> ").strip()
        
        if not input_text:
            print("❌ No text provided. Exiting.")
            return
        
        report = app.process_text(input_text)
        
        print("\n" + report)
        
        save_option = input("\n💾 Save report to file? (y/n): ").lower().strip()
        if save_option in ['y', 'yes']:
            filename = f"reconstruction_report_{int(time.time())}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Report saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nPlease check your API keys and configuration.")


if __name__ == "__main__":
    main()
    
