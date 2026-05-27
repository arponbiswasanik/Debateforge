from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from debateforge.agents import BullAgent, BearAgent, DevilAgent, JudgeAgent
from debateforge.argumentation import Argument, AttackGraph, ExtensionSolver
from debateforge.retrieval.retriever import FinancialRetriever
from debateforge.config.settings import settings


class DebateEngine:
    def __init__(self):
        self.agents = [BullAgent(), BearAgent(), DevilAgent()]
        self.judge = JudgeAgent()
        self.retriever = FinancialRetriever()
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.llm_model,
            max_tokens=settings.max_tokens,
        )

    def debate(self, question: str, ticker: str = "") -> dict:
        #load financial context if ticker provided
        context = ""
        if not ticker:
            ticker = self._detect_ticker(question)
        if ticker:
            context = self.retriever.load_ticker(ticker)

        graph = AttackGraph()

        #each agent generates initial argument
        arguments = {}
        for agent in self.agents:
            arg = agent.generate_argument(question, context)
            arguments[agent.agent_id] = arg
            graph.add_argument(arg)

        #debate rounds
        for round_num in range(settings.max_debate_rounds):
            for attacker in self.agents:
                for defender in self.agents:
                    if attacker.agent_id == defender.agent_id:
                        continue

                    target_arg = arguments[defender.agent_id]
                    is_attack, reason = attacker.try_attack(target_arg, context)

                    if not is_attack:
                        continue

                    attacker_arg = arguments[attacker.agent_id]
                    is_valid, judge_note = self.judge.validate_attack(
                        attacker_arg, target_arg, reason
                    )

                    if not is_valid:
                        continue

                    graph.add_attack(attacker_arg, target_arg, reason)

                    # defender rebuts
                    rebuttal = defender.rebut(reason, target_arg, context)
                    arguments[defender.agent_id] = rebuttal
                    graph.add_argument(rebuttal)

        #compute winner
        solver = ExtensionSolver(graph)
        grounded = solver.grounded()
        preferred = solver.preferred()
        winner = self._pick_winner(grounded, arguments)

        conclusion = self._generate_conclusion(
            question=question,
            arguments=arguments,
            graph=graph,
            winner=winner,
        )

        return {
            "question": question,
            "ticker": ticker,
            "context": context,
            "arguments": arguments,
            "grounded": grounded,
            "preferred": preferred,
            "graph": graph,
            "winner": winner,
            "conclusion": conclusion,
        }

    def _pick_winner(self, grounded: set, arguments: dict) -> str:
        winning_agents = [
            agent_id for agent_id, arg in arguments.items()
            if arg in grounded
        ]

        if not winning_agents:
            return "No consensus reached."

        if len(winning_agents) == 1:
            return f"{winning_agents[0].upper()} wins the debate."

        return f"Consensus between: {', '.join(winning_agents)}"

    def _generate_conclusion(self, question: str, arguments: dict, graph: AttackGraph, winner: str) -> str:
        debate_summary = "\n".join([
            f"[{agent_id.upper()}]: {arg.claim}"
            for agent_id, arg in arguments.items()
        ])

        attacks_summary = "\n".join([
            f"{a.attacker.agent_id.upper()} → {a.target.agent_id.upper()}: {a.reason}"
            for a in graph.attacks
        ])

        messages = [
            SystemMessage(content="""You are an expert analyst summarizing a structured debate.
Based on the question type and debate content, choose the most appropriate verdict format.

For investment questions: use BUY / SELL / HOLD
For yes/no questions: use YES / NO / UNCERTAIN
For comparison questions: use OPTION A / OPTION B / BOTH
For policy/strategy questions: use RECOMMENDED / NOT RECOMMENDED / CONDITIONAL
For any other questions: choose a single clear 1-3 word verdict that fits best

Format your response exactly as:
VERDICT: [your chosen verdict]
REASONING: [2-3 sentences explaining the verdict based on the debate]
KEY RISK: [1 sentence on the main caveat or risk to keep in mind]"""),
            HumanMessage(content=f"""Question: {question}

Arguments:
{debate_summary}

Attacks:
{attacks_summary}

Winner: {winner}

Provide your final recommendation.""")
        ]

        response = self.llm.invoke(messages)
        return response.content
    

    def _detect_ticker(self, question: str) -> str:
        messages = [
            SystemMessage(content="""You are a financial data assistant. 
    Extract the stock ticker symbol from the given question.
    If a company is mentioned, return only its ticker symbol (e.g. AAPL, GOOGL, MSFT).
    If no specific publicly traded company is mentioned, return NONE.
    Return only the ticker symbol, nothing else."""),
            HumanMessage(content=question)
        ]
        response = self.llm.invoke(messages)
        ticker = response.content.strip().upper()
        return "" if ticker == "NONE" else ticker 