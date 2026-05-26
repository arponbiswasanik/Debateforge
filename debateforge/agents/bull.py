from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from debateforge.core.base_agent import BaseAgent
from debateforge.argumentation.argument import Argument
from debateforge.config.settings import settings


BULL_SYSTEM_PROMPT = """You are a bullish financial analyst. Your job is to find and argue 
the strongest case FOR investing in a given asset or company.

When generating arguments, focus on:
- Revenue growth and profitability trends
- Market position and competitive advantages
- Management quality and strategic vision
- Growth catalysts and future potential

When attacking opposing arguments, look for:
- Missing context or incomplete data
- Overly pessimistic assumptions
- Short-term thinking vs long-term value

Always be specific, cite numbers when possible, and stay grounded in facts.
Respond concisely in 2-3 sentences."""


class BullAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_id="bull", stance="optimistic")
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.llm_model,
            max_tokens=settings.max_tokens,
        )

    def generate_argument(self, question: str, context: str = "") -> Argument:
        messages = [
            SystemMessage(content=BULL_SYSTEM_PROMPT),
            HumanMessage(content=f"Question: {question}\nContext: {context}\n\nMake your bullish argument.")
        ]
        response = self.llm.invoke(messages)
        claim = response.content

        return Argument(
            claim=claim,
            evidence=context,
            agent_id=self.agent_id,
            strength=0.75,
        )

    def try_attack(self, argument: Argument, context: str = "") -> tuple[bool, str]:
        messages = [
            SystemMessage(content=BULL_SYSTEM_PROMPT),
            HumanMessage(content=f"""Can you find a flaw in this bearish argument?
Argument: {argument.claim}

If yes, explain the flaw in 1-2 sentences and start with 'ATTACK:'.
If no valid attack exists, start with 'PASS:'.""")
        ]
        response = self.llm.invoke(messages)
        content = response.content

        if content.startswith("ATTACK:"):
            return True, content.replace("ATTACK:", "").strip()
        return False, ""

    def rebut(self, attack_reason: str, original: Argument, context: str = "") -> Argument:
        messages = [
            SystemMessage(content=BULL_SYSTEM_PROMPT),
            HumanMessage(content=f"""Your argument was attacked:
Original claim: {original.claim}
Attack: {attack_reason}

Rebut this attack and strengthen your position in 2-3 sentences.""")
        ]
        response = self.llm.invoke(messages)

        return Argument(
            claim=response.content,
            evidence=original.evidence,
            agent_id=self.agent_id,
            strength=min(original.strength + 0.1, 1.0),
        )