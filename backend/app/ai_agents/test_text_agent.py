import pytest
from .text_agent import TextAgent, TextAnalysisResult
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@pytest.mark.asyncio
async def test_text_analysis():
    # Initialize agent
    api_key = os.getenv("OPENAI_API_KEY")
    agent = TextAgent(api_key)
    
    # Test text
    test_text = """
    I really love programming in Python! 
    The language is so elegant and powerful. 
    Recently, I've been working on AI projects 
    and learning about machine learning.
    """
    
    # Get analysis
    result = await agent.analyze_content(test_text)
    
    # Check result structure
    assert isinstance(result, TextAnalysisResult)
    assert isinstance(result.topics, list)
    assert isinstance(result.sentiment, str)
    assert isinstance(result.themes, list)
    assert isinstance(result.language, str)
    
    # Print results for manual verification
    print("\nAnalysis Results:")
    print(f"Topics: {result.topics}")
    print(f"Sentiment: {result.sentiment}")
    print(f"Themes: {result.themes}")
    print(f"Language: {result.language}")

@pytest.mark.asyncio
async def test_mock_text_analysis():
    # Initialize agent in mock mode
    agent = TextAgent(use_mock=True)
    
    # Test cases
    test_cases = [
        {
            "text": "I love programming in Python! It's amazing.",
            "expected_sentiment": "positive",
            "expected_topics": ["programming"]
        },
        {
            "text": "AI and machine learning are fascinating topics.",
            "expected_sentiment": "neutral",
            "expected_topics": ["AI"]
        },
        {
            "text": "This is terrible code, I hate it.",
            "expected_sentiment": "negative",
            "expected_topics": ["general"]
        }
    ]
    
    for case in test_cases:
        # Get analysis
        result = await agent.analyze_content(case["text"])
        
        # Check result structure
        assert isinstance(result, TextAnalysisResult)
        assert isinstance(result.topics, list)
        assert isinstance(result.sentiment, str)
        assert isinstance(result.themes, list)
        assert isinstance(result.language, str)
        
        # Check specific expectations
        assert result.sentiment == case["expected_sentiment"]
        assert any(topic in case["expected_topics"] for topic in result.topics)
        
        # Print results
        print(f"\nAnalysis for: {case['text']}")
        print(f"Topics: {result.topics}")
        print(f"Sentiment: {result.sentiment}")
        print(f"Themes: {result.themes}")
        print(f"Language: {result.language}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 