from debateforge.argumentation import Argument, AttackGraph, ExtensionSolver


def make_arg(claim: str, agent_id: str) -> Argument:
    return Argument(claim=claim, evidence="test", agent_id=agent_id)


def test_unattacked_argument_in_grounded():
    graph = AttackGraph()
    a1 = make_arg("Revenue grew 23%", "bull")
    graph.add_argument(a1)

    solver = ExtensionSolver(graph)
    result = solver.grounded()

    assert a1 in result


def test_attacked_argument_not_in_grounded():
    graph = AttackGraph()
    a1 = make_arg("Revenue grew 23%", "bull")
    a2 = make_arg("Growth is inflation-adjusted misleading", "bear")

    graph.add_attack(a2, a1, reason="not inflation adjusted")

    solver = ExtensionSolver(graph)
    result = solver.grounded()

    assert a1 not in result


def test_reinstated_argument_in_grounded():
    graph = AttackGraph()
    a1 = make_arg("Revenue grew 23%", "bull")
    a2 = make_arg("Growth is misleading", "bear")
    a3 = make_arg("Real growth still positive", "skeptic")

    graph.add_attack(a2, a1, reason="misleading")
    graph.add_attack(a3, a2, reason="real growth positive")

    solver = ExtensionSolver(graph)
    result = solver.grounded()

    assert a1 in result
    assert a2 not in result