import pytest
from datetime import datetime, timedelta
from ..ai_agents.behavior_agent import UserAction, ActionType
from .matching_engine import MatchingEngine, UserProfile, MatchResult

@pytest.mark.asyncio
async def test_matching_engine():
    # Initialize engine
    engine = MatchingEngine(use_mock=True)
    
    # Create test profiles
    base_time = datetime.now()
    
    profile1 = UserProfile(
        user_id="user1",
        text_content="I love programming in Python and working on AI projects",
        actions=[
            UserAction(
                action_type=ActionType.POST,
                timestamp=base_time + timedelta(hours=i),
                target_id=f"post_{i}",
                metadata={"topic": "tech"}
            )
            for i in range(3)
        ]
    )
    
    profile2 = UserProfile(
        user_id="user2",
        text_content="Python programming and artificial intelligence are my passion",
        actions=[
            UserAction(
                action_type=ActionType.POST,
                timestamp=base_time + timedelta(hours=i),
                target_id=f"post_{i}",
                metadata={"topic": "tech"}
            )
            for i in range(2)
        ]
    )
    
    profile3 = UserProfile(
        user_id="user3",
        text_content="I enjoy cooking and trying new recipes",
        actions=[
            UserAction(
                action_type=ActionType.POST,
                timestamp=base_time + timedelta(hours=i),
                target_id=f"post_{i}",
                metadata={"topic": "cooking"}
            )
            for i in range(2)
        ]
    )
    
    # Find matches for profile1
    matches = await engine.find_matches(
        profile1,
        [profile1, profile2, profile3]
    )
    
    # Check results
    assert isinstance(matches, list)
    assert all(isinstance(match, MatchResult) for match in matches)
    assert len(matches) > 0
    
    # Profile2 should be more similar to Profile1 than Profile3
    profile2_score = next(m.similarity_score for m in matches if m.user_id == "user2")
    profile3_score = next(m.similarity_score for m in matches if m.user_id == "user3")
    assert profile2_score > profile3_score
    
    print("\nMatching Results:")
    for match in matches:
        print(f"\nMatch for {match.user_id}:")
        print(f"Total Similarity: {match.similarity_score:.2f}")
        print("Similarity Breakdown:")
        for reason, score in match.match_reasons.items():
            print(f"- {reason}: {score:.2f}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 