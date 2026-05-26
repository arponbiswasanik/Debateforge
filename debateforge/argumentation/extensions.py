from debateforge.argumentation.attack_graph import AttackGraph
from debateforge.argumentation.semantics.grounded import grounded_extension
from debateforge.argumentation.semantics.preferred import preferred_extensions
from debateforge.argumentation.semantics.stable import stable_extensions


class ExtensionSolver:
    def __init__(self, graph: AttackGraph):
        self.graph = graph

    def grounded(self):
        return grounded_extension(self.graph)

    def preferred(self):
        return preferred_extensions(self.graph)

    def stable(self):
        return stable_extensions(self.graph)

    def solve_all(self) -> dict:
        return {
            "grounded": self.grounded(),
            "preferred": self.preferred(),
            "stable": self.stable(),
        }