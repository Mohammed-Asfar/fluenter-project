import os
import logging
from typing import Tuple, List
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import json

logger = logging.getLogger(__name__)


class GeminiClient:
    def __init__(self):
        """Initialize Gemini client with Vertex AI."""
        try:
            # Get credentials from environment
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
            location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
            
            # Initialize Vertex AI
            vertexai.init(project=project_id, location=location)
            
            # Initialize the model
            self.model = GenerativeModel("gemini-1.5-flash")
            
            logger.info(f"Gemini client initialized with project: {project_id}")
        
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {str(e)}")
            logger.warning("Falling back to mock mode")
            self.model = None
    
    async def correct_grammar(self, text: str, context: str = "") -> Tuple[str, List[str]]:
        """
        Correct grammar and return corrected text with suggestions.
        
        Args:
            text: The text to correct
            context: Additional context about the text
        
        Returns:
            Tuple of (corrected_text, list_of_suggestions)
        """
        try:
            if self.model is None:
                # Mock mode for testing without API
                return self._mock_correction(text)
            
            prompt = f"""You are a grammar correction assistant. Analyze the following text and correct any grammar, spelling, or punctuation errors.

Text to correct: "{text}"

Provide your response in the following JSON format:
{{
    "corrected": "the corrected text here",
    "suggestions": ["suggestion 1", "suggestion 2"]
}}

If the text has no errors, return it unchanged. Suggestions should explain what was fixed."""

            generation_config = GenerationConfig(
                temperature=0.3,
                max_output_tokens=1024,
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Parse the response
            result_text = response.text.strip()
            
            # Try to extract JSON from response
            try:
                # Remove markdown code blocks if present
                if result_text.startswith("```json"):
                    result_text = result_text.split("```json")[1].split("```")[0].strip()
                elif result_text.startswith("```"):
                    result_text = result_text.split("```")[1].split("```")[0].strip()
                
                result = json.loads(result_text)
                corrected = result.get("corrected", text)
                suggestions = result.get("suggestions", [])
            except json.JSONDecodeError:
                # If JSON parsing fails, use the raw response
                logger.warning("Failed to parse JSON response, using raw text")
                corrected = result_text
                suggestions = []
            
            return corrected, suggestions
        
        except Exception as e:
            logger.error(f"Error in grammar correction: {str(e)}")
            return text, [f"Error: {str(e)}"]
    
    async def rephrase_text(self, text: str) -> List[str]:
        """
        Rephrase text for better clarity and style.
        
        Args:
            text: The text to rephrase
        
        Returns:
            List of rephrased alternatives
        """
        try:
            if self.model is None:
                return self._mock_rephrase(text)
            
            prompt = f"""Rephrase the following text in 3 different ways to improve clarity, tone, or formality. Make each version distinct.

Text: "{text}"

Provide your response in JSON format:
{{
    "options": ["option 1", "option 2", "option 3"]
}}"""

            generation_config = GenerationConfig(
                temperature=0.7,
                max_output_tokens=1024,
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            result_text = response.text.strip()
            
            # Try to extract JSON
            try:
                if result_text.startswith("```json"):
                    result_text = result_text.split("```json")[1].split("```")[0].strip()
                elif result_text.startswith("```"):
                    result_text = result_text.split("```")[1].split("```")[0].strip()
                
                result = json.loads(result_text)
                options = result.get("options", [])
            except json.JSONDecodeError:
                options = [result_text]
            
            return options
        
        except Exception as e:
            logger.error(f"Error in rephrasing: {str(e)}")
            return [f"Error: {str(e)}"]
    
    def _mock_correction(self, text: str) -> Tuple[str, List[str]]:
        """Mock correction for testing without API."""
        # Simple mock logic
        corrections = {
            "i has": "I have",
            "she go": "she goes",
            "everydays": "every day",
            "a apple": "an apple"
        }
        
        corrected = text
        suggestions = []
        
        for wrong, right in corrections.items():
            if wrong in text.lower():
                corrected = corrected.replace(wrong, right)
                suggestions.append(f"Changed '{wrong}' to '{right}'")
        
        # Capitalize first letter
        if corrected and corrected[0].islower():
            corrected = corrected[0].upper() + corrected[1:]
            suggestions.append("Capitalized first letter")
        
        return corrected, suggestions
    
    def _mock_rephrase(self, text: str) -> List[str]:
        """Mock rephrasing for testing."""
        return [
            f"Rephrased: {text}",
            f"Alternative: {text}",
            f"Improved: {text}"
        ]
