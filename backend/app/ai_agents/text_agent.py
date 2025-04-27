from typing import List, Dict
from pydantic import BaseModel
import json

class Theme(BaseModel):
    name: str
    confidence: float

class TextAnalysisResult(BaseModel):
    topics: List[str]
    sentiment: str
    themes: List[Theme]
    language: str

class TextAgent:
    def __init__(self, api_key: str = None, use_mock: bool = True):
        """Initialize text analysis agent.
        
        Args:
            api_key: OpenAI API key (not used in mock mode)
            use_mock: If True, use mock responses instead of real API
        """
        self.use_mock = use_mock
        if not use_mock and api_key:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=api_key)
    
    def _mock_analyze(self, text: str) -> TextAnalysisResult:
        """Mock analysis based on text content."""
        # Simple keyword-based analysis
        text = text.lower()
        
        # Mock topics based on keywords
        topics = []
        if "python" in text: topics.append("programming")
        if "ai" in text or "artificial intelligence" in text: topics.append("AI")
        if "learn" in text: topics.append("education")
        if not topics: topics = ["general"]
            
        # Mock sentiment based on positive/negative words
        positive_words = ["love", "great", "good", "excellent", "amazing"]
        negative_words = ["hate", "bad", "terrible", "awful", "poor"]
        
        sentiment = "neutral"
        for word in positive_words:
            if word in text:
                sentiment = "positive"
                break
        for word in negative_words:
            if word in text:
                sentiment = "negative"
                break
                
        # Mock themes with confidence scores
        themes = [
            Theme(name=topic, confidence=0.8)
            for topic in topics
        ]
        
        # Detect language (simple mock - always English)
        language = "en"
        
        return TextAnalysisResult(
            topics=topics,
            sentiment=sentiment,
            themes=themes,
            language=language
        )
    
    async def analyze_content(self, text: str) -> TextAnalysisResult:
        """Analyze text content."""
        if self.use_mock:
            return self._mock_analyze(text)
        else:
            # Real API call (to be implemented)
            raise NotImplementedError("Real API analysis not implemented yet")
    
    async def batch_analyze(self, texts: List[str]) -> List[TextAnalysisResult]:
        """Analyze multiple texts."""
        results = []
        for text in texts:
            result = await self.analyze_content(text)
            results.append(result)
        return results
