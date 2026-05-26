from dataclasses import dataclass, field
from debateforge.argumentation.argument import Argument


@dataclass
class Attack:
    attacker: Argument
    target: Argument
    reason: str
    strength: float = 1.0


class AttackGraph:
    def __init__(self):
        self.arguments: set[Argument] = set()
        self.attacks: list[Attack] = []

    def add_argument(self, argument: Argument):
        self.arguments.add(argument)

    def add_attack(self, attacker: Argument, target: Argument, reason: str, strength: float = 1.0):
        self.arguments.add(attacker)
        self.arguments.add(target)
        self.attacks.append(Attack(attacker, target, reason, strength))

    def get_attackers(self, argument: Argument) -> list[Argument]:
        return [a.attacker for a in self.attacks if a.target == argument]

    def get_targets(self, argument: Argument) -> list[Argument]:
        return [a.target for a in self.attacks if a.attacker == argument]

    def is_attacked(self, argument: Argument) -> bool:
        return any(a.target == argument for a in self.attacks)

    def summary(self) -> str:
        return f"AttackGraph({len(self.arguments)} args, {len(self.attacks)} attacks)"
    
    