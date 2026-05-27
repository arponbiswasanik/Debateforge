import plotly.graph_objects as go
from debateforge.visualization.argument_graph import ArgumentGraphVisualizer
from debateforge.argumentation.attack_graph import AttackGraph
from debateforge.argumentation.argument import Argument


def render_debate_graph(graph: AttackGraph, grounded: set[Argument]) -> go.Figure:
    visualizer = ArgumentGraphVisualizer(graph, grounded)
    traces = visualizer.to_plotly()

    fig = go.Figure(
        data=[traces["edge_trace"], traces["node_trace"]],
        layout=go.Layout(
            paper_bgcolor="#ffffff",
            plot_bgcolor="#f8fafc",
            font=dict(family="Inter, sans-serif", size=11, color="#1e293b"),
            showlegend=False,
            hovermode="closest",
            margin=dict(t=20, b=20, l=20, r=20),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        )
    )

    return fig