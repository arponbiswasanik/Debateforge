from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from debateforge.core.base_agent import BaseAgent
from debateforge.argumentation.argument import Argument
from debateforge.config.settings import settings


DEVIL_SYSTEM_PROMPT = """You are a devil's advocate analyst. Your job is to challenge 
ALL assumptions and arguments regardless of which side they come from.

When generating arguments, focus on:
- Uncertainty and unknowable risks
- Conflicting data interpretations
- Assumptions that may not hold
- Black swan scenarios being ignored

When attacking arguments, look for:
- Overconfidence in either direction
- False certainty in uncertain markets
- Logical fallacies or cognitive biases

You are not bullish or bearish — you are skeptical of everyone.
Respond concisely in 2-3 sentences."""


class DevilAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_id="devil", stance="skeptical")
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.llm_model,
            max_tokens=settings.max_tokens,
        )

    def generate_argument(self, question: str, context: str = "") -> Argument:
        messages = [
            SystemMessage(content=DEVIL_SYSTEM_PROMPT),
            HumanMessage(content=f"Question: {question}\nContext: {context}\n\nChallenge the core assumptions.")
        ]
        response = self.invoke_with_retry(messages)

        return Argument(
            claim=response.content,
            evidence=context,
            agent_id=self.agent_id,
            strength=0.75,
        )

    def try_attack(self, argument: Argument, context: str = "") -> tuple[bool, str]:
        messages = [
            SystemMessage(content=DEVIL_SYSTEM_PROMPT),
            HumanMessage(content=f"""Challenge this argument by finding its weakest assumption:
Argument: {argument.claim}

If you can challenge it, start with 'ATTACK:' and explain in 1-2 sentences.
If the argument is solid, start with 'PASS:'.""")
        ]
        response = self.invoke_with_retry(messages)
        content = response.content

        if content.startswith("ATTACK:"):
            return True, content.replace("ATTACK:", "").strip()
        return False, ""

    def rebut(self, attack_reason: str, original: Argument, context: str = "") -> Argument:
        messages = [
            SystemMessage(content=DEVIL_SYSTEM_PROMPT),
            HumanMessage(content=f"""Your argument was challenged:
Original claim: {original.claim}
Challenge: {attack_reason}

Defend your skeptical position in 2-3 sentences.""")
        ]
        response = self.invoke_with_retry(messages)

        return Argument(
            claim=response.content,
            evidence=original.evidence,
            agent_id=self.agent_id,
            strength=min(original.strength + 0.1, 1.0),
        )