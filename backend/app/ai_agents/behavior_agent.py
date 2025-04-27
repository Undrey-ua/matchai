from typing import List, Dict
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class ActionType(str, Enum):
    POST = "post"
    LIKE = "like"
    COMMENT = "comment"
    SHARE = "share"
    VIEW = "view"

class UserAction(BaseModel):
    action_type: ActionType
    timestamp: datetime
    target_id: str
    metadata: Dict[str, str] = {}

class BehaviorPattern(BaseModel):
    activity_level: float  # 0.0 to 1.0
    peak_hours: List[int]  # 0-23 hours
    preferred_actions: List[ActionType]
    interests: Dict[str, float]  # topic: weight

class BehaviorAgent:
    def __init__(self, use_mock: bool = True):
        """Initialize behavior analysis agent."""
        self.use_mock = use_mock
    
    def _mock_analyze(self, actions: List[UserAction]) -> BehaviorPattern:
        """Mock behavior analysis."""
        if not actions:
            return BehaviorPattern(
                activity_level=0.0,
                peak_hours=[12, 18],  # Default peak hours
                preferred_actions=[ActionType.VIEW],
                interests={"general": 1.0}
            )
            
        # Count actions by type
        action_counts = {}
        for action in actions:
            action_counts[action.action_type] = action_counts.get(action.action_type, 0) + 1
            
        # Get most frequent actions
        total_actions = sum(action_counts.values())
        preferred_actions = [
            action_type for action_type, count in action_counts.items()
            if count > total_actions * 0.2  # 20% threshold
        ]
        
        # Mock activity level based on action count
        activity_level = min(1.0, len(actions) / 100)  # 100 actions = max activity
        
        # Get hours with most activity
        hours = [action.timestamp.hour for action in actions]
        hour_counts = {}
        for hour in hours:
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
            
        peak_hours = sorted(
            hour_counts.keys(),
            key=lambda h: hour_counts[h],
            reverse=True
        )[:3]  # Top 3 active hours
        
        return BehaviorPattern(
            activity_level=activity_level,
            peak_hours=peak_hours,
            preferred_actions=preferred_actions or [ActionType.VIEW],
            interests={"general": 1.0}  # Mock interests
        )
    
    async def analyze_behavior(self, actions: List[UserAction]) -> BehaviorPattern:
        """Analyze user behavior patterns."""
        if self.use_mock:
            return self._mock_analyze(actions)
        else:
            # Real behavior analysis (to be implemented)
            raise NotImplementedError("Real behavior analysis not implemented yet")
