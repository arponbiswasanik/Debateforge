from debateforge.agents import BullAgent, BearAgent, DevilAgent, JudgeAgent
from debateforge.argumentation import Argument, AttackGraph, ExtensionSolver
from debateforge.retrieval.retriever import FinancialRetriever
from debateforge.config.settings import settings


class DebateEngine:
    def __init__(self):
        self.agents = [BullAgent(), BearAgent(), DevilAgent()]
        self.judge = JudgeAgent()
        self.retriever = FinancialRetriever()

    def debate(self, question: str, ticker: str = "") -> dict:
        #load financial context if ticker provided
        context = ""
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

                    #defender rebuts
                    rebuttal = defender.rebut(reason, target_arg, context)
                    arguments[defender.agent_id] = rebuttal
                    graph.add_argument(rebuttal)

        #compute winner
        solver = ExtensionSolver(graph)
        grounded = solver.grounded()
        preferred = solver.preferred()

        return {
            "question": question,
            "ticker": ticker,
            "context": context,
            "arguments": arguments,
            "grounded": grounded,
            "preferred": preferred,
            "graph": graph,
            "winner": self._pick_winner(grounded, arguments),
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