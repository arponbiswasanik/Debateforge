import streamlit as st


def render_result(winner: str, total_attacks: int, grounded_count: int):
    is_consensus = "Consensus" in winner
    is_no_consensus = "No consensus" in winner

    if is_consensus:
        bg, border, icon = "#f0fdf4", "#16a34a", ""
    elif is_no_consensus:
        bg, border, icon = "#fef2f2", "#dc2626", ""
    else:
        bg, border, icon = "#eff6ff", "#2563eb", ""

    st.markdown(f"""
    <div style="
        background: {bg};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 24px;
    ">
        <p style="font-size: 13px; color: #64748b; margin: 0 0 4px 0; font-weight: 600; letter-spacing: 0.05em;">
            DEBATE RESULT
        </p>
        <p style="font-size: 20px; font-weight: 700; color: #1e293b; margin: 0;">
                {winner}
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; text-align: center;">
            <p style="font-size: 28px; font-weight: 700; color: #1e293b; margin: 0;">{total_attacks}</p>
            <p style="font-size: 12px; color: #64748b; margin: 4px 0 0 0; font-weight: 600;">TOTAL ATTACKS</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; text-align: center;">
            <p style="font-size: 28px; font-weight: 700; color: #1e293b; margin: 0;">{grounded_count}</p>
            <p style="font-size: 12px; color: #64748b; margin: 4px 0 0 0; font-weight: 600;">ACCEPTED ARGS</p>
        </div>
        """, unsafe_allow_html=True)