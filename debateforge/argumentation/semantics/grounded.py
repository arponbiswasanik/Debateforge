from debateforge.argumentation.argument import Argument
from debateforge.argumentation.attack_graph import AttackGraph


def is_defended(argument: Argument, defended: set[Argument], graph: AttackGraph) -> bool:
    #an argument is defended if all its attackers are attacked by the defended set
    attackers = graph.get_attackers(argument)
    return all(
        any(d in graph.get_attackers(attacker) for d in defended)
        for attacker in attackers
    )


def grounded_extension(graph: AttackGraph) -> set[Argument]:
    #iteratively compute the grounded extension
    defended = set()

    while True:
        new_defended = {
            arg for arg in graph.arguments
            if not graph.is_attacked(arg) or is_defended(arg, defended, graph)
        }

        if new_defended == defended:
            break

        defended = new_defended

    return defended