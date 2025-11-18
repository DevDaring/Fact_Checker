import google.generativeai as genai
from typing import Dict, List, Optional
from pathlib import Path
from backend.config.settings import settings
import re
import json

class GeminiService:
    """Gemini 2.5 Flash API service with Search Grounding"""

    def __init__(self):
        """Initialize Gemini API"""
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            # Use Gemini 2.5 Flash with Google Search grounding
            self.model = genai.GenerativeModel(
                'gemini-2.0-flash-exp',
                tools='google_search_retrieval'
            )
        else:
            print("Warning: GEMINI_API_KEY not set")
            self.model = None

    def fact_check_text(self, text: str) -> Dict[str, any]:
        """
        Fact-check text using Gemini with Search Grounding

        Args:
            text: Text to fact-check

        Returns:
            Dictionary with response and citations
        """
        if not self.model:
            raise Exception("Gemini API not initialized. Please check GEMINI_API_KEY.")

        prompt = f"""You are a fact-checking assistant. Analyze the following statement and verify its accuracy using reliable sources.

Statement: "{text}"

Please provide:
1. A clear verdict (True, False, Partially True, or Unverifiable)
2. A detailed explanation with evidence
3. Key facts and context
4. Sources and citations

Be objective and cite specific sources."""

        try:
            response = self.model.generate_content(prompt)

            # Extract citations from grounding metadata if available
            citations = self._extract_citations(response)

            return {
                "response": response.text,
                "citations": citations
            }

        except Exception as e:
            raise Exception(f"Error during fact-checking: {str(e)}")

    def fact_check_image(self, image_path: str) -> Dict[str, any]:
        """
        Fact-check image using Gemini with Search Grounding

        Args:
            image_path: Path to the image file

        Returns:
            Dictionary with response and citations
        """
        if not self.model:
            raise Exception("Gemini API not initialized. Please check GEMINI_API_KEY.")

        # Upload image
        try:
            from PIL import Image
            img = Image.open(image_path)

            prompt = """You are a fact-checking assistant. Analyze this image and verify the claims or information it contains.

Please provide:
1. Description of what the image shows
2. Verification of any visible claims, text, or information
3. Context and background information
4. Assessment of authenticity (if applicable)
5. Sources and citations for verification

Be thorough and cite reliable sources."""

            response = self.model.generate_content([prompt, img])

            # Extract citations
            citations = self._extract_citations(response)

            return {
                "response": response.text,
                "citations": citations
            }

        except Exception as e:
            raise Exception(f"Error during image fact-checking: {str(e)}")

    def _extract_citations(self, response) -> List[Dict]:
        """
        Extract citations from Gemini response

        Args:
            response: Gemini API response

        Returns:
            List of citation dictionaries
        """
        citations = []

        try:
            # Check if response has grounding metadata
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]

                # Check for grounding metadata
                if hasattr(candidate, 'grounding_metadata'):
                    grounding = candidate.grounding_metadata

                    # Extract grounding chunks/sources
                    if hasattr(grounding, 'grounding_chunks'):
                        for chunk in grounding.grounding_chunks:
                            if hasattr(chunk, 'web'):
                                web = chunk.web
                                citation = {
                                    "title": getattr(web, 'title', 'Source'),
                                    "url": getattr(web, 'uri', ''),
                                    "snippet": getattr(chunk, 'content', '')
                                }
                                citations.append(citation)

                    # Extract web search queries
                    if hasattr(grounding, 'web_search_queries'):
                        for query in grounding.web_search_queries:
                            # This is just the query, not a citation
                            pass

            # If no grounding metadata, try to extract URLs from response text
            if not citations:
                citations = self._extract_urls_from_text(response.text)

        except Exception as e:
            print(f"Error extracting citations: {e}")
            # Try fallback URL extraction
            citations = self._extract_urls_from_text(response.text)

        return citations

    def _extract_urls_from_text(self, text: str) -> List[Dict]:
        """
        Extract URLs from response text as fallback

        Args:
            text: Response text

        Returns:
            List of citation dictionaries
        """
        citations = []

        # Regular expression to find URLs
        url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        urls = re.findall(url_pattern, text)

        for url in urls:
            citations.append({
                "title": "Source",
                "url": url,
                "snippet": ""
            })

        return citations

    def generate_summary(self, text: str, max_words: int = 100) -> str:
        """
        Generate a summary of the text

        Args:
            text: Text to summarize
            max_words: Maximum words in summary

        Returns:
            Summary text
        """
        if not self.model:
            raise Exception("Gemini API not initialized. Please check GEMINI_API_KEY.")

        prompt = f"Summarize the following text in {max_words} words or less:\n\n{text}"

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")
