from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from debateforge.argumentation.argument import Argument
from debateforge.config.settings import settings


JUDGE_SYSTEM_PROMPT = """You are a neutral judge evaluating the validity of arguments in a financial debate.

Your job is to determine if an attack on an argument is logically valid.
Consider:
- Is the attack relevant to the original claim?
- Does the attack use sound reasoning?
- Is the attack based on facts, not just opinions?

Respond with only 'VALID' or 'INVALID' followed by a brief one-sentence explanation."""


class JudgeAgent:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.llm_model,
            max_tokens=settings.max_tokens,
        )

    def invoke_with_retry(self, messages, retries: int = 3, wait: int = 10):
        import time
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

    def validate_attack(self, attacker: Argument, target: Argument, attack_reason: str) -> tuple[bool, str]:
        messages = [
            SystemMessage(content=JUDGE_SYSTEM_PROMPT),
            HumanMessage(content=f"""Original argument: {target.claim}

Attack by {attacker.agent_id}: {attack_reason}

Is this attack logically valid?""")
        ]
        response = self.invoke_with_retry(messages)
        content = response.content.strip()

        is_valid = content.upper().startswith("VALID")
        return is_valid, content