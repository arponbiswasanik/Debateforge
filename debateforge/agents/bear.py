from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from debateforge.core.base_agent import BaseAgent
from debateforge.argumentation.argument import Argument
from debateforge.config.settings import settings


BEAR_SYSTEM_PROMPT = """You are a bearish financial analyst. Your job is to find and argue 
the strongest case AGAINST investing in a given asset or company.

When generating arguments, focus on:
- Overvaluation and stretched multiples
- Declining margins or revenue quality
- Competitive threats and market headwinds
- Regulatory risks and macroeconomic concerns

When attacking opposing arguments, look for:
- Cherry-picked metrics or survivorship bias
- Unsustainable growth assumptions
- Hidden risks being ignored

Always be specific, cite numbers when possible, and stay grounded in facts.
Respond concisely in 2-3 sentences."""


class BearAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_id="bear", stance="pessimistic")
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.llm_model,
            max_tokens=settings.max_tokens,
        )

    def generate_argument(self, question: str, context: str = "") -> Argument:
        messages = [
            SystemMessage(content=BEAR_SYSTEM_PROMPT),
            HumanMessage(content=f"Question: {question}\nContext: {context}\n\nMake your bearish argument.")
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
            SystemMessage(content=BEAR_SYSTEM_PROMPT),
            HumanMessage(content=f"""Can you find a flaw in this bullish argument?
Argument: {argument.claim}

If yes, explain the flaw in 1-2 sentences and start with 'ATTACK:'.
If no valid attack exists, start with 'PASS:'.""")
        ]
        response = self.invoke_with_retry(messages)
        content = response.content

        if content.startswith("ATTACK:"):
            return True, content.replace("ATTACK:", "").strip()
        return False, ""

    def rebut(self, attack_reason: str, original: Argument, context: str = "") -> Argument:
        messages = [
            SystemMessage(content=BEAR_SYSTEM_PROMPT),
            HumanMessage(content=f"""Your argument was attacked:
Original claim: {original.claim}
Attack: {attack_reason}

Rebut this attack and strengthen your position in 2-3 sentences.""")
        ]
        response = self.invoke_with_retry(messages)

        return Argument(
            claim=response.content,
            evidence=original.evidence,
            agent_id=self.agent_id,
            strength=min(original.strength + 0.1, 1.0),
        )