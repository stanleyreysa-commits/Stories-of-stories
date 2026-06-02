"""
Node Engine - Handles story nodes and narrative flow.
A node represents a moment in the story where the player can make choices.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class Node:
    """Represents a story node."""
    id: int
    title: str
    content: str
    choices: List['Choice'] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.choices is None:
            self.choices = []
        if self.metadata is None:
            self.metadata = {}
    
    def add_choice(self, choice: 'Choice') -> None:
        """Add a choice to this node."""
        self.choices.append(choice)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'choices': [c.to_dict() for c in self.choices],
            'metadata': self.metadata
        }


@dataclass
class Choice:
    """Represents a player choice within a node."""
    id: int
    text: str
    next_node_id: int
    consequence: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert choice to dictionary."""
        return {
            'id': self.id,
            'text': self.text,
            'next_node_id': self.next_node_id,
            'consequence': self.consequence
        }


class NodeEngine:
    """Engine for managing story nodes and navigation."""
    
    def __init__(self):
        self.nodes: Dict[int, Node] = {}
        self.current_node_id: Optional[int] = None
    
    def create_node(self, node_id: int, title: str, content: str) -> Node:
        """Create a new story node."""
        node = Node(id=node_id, title=title, content=content)
        self.nodes[node_id] = node
        return node
    
    def get_node(self, node_id: int) -> Optional[Node]:
        """Retrieve a node by ID."""
        return self.nodes.get(node_id)
    
    def set_current_node(self, node_id: int) -> bool:
        """Set the current active node."""
        if node_id in self.nodes:
            self.current_node_id = node_id
            return True
        return False
    
    def get_current_node(self) -> Optional[Node]:
        """Get the current active node."""
        if self.current_node_id is not None:
            return self.get_node(self.current_node_id)
        return None
    
    def navigate(self, choice_id: int) -> Optional[Node]:
        """
        Navigate to the next node based on a choice.
        Returns the new node or None if navigation failed.
        """
        current = self.get_current_node()
        if current is None:
            return None
        
        # Find the choice
        choice = next((c for c in current.choices if c.id == choice_id), None)
        if choice is None:
            return None
        
        # Navigate to next node
        if self.set_current_node(choice.next_node_id):
            return self.get_current_node()
        return None
    
    def all_nodes(self) -> List[Node]:
        """Get all nodes."""
        return list(self.nodes.values())
