from dataclasses import dataclass
from debateforge.argumentation.argument import Argument
from debateforge.argumentation.attack_graph import AttackGraph


@dataclass
class DebateResult:
    question: str
    winner: str
    arguments: dict[str, Argument]
    grounded: set[Argument]
    preferred: list[set[Argument]]
    graph: AttackGraph

    def summary(self) -> str:
        lines = [
            f"Question: {self.question}",
            f"Winner: {self.winner}",
            f"",
            f"Arguments:",
        ]
        for agent_id, arg in self.arguments.items():
            status = "✓" if arg in self.grounded else "✗"
            lines.append(f"  {status} [{agent_id.upper()}]: {arg.claim[:100]}...")

        lines.append(f"")
        lines.append(f"Total attacks: {len(self.graph.attacks)}")
        return "\n".join(lines)