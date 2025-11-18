from google import genai
from google.genai import types
from typing import Dict, List, Optional
from pathlib import Path
from config.settings import settings
import re
import json

class GeminiService:
    """Gemini 2.0 Flash API service with Google Search Grounding"""

    def __init__(self):
        """Initialize Gemini API"""
        if settings.GEMINI_API_KEY:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
            self.model_name = 'gemini-2.0-flash-exp'
        else:
            print("Warning: GEMINI_API_KEY not set")
            self.client = None
            self.model_name = None

    def fact_check_text(self, text: str) -> Dict[str, any]:
        """
        Fact-check text using Gemini with Google Search Grounding

        Args:
            text: Text to fact-check

        Returns:
            Dictionary with response and citations
        """
        if not self.client:
            raise Exception("Gemini API not initialized. Please check GEMINI_API_KEY.")

        prompt = f"""You are a fact-checking assistant. Analyze the following statement and verify its accuracy using reliable sources from the web.

Statement: "{text}"

Provide your analysis in exactly 10 clear, well-structured sentences. Do not use bullet points, asterisks, or numbered lists. Write in flowing paragraphs with proper sentence structure. Include:
- A clear verdict on the accuracy
- Detailed explanation with evidence
- Key facts and context
- Reference to sources when mentioning information

Format your response as natural prose, not as a list."""

        try:
            # Use Google Search grounding
            config = types.GenerateContentConfig(
                tools=[{'google_search': {}}],
                temperature=0.7
            )
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )

            # Extract citations from grounding metadata
            citations = self._extract_citations_new(response)
            
            # Format the response text
            formatted_response = self._format_response(response.text)

            return {
                "response": formatted_response,
                "citations": citations
            }

        except Exception as e:
            raise Exception(f"Error during fact-checking: {str(e)}")

    def fact_check_image(self, image_path: str) -> Dict[str, any]:
        """
        Fact-check image using Gemini in two steps:
        1. Extract description without grounding
        2. Fact-check the description with Google Search grounding

        Args:
            image_path: Path to the image file

        Returns:
            Dictionary with response and citations
        """
        if not self.client:
            raise Exception("Gemini API not initialized. Please check GEMINI_API_KEY.")

        try:
            # Step 1: Extract description from image (without grounding)
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            description_prompt = """Analyze this image carefully. Describe what you see including any visible text, claims, people, objects, settings, and notable details. Be objective and thorough in your description."""

            # Upload image and get description
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[
                    types.Part.from_bytes(data=image_data, mime_type='image/jpeg'),
                    description_prompt
                ]
            )
            
            image_description = response.text

            # Step 2: Fact-check the description with Google Search grounding
            fact_check_prompt = f"""You are a fact-checking assistant. Based on this image description, verify any claims or information using reliable web sources.

Image Description: "{image_description}"

Provide your fact-check analysis in exactly 10 clear, well-structured sentences. Do not use bullet points, asterisks, or numbered lists. Write in flowing paragraphs with proper sentence structure. Include:
- Verification of any visible claims or information
- A clear verdict on authenticity
- Additional context and background
- Reference to sources when mentioning information

Format your response as natural prose, not as a list."""

            # Use Google Search grounding for fact-checking
            config = types.GenerateContentConfig(
                tools=[{'google_search': {}}],
                temperature=0.7
            )
            
            fact_check_response = self.client.models.generate_content(
                model=self.model_name,
                contents=fact_check_prompt,
                config=config
            )

            # Extract citations from fact-check response
            citations = self._extract_citations_new(fact_check_response)
            
            # Format the response
            formatted_response = self._format_response(fact_check_response.text)

            return {
                "response": formatted_response,
                "citations": citations
            }

        except Exception as e:
            raise Exception(f"Error during image fact-checking: {str(e)}")

    def _extract_citations_new(self, response) -> List[Dict]:
        """
        Extract citations from google-genai response with grounding metadata

        Args:
            response: Gemini API response from google-genai

        Returns:
            List of citation dictionaries
        """
        citations = []

        try:
            # Check for grounding metadata in the new SDK format
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                        grounding = candidate.grounding_metadata
                        
                        # Extract search entry point if available
                        if hasattr(grounding, 'search_entry_point'):
                            search_entry = grounding.search_entry_point
                            if hasattr(search_entry, 'rendered_content'):
                                # This contains the search results used
                                pass
                        
                        # Extract grounding supports (the actual sources)
                        if hasattr(grounding, 'grounding_supports'):
                            for support in grounding.grounding_supports:
                                if hasattr(support, 'segment'):
                                    segment = support.segment
                                    
                                    # Get the grounding chunk index
                                    if hasattr(support, 'grounding_chunk_indices'):
                                        for idx in support.grounding_chunk_indices:
                                            if hasattr(grounding, 'grounding_chunks') and idx < len(grounding.grounding_chunks):
                                                chunk = grounding.grounding_chunks[idx]
                                                
                                                if hasattr(chunk, 'web') and chunk.web:
                                                    citation = {
                                                        "title": getattr(chunk.web, 'title', 'Source'),
                                                        "url": getattr(chunk.web, 'uri', ''),
                                                        "snippet": ''
                                                    }
                                                    if citation not in citations:
                                                        citations.append(citation)

            # Fallback: extract URLs from text if no grounding metadata
            if not citations:
                citations = self._extract_urls_from_text(response.text)

        except Exception as e:
            print(f"Error extracting citations: {e}")
            citations = self._extract_urls_from_text(response.text)

        return citations
    
    def _format_response(self, text: str) -> str:
        """
        Format the response text to remove bullets, stars, and ensure proper sentence flow

        Args:
            text: Raw response text

        Returns:
            Formatted text
        """
        # Remove markdown formatting
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Remove bold
        text = re.sub(r'\*(.+?)\*', r'\1', text)  # Remove italic
        text = re.sub(r'^[\*\-\•]\s+', '', text, flags=re.MULTILINE)  # Remove bullet points
        text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)  # Remove numbered lists
        
        # Clean up extra whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)  # Max 2 newlines
        text = text.strip()
        
        return text

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
        if not self.client:
            raise Exception("Gemini API not initialized. Please check GEMINI_API_KEY.")

        prompt = f"Summarize the following text in {max_words} words or less:\n\n{text}"

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")
