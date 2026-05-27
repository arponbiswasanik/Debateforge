import time
from abc import ABC, abstractmethod
from debateforge.argumentation.argument import Argument


class BaseAgent(ABC):
    def __init__(self, agent_id: str, stance: str):
        self.agent_id = agent_id
        self.stance = stance

    def invoke_with_retry(self, messages, retries: int = 3, wait: int = 10):
        for attempt in range(retries):
            try:
                return self.llm.invoke(messages)
            except Exception as e:
                if "429" in str(e) or "rate_limit" in str(e).lower():
                    if attempt < retries - 1:
                        time.sleep(wait)
                    else:
                        raise
                else:
                    raise

    @abstractmethod
    def generate_argument(self, question: str, context: str = "") -> Argument:
        pass

    @abstractmethod
    def try_attack(self, argument: Argument, context: str = "") -> tuple[bool, str]:
        pass

    @abstractmethod
    def rebut(self, attack_reason: str, original: Argument, context: str = "") -> Argument:
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(stance={self.stance})"