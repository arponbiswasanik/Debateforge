from dataclasses import dataclass, field
from typing import Optional
import uuid


@dataclass
class Argument:
    claim: str
    evidence: str
    agent_id: str
    argument_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    strength: float = 1.0  # 0.0 to 1.0
    metadata: dict = field(default_factory=dict)

    def __hash__(self):
        return hash(self.argument_id)

    def __eq__(self, other):
        if not isinstance(other, Argument):
            return False
        return self.argument_id == other.argument_id

    def __repr__(self):
        return f"Argument({self.agent_id}: {self.claim[:50]}...)"
    
    