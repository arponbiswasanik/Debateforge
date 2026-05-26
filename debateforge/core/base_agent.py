from abc import ABC, abstractmethod
from debateforge.argumentation.argument import Argument


class BaseAgent(ABC):
    def __init__(self, agent_id: str, stance: str):
        self.agent_id = agent_id
        self.stance = stance

    @abstractmethod
    def generate_argument(self, question: str, context: str = "") -> Argument:
        pass

    @abstractmethod
    def try_attack(self, argument: Argument, context: str = "") -> tuple[bool, str]:
        # returns (is_valid_attack, reason)
        pass

    @abstractmethod
    def rebut(self, attack_reason: str, original: Argument, context: str = "") -> Argument:
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(stance={self.stance})"
    
    