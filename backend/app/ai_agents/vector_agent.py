from typing import List
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from huggingface_hub import snapshot_download

class VectorResult(BaseModel):
    vector: List[float]
    dimension: int
    text: str

class VectorAgent:
    def __init__(self, use_mock: bool = True):
        """Initialize vector agent."""
        self.use_mock = use_mock
        if not use_mock:
            # Використовуємо новий метод завантаження моделі
            model_path = snapshot_download(
                repo_id="sentence-transformers/all-MiniLM-L6-v2",
                cache_dir=".model_cache"
            )
            self.model = SentenceTransformer(model_path)
    
    def _mock_vectorize(self, text: str) -> VectorResult:
        """Mock vectorization for testing."""
        # Return mock 384-dimensional vector (same dimension as MiniLM-L6-v2)
        mock_vector = [0.1] * 384
        
        return VectorResult(
            vector=mock_vector,
            dimension=384,
            text=text
        )
    
    async def vectorize(self, text: str) -> VectorResult:
        """Convert text to vector representation."""
        if self.use_mock:
            return self._mock_vectorize(text)
        else:
            # Real vectorization
            embeddings = self.model.encode([text])[0]
            return VectorResult(
                vector=embeddings.tolist(),
                dimension=len(embeddings),
                text=text
            )
    
    async def batch_vectorize(self, texts: List[str]) -> List[VectorResult]:
        """Vectorize multiple texts."""
        results = []
        for text in texts:
            result = await self.vectorize(text)
            results.append(result)
        return results
