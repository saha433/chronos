#!/usr/bin/env python3

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from typing import List, Dict, Any
import google.generativeai as genai
import requests
from dotenv import load_dotenv

app = Flask(__name__, static_folder='.')
CORS(app)  # Enable CORS for frontend communication

# Load environment variables
load_dotenv()

class TextReconstructionService:
    """Service class for text reconstruction."""
    
    def __init__(self):
        """Initialize the service with API configurations."""
        # Initialize Gemini API
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Initialize web search API
        self.search_api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
        self.search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        
        if not self.search_api_key or not self.search_engine_id:
            raise ValueError("GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID required")
    
    def reconstruct_text_with_ai(self, input_text: str) -> str:
        """Reconstruct text using Google Gemini API."""
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
        """Find contextual sources using web search."""
        search_query = self._extract_search_terms(reconstructed_text)
        
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
        """Extract key terms from reconstructed text for better search results."""
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'was', 'are', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        words = text.lower().split()
        keywords = [word.strip('.,!?;:"') for word in words if word.lower() not in common_words and len(word) > 2]
        
        return ' '.join(keywords[:7])

# Initialize service
service = TextReconstructionService()

@app.route('/')
def index():
    """Serve the main HTML page."""
    return send_from_directory('.', 'index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'message': 'API is running'})

@app.route('/api/reconstruct', methods=['POST'])
def reconstruct_text():
    """Main endpoint to reconstruct text."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        input_text = data['text'].strip()
        
        if not input_text:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        # Step 1: Reconstruct text
        reconstructed_text = service.reconstruct_text_with_ai(input_text)
        
        # Step 2: Search for sources
        sources = service.search_contextual_sources(reconstructed_text)
        
        # Step 3: Return results
        return jsonify({
            'success': True,
            'original_text': input_text,
            'reconstructed_text': reconstructed_text,
            'sources': sources
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print("🚀 Starting Text Reconstruction API Server...")
    print(f"📡 Server running on port {port}")
    print("✨ Ready to process requests!")
    app.run(host='0.0.0.0', port=port, debug=False)