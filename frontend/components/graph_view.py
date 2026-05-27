import streamlit as st
from debateforge.visualization.renderer import render_debate_graph
from debateforge.argumentation.attack_graph import AttackGraph
from debateforge.argumentation.argument import Argument


def render_graph(graph: AttackGraph, grounded: set[Argument]):
    if not graph.attacks:
        st.info("No attacks to visualize.")
        return

    fig = render_debate_graph(graph, grounded)
    st.plotly_chart(fig, use_container_width=True)