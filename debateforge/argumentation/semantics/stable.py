from debateforge.argumentation.argument import Argument
from debateforge.argumentation.attack_graph import AttackGraph
from debateforge.argumentation.semantics.preferred import is_conflict_free


def stable_extensions(graph: AttackGraph) -> list[set[Argument]]:
    all_args = list(graph.arguments)
    stable = []

    for i in range(1 << len(all_args)):
        subset = {all_args[j] for j in range(len(all_args)) if i & (1 << j)}

        if not is_conflict_free(subset, graph):
            continue

        #every argument outside the set must be attacked by the set
        outside = graph.arguments - subset
        if all(
            any(arg in graph.get_attackers(out) for arg in subset)
            for out in outside
        ):
            stable.append(subset)

    return stable