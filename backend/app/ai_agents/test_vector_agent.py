import pytest
from .vector_agent import VectorAgent, VectorResult

@pytest.mark.asyncio
async def test_mock_vector_agent():
    # Initialize agent in mock mode
    agent = VectorAgent(use_mock=True)
    
    # Test text
    test_text = "This is a test sentence for vectorization"
    
    # Get vector
    result = await agent.vectorize(test_text)
    
    # Check result structure
    assert isinstance(result, VectorResult)
    assert isinstance(result.vector, list)
    assert len(result.vector) == 384  # Expected dimension
    assert result.dimension == 384
    assert result.text == test_text
    
    # Test batch processing
    texts = ["First text", "Second text", "Third text"]
    results = await agent.batch_vectorize(texts)
    
    assert len(results) == 3
    for res in results:
        assert isinstance(res, VectorResult)
        assert len(res.vector) == 384

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 