"""
Echo Engine - Handles narrative echoes, consequences, and story callbacks.
Reflects player choices back into the world state.
"""

from dataclasses import dataclass
from typing import Callable, Any, Dict, List
from enum import Enum


class EchoType(Enum):
    """Types of narrative echoes."""
    CHARACTER_REACTION = "character_reaction"
    WORLD_CHANGE = "world_change"
    STAT_CHANGE = "stat_change"
    TRIGGER_EVENT = "trigger_event"
    DIALOGUE = "dialogue"


@dataclass
class Echo:
    """Represents a narrative consequence/echo."""
    id: int
    echo_type: EchoType
    description: str
    affected_entity: str  # character name, location name, or stat name
    magnitude: int = 1  # intensity of the echo
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'echo_type': self.echo_type.value,
            'description': self.description,
            'affected_entity': self.affected_entity,
            'magnitude': self.magnitude,
            'metadata': self.metadata
        }


class EchoEngine:
    """Engine for managing narrative echoes and consequences."""
    
    def __init__(self):
        self.echoes: List[Echo] = []
        self.echo_history: List[Echo] = []
        self.callbacks: Dict[str, List[Callable]] = {}
    
    def create_echo(
        self,
        echo_id: int,
        echo_type: EchoType,
        description: str,
        affected_entity: str,
        magnitude: int = 1
    ) -> Echo:
        """Create a new echo."""
        echo = Echo(
            id=echo_id,
            echo_type=echo_type,
            description=description,
            affected_entity=affected_entity,
            magnitude=magnitude
        )
        self.echoes.append(echo)
        return echo
    
    def trigger_echo(self, echo_id: int) -> Echo | None:
        """Trigger an echo and record it in history."""
        echo = next((e for e in self.echoes if e.id == echo_id), None)
        if echo is None:
            return None
        
        self.echo_history.append(echo)
        
        # Call registered callbacks
        callback_key = echo.echo_type.value
        if callback_key in self.callbacks:
            for callback in self.callbacks[callback_key]:
                callback(echo)
        
        return echo
    
    def register_callback(self, echo_type: str, callback: Callable) -> None:
        """Register a callback for a specific echo type."""
        if echo_type not in self.callbacks:
            self.callbacks[echo_type] = []
        self.callbacks[echo_type].append(callback)
    
    def get_echo_history(self) -> List[Echo]:
        """Get the history of triggered echoes."""
        return self.echo_history.copy()
    
    def get_pending_echoes(self) -> List[Echo]:
        """Get echoes that haven't been triggered yet."""
        triggered_ids = {e.id for e in self.echo_history}
        return [e for e in self.echoes if e.id not in triggered_ids]
    
    def clear_history(self) -> None:
        """Clear the echo history."""
        self.echo_history.clear()
