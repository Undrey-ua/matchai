from typing import List, Dict, Optional
from pydantic import BaseModel
from ..ai_agents.text_agent import TextAgent, TextAnalysisResult
from ..ai_agents.vector_agent import VectorAgent, VectorResult
from ..ai_agents.behavior_agent import BehaviorAgent, BehaviorPattern, UserAction
import numpy as np

class UserProfile(BaseModel):
    user_id: str
    text_content: str
    actions: List[UserAction]
    
class MatchResult(BaseModel):
    user_id: str
    similarity_score: float
    match_reasons: Dict[str, float]

class MatchingEngine:
    def __init__(
        self,
        text_agent: Optional[TextAgent] = None,
        vector_agent: Optional[VectorAgent] = None,
        behavior_agent: Optional[BehaviorAgent] = None,
        use_mock: bool = True
    ):
        """Initialize matching engine with AI agents."""
        self.text_agent = text_agent or TextAgent(use_mock=use_mock)
        self.vector_agent = vector_agent or VectorAgent(use_mock=use_mock)
        self.behavior_agent = behavior_agent or BehaviorAgent(use_mock=use_mock)
        
    async def _analyze_profile(self, profile: UserProfile) -> Dict[str, any]:
        """Analyze user profile using all agents."""
        # Get text analysis
        text_analysis = await self.text_agent.analyze_content(profile.text_content)
        
        # Get vector representation
        vector_result = await self.vector_agent.vectorize(profile.text_content)
        
        # Get behavior analysis
        behavior_pattern = await self.behavior_agent.analyze_behavior(profile.actions)
        
        return {
            "text_analysis": text_analysis,
            "vector_result": vector_result,
            "behavior_pattern": behavior_pattern
        }
    
    def _calculate_text_similarity(
        self,
        analysis1: TextAnalysisResult,
        analysis2: TextAnalysisResult
    ) -> float:
        """Calculate similarity based on text analysis."""
        # Compare topics
        common_topics = set(analysis1.topics) & set(analysis2.topics)
        topic_similarity = len(common_topics) / max(
            len(analysis1.topics), len(analysis2.topics), 1
        )
        
        # Compare sentiment
        sentiment_similarity = 1.0 if analysis1.sentiment == analysis2.sentiment else 0.0
        
        return 0.7 * topic_similarity + 0.3 * sentiment_similarity
    
    def _calculate_vector_similarity(
        self,
        vector1: VectorResult,
        vector2: VectorResult
    ) -> float:
        """Calculate cosine similarity between vectors."""
        v1 = np.array(vector1.vector)
        v2 = np.array(vector2.vector)
        
        dot_product = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        
        return dot_product / (norm1 * norm2)
    
    def _calculate_behavior_similarity(
        self,
        pattern1: BehaviorPattern,
        pattern2: BehaviorPattern
    ) -> float:
        """Calculate similarity based on behavior patterns."""
        # Compare activity levels
        activity_diff = abs(pattern1.activity_level - pattern2.activity_level)
        activity_similarity = 1.0 - activity_diff
        
        # Compare peak hours
        common_hours = set(pattern1.peak_hours) & set(pattern2.peak_hours)
        hour_similarity = len(common_hours) / max(
            len(pattern1.peak_hours), len(pattern2.peak_hours), 1
        )
        
        # Compare preferred actions
        common_actions = set(pattern1.preferred_actions) & set(pattern2.preferred_actions)
        action_similarity = len(common_actions) / max(
            len(pattern1.preferred_actions), len(pattern2.preferred_actions), 1
        )
        
        return (activity_similarity + hour_similarity + action_similarity) / 3
    
    async def find_matches(
        self,
        target_profile: UserProfile,
        candidate_profiles: List[UserProfile],
        min_similarity: float = 0.5
    ) -> List[MatchResult]:
        """Find matching profiles based on combined similarity."""
        # Analyze target profile
        target_analysis = await self._analyze_profile(target_profile)
        
        matches = []
        for candidate in candidate_profiles:
            if candidate.user_id == target_profile.user_id:
                continue
                
            # Analyze candidate profile
            candidate_analysis = await self._analyze_profile(candidate)
            
            # Calculate similarities
            text_sim = self._calculate_text_similarity(
                target_analysis["text_analysis"],
                candidate_analysis["text_analysis"]
            )
            
            vector_sim = self._calculate_vector_similarity(
                target_analysis["vector_result"],
                candidate_analysis["vector_result"]
            )
            
            behavior_sim = self._calculate_behavior_similarity(
                target_analysis["behavior_pattern"],
                candidate_analysis["behavior_pattern"]
            )
            
            # Calculate weighted similarity
            total_similarity = (
                0.3 * text_sim +
                0.4 * vector_sim +
                0.3 * behavior_sim
            )
            
            if total_similarity >= min_similarity:
                matches.append(MatchResult(
                    user_id=candidate.user_id,
                    similarity_score=total_similarity,
                    match_reasons={
                        "text_similarity": text_sim,
                        "vector_similarity": vector_sim,
                        "behavior_similarity": behavior_sim
                    }
                ))
        
        # Sort by similarity score
        matches.sort(key=lambda x: x.similarity_score, reverse=True)
        return matches 