"""
World Engine - Manages the game world state, characters, and environmental context.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from enum import Enum


class WorldState(Enum):
    """Possible world states."""
    PEACEFUL = "peaceful"
    CONFLICT = "conflict"
    DISCOVERY = "discovery"
    CRISIS = "crisis"


@dataclass
class Character:
    """Represents a character in the world."""
    id: int
    name: str
    role: str
    state: str = "active"
    relationships: Dict[int, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'state': self.state,
            'relationships': self.relationships,
            'metadata': self.metadata
        }


@dataclass
class Location:
    """Represents a location in the world."""
    id: int
    name: str
    description: str
    exits: Dict[str, int] = field(default_factory=dict)  # direction -> location_id
    npcs: List[int] = field(default_factory=list)
    items: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'exits': self.exits,
            'npcs': self.npcs,
            'items': self.items,
            'metadata': self.metadata
        }


class World:
    """Manages the game world."""
    
    def __init__(self, name: str):
        self.name = name
        self.state = WorldState.PEACEFUL
        self.characters: Dict[int, Character] = {}
        self.locations: Dict[int, Location] = {}
        self.global_state: Dict[str, Any] = {}
    
    def add_character(self, character: Character) -> None:
        """Add a character to the world."""
        self.characters[character.id] = character
    
    def get_character(self, character_id: int) -> Character | None:
        """Get a character by ID."""
        return self.characters.get(character_id)
    
    def add_location(self, location: Location) -> None:
        """Add a location to the world."""
        self.locations[location.id] = location
    
    def get_location(self, location_id: int) -> Location | None:
        """Get a location by ID."""
        return self.locations.get(location_id)
    
    def set_world_state(self, state: WorldState) -> None:
        """Change the state of the world."""
        self.state = state
    
    def update_global_state(self, key: str, value: Any) -> None:
        """Update a global world state variable."""
        self.global_state[key] = value
    
    def get_global_state(self, key: str, default: Any = None) -> Any:
        """Get a global world state variable."""
        return self.global_state.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert world state to dictionary."""
        return {
            'name': self.name,
            'state': self.state.value,
            'characters': {cid: c.to_dict() for cid, c in self.characters.items()},
            'locations': {lid: l.to_dict() for lid, l in self.locations.items()},
            'global_state': self.global_state
        }
