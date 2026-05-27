import networkx as nx
from debateforge.argumentation.attack_graph import AttackGraph
from debateforge.argumentation.argument import Argument


class ArgumentGraphVisualizer:
    def __init__(self, graph: AttackGraph, grounded: set[Argument]):
        self.graph = graph
        self.grounded = grounded
        self.nx_graph = self._build()

    def _build(self) -> nx.DiGraph:
        G = nx.DiGraph()

        for arg in self.graph.arguments:
            status = "accepted" if arg in self.grounded else "rejected"
            G.add_node(
                arg.argument_id,
                label=f"[{arg.agent_id.upper()}]\n{arg.claim[:60]}...",
                agent=arg.agent_id,
                status=status,
                strength=arg.strength,
            )

        for attack in self.graph.attacks:
            G.add_edge(
                attack.attacker.argument_id,
                attack.target.argument_id,
                reason=attack.reason[:80],
                strength=attack.strength,
            )

        return G

    def to_plotly(self) -> dict:
        import plotly.graph_objects as go

        pos = nx.spring_layout(self.nx_graph, seed=42)

        # color mapping
        color_map = {
            ("bull", "accepted"): "#16a34a",
            ("bull", "rejected"): "#86efac",
            ("bear", "accepted"): "#dc2626",
            ("bear", "rejected"): "#fca5a5",
            ("devil", "accepted"): "#7c3aed",
            ("devil", "rejected"): "#c4b5fd",
        }

        node_x, node_y, node_colors, node_text = [], [], [], []

        for node, data in self.nx_graph.nodes(data=True):
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            key = (data["agent"], data["status"])
            node_colors.append(color_map.get(key, "#94a3b8"))
            node_text.append(data["label"])

        edge_x, edge_y = [], []
        for u, v in self.nx_graph.edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            mode="lines",
            line=dict(width=1.5, color="#94a3b8"),
            hoverinfo="none",
        )

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode="markers+text",
            marker=dict(size=20, color=node_colors, line=dict(width=2, color="#1e293b")),
            text=node_text,
            textposition="top center",
            hoverinfo="text",
        )

        return {"edge_trace": edge_trace, "node_trace": node_trace}