import streamlit as st
from debateforge.argumentation.argument import Argument


def render_argument_card(agent_id: str, arg: Argument, is_accepted: bool):
    colors = {
        "bull": {"bg": "#f0fdf4", "border": "#16a34a", "badge": "#16a34a", "label": "BULL"},
        "bear": {"bg": "#fef2f2", "border": "#dc2626", "badge": "#dc2626", "label": "BEAR"},
        "devil": {"bg": "#f5f3ff", "border": "#7c3aed", "badge": "#7c3aed", "label": "DEVIL"},
    }

    c = colors.get(agent_id, {"bg": "#f8fafc", "border": "#94a3b8", "badge": "#94a3b8", "label": agent_id.upper()})
    status_icon = "✓" if is_accepted else "✗"
    status_color = "#16a34a" if is_accepted else "#dc2626"

    st.markdown(f"""
    <div style="
        background: {c['bg']};
        border-left: 4px solid {c['border']};
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="
                background: {c['badge']};
                color: #ffffff !important;
                padding: 2px 10px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 0.05em;
            ">{c['label']}</span>
            <span style="color: {status_color}; font-size: 13px; font-weight: 600;">
                {status_icon} {'Accepted' if is_accepted else 'Rejected'}
            </span>
        </div>
        <p style="color: #1e293b; font-size: 14px; line-height: 1.6; margin: 0;">
            {arg.claim}
        </p>
        <p style="color: #94a3b8; font-size: 11px; margin: 8px 0 0 0;">
            Strength: {arg.strength:.2f}
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_attacks(graph):
    if not graph.attacks:
        st.info("No attacks in this debate.")
        return

    for attack in graph.attacks:
        st.markdown(f"""
        <div style="
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 8px;
        ">
            <span style="font-weight: 600; color: #1e293b; font-size: 13px;">
                [{attack.attacker.agent_id.upper()}] → [{attack.target.agent_id.upper()}]
            </span>
            <p style="color: #475569; font-size: 13px; margin: 6px 0 0 0;">
                {attack.reason}
            </p>
        </div>
        """, unsafe_allow_html=True)