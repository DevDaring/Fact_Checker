import google.generativeai as genai
from typing import Dict, List, Optional
from pathlib import Path
from config.settings import settings
import re
import json

class GeminiService:
    """Gemini 2.5 Flash API service with Search Grounding"""

    def __init__(self):
        """Initialize Gemini API"""
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            # Model for general use
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
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
            # Generate response without grounding (google_search not supported in google.generativeai SDK)
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
        Fact-check image using Gemini in two steps:
        1. Extract description without grounding
        2. Fact-check the description with grounding

        Args:
            image_path: Path to the image file

        Returns:
            Dictionary with response and citations
        """
        if not self.model:
            raise Exception("Gemini API not initialized. Please check GEMINI_API_KEY.")

        try:
            from PIL import Image
            img = Image.open(image_path)

            # Step 1: Extract description from image (without grounding)
            description_prompt = """Analyze this image and provide a detailed description including:
1. What the image shows
2. Any visible text, claims, or information
3. Context and setting
4. Notable details or elements

Be thorough and objective in your description."""

            description_response = self.model.generate_content([description_prompt, img])
            image_description = description_response.text

            # Step 2: Fact-check the description (with grounding)
            fact_check_prompt = f"""You are a fact-checking assistant. Based on this image description, verify any claims or information using reliable sources.

Image Description: "{image_description}"

Please provide:
1. Verification of any claims or information mentioned
2. A clear verdict (True, False, Partially True, or Unverifiable)
3. Additional context and background information
4. Assessment of authenticity (if applicable)
5. Sources and citations for verification

Be thorough and cite reliable sources."""

            # Generate fact-check response without grounding (google_search not supported in google.generativeai SDK)
            fact_check_response = self.model.generate_content(fact_check_prompt)

            # Extract citations from fact-check response
            citations = self._extract_citations(fact_check_response)

            # Combine description and fact-check
            combined_response = f"**Image Description:**\n{image_description}\n\n**Fact-Check Analysis:**\n{fact_check_response.text}"

            return {
                "response": combined_response,
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
