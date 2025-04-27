import pytest
from datetime import datetime, timedelta
from .behavior_agent import BehaviorAgent, UserAction, ActionType, BehaviorPattern

@pytest.mark.asyncio
async def test_mock_behavior_agent():
    # Initialize agent
    agent = BehaviorAgent(use_mock=True)
    
    # Create test actions
    base_time = datetime.now()
    test_actions = [
        UserAction(
            action_type=ActionType.POST,
            timestamp=base_time + timedelta(hours=i),
            target_id=f"post_{i}",
            metadata={"topic": "tech"}
        )
        for i in range(5)
    ]
    
    # Add some likes
    test_actions.extend([
        UserAction(
            action_type=ActionType.LIKE,
            timestamp=base_time + timedelta(hours=i),
            target_id=f"like_{i}",
            metadata={"topic": "tech"}
        )
        for i in range(3)
    ])
    
    # Get behavior analysis
    result = await agent.analyze_behavior(test_actions)
    
    # Check result structure
    assert isinstance(result, BehaviorPattern)
    assert 0 <= result.activity_level <= 1.0
    assert isinstance(result.peak_hours, list)
    assert all(0 <= hour <= 23 for hour in result.peak_hours)
    assert isinstance(result.preferred_actions, list)
    assert isinstance(result.interests, dict)
    
    # Check empty input
    empty_result = await agent.analyze_behavior([])
    assert isinstance(empty_result, BehaviorPattern)
    assert empty_result.activity_level == 0.0
    
    print("\nBehavior Analysis Results:")
    print(f"Activity Level: {result.activity_level}")
    print(f"Peak Hours: {result.peak_hours}")
    print(f"Preferred Actions: {result.preferred_actions}")
    print(f"Interests: {result.interests}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 