from debateforge.argumentation.argument import Argument
from debateforge.argumentation.attack_graph import AttackGraph


def is_conflict_free(args: set[Argument], graph: AttackGraph) -> bool:
    #no argument in the set attacks another in the same set
    for arg in args:
        for target in graph.get_targets(arg):
            if target in args:
                return False
    return True


def is_admissible(args: set[Argument], graph: AttackGraph) -> bool:
    if not is_conflict_free(args, graph):
        return False
    #every attacker of the set is counter-attacked by the set
    for arg in args:
        for attacker in graph.get_attackers(arg):
            if not any(arg2 in graph.get_attackers(attacker) for arg2 in args):
                return False
    return True


def preferred_extensions(graph: AttackGraph) -> list[set[Argument]]:
    all_args = list(graph.arguments)
    admissible_sets = []

    #check all subsets
    for i in range(1 << len(all_args)):
        subset = {all_args[j] for j in range(len(all_args)) if i & (1 << j)}
        if is_admissible(subset, graph):
            admissible_sets.append(subset)

    #keep only maximal admissible sets
    preferred = []
    for s in admissible_sets:
        if not any(s < other for other in admissible_sets):
            preferred.append(s)

    return preferred