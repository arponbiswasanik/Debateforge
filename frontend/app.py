import streamlit as st
from debateforge.debate import DebateEngine
from components.debate_view import render_argument_card, render_attacks
from components.graph_view import render_graph
from components.result_view import render_result

st.set_page_config(
    page_title="DebateForge",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #f8fafc;
    }

    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 900px;
    }

    .stButton > button {
        background: #1e293b;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 11px 24px;
        font-weight: 600;
        font-size: 14px;
        white-space: nowrap;
    }

    .stButton > button:hover {
        background: #334155;
        color: white;
    }

    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1.5px solid #e2e8f0;
        background: #ffffff;
        font-size: 14px;
        padding: 10px 14px;
    }

    .stTextInput > div > div > input:focus {
        border-color: #1e293b;
        box-shadow: none;
    }

    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 13px;
    }

    .stSpinner > div {
        border-top-color: #1e293b !important;
    }
            


    .stTextInput input {
        border-radius: 8px !important;
        border: 1.5px solid #cbd5e1 !important;
        background: #ffffff !important;
        font-size: 15px !important;
        padding: 12px 16px !important;
        color: #1e293b !important;
        z-index: 10 !important;
        position: relative !important;
    }
    
    .stTextInput input::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }

    .stTextInput input:focus {
        border-color: #1e293b !important;
        box-shadow: 0 0 0 1px #1e293b !important;
    }
            
    /* Fix Warning/Alert Text Color */
    div[data-testid="stAlert"] {
        background-color: #fef08a !important; 
        border-radius: 8px !important;
        border: 1px solid #fde047 !important;
    }
    
    div[data-testid="stAlert"] p {
        color: #854d0e !important; 
        font-weight: 500 !important;
        font-size: 14px !important;
        margin: 0 !important;
    }
            
/* Fix Spinner/Loading Text */
    div[data-testid="stSpinner"] p {
        color: #64748b !important; 
        font-size: 14px !important;
        font-weight: 500 !important;
        margin-left: 10px !important;
    }

    /* Fix Spinner Circle Visibility */
    div[data-testid="stSpinner"] i, 
    div[data-testid="stSpinner"] > div[class*="spinner"] {
        border-color: #e2e8f0 !important; 
        border-top-color: #64748b !important;
        border-width: 3px !important;
    }
            

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
            
    /* Fix Input Cursor Color */
    .stTextInput input, 
    div[data-baseweb="input"] input {
        caret-color: #1e293b !important; 
    }


    /* Fix Tabs and Result Section Visibility */
    
    .stTabs [data-baseweb="tab"] p {
        color: #64748b !important; 
        font-weight: 600 !important;
    }
    
    .stTabs [aria-selected="true"] p {
        color: #1e293b !important; 
    }

    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #1e293b !important; 
    }

    div[data-baseweb="tab-panel"] p,
    div[data-baseweb="tab-panel"] li {
        color: #334155 !important; 
    }
           

</style>
""", unsafe_allow_html=True)

# header
st.markdown("""
<div style="
    background: linear-gradient(109.6deg, rgba(240,244,248,1) 11.2%, rgba(255,255,255,1) 91.1%);
    padding: 45px 32px;
    border-radius: 16px;
    margin-top: 10px;
    margin-bottom: 40px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    text-align: center;
">
    <div style="display: flex; justify-content: center; align-items: center; gap: 12px; margin-bottom: 16px;">
        <span style="
            background: #1e293b;
            color: #ffffff;
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.5px;
            padding: 8px 22px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(30, 41, 59, 0.15);
        ">DebateForge</span>
        <span style="
            background: #f0fdf4;
            color: #16a34a;
            font-size: 12px;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 20px;
            border: 1px solid #bbf7d0;
            letter-spacing: 0.05em;
        ">BETA</span>
    </div>
    <p style="color: #64748b; font-size: 15px; margin: 0; letter-spacing: 0.01em; font-weight: 500;">
        Multi-agent epistemic debate · Formal argumentation theory · Real financial data
    </p>
</div>
""", unsafe_allow_html=True)

#search box
col1, col2 = st.columns([7, 1.5])

with col1:
    question = st.text_input(
        "Question",
        placeholder="e.g. Should I invest in Google?",
        label_visibility="collapsed",
    )

with col2:
    run = st.button("Run Debate")


st.markdown("""
<p style="color: #cbd5e1; font-size: 12px; margin: 4px 0 32px 4px;">
    Ticker is auto-detected from your question
</p>
""", unsafe_allow_html=True)

st.markdown("<hr style='border: none; height: 1.3px; background-color: #cbd5e1; margin: 10px 0;'>", unsafe_allow_html=True)


# session state
if "detected_ticker" not in st.session_state:
    st.session_state.detected_ticker = ""
if "debate_result" not in st.session_state:
    st.session_state.debate_result = None

ticker = st.session_state.detected_ticker

if run:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Agents are debating..."):
            engine = DebateEngine()
            result = engine.debate(question, ticker=ticker.strip().upper() if ticker.strip() else "")
            st.session_state.debate_result = result
            if result.get("ticker"):
                st.session_state.detected_ticker = result["ticker"]

if st.session_state.debate_result:
    result = st.session_state.debate_result

    render_result(
        winner=result["winner"],
        total_attacks=len(result["graph"].attacks),
        grounded_count=len(result["grounded"]),
    )

    tab0, tab1, tab2, tab3 = st.tabs(["Decision", "Arguments", "Attacks", "Graph"])

    with tab0:
        if result.get("conclusion"):
            positive = ["BUY", "YES", "RECOMMENDED", "OPTION A", "OPTION B", "BOTH"]
            negative = ["SELL", "NO", "NOT RECOMMENDED"]

            verdict_color = {}
            for v in positive:
                verdict_color[v] = "#16a34a"
            for v in negative:
                verdict_color[v] = "#dc2626"

            verdict = "UNCERTAIN"
            if "VERDICT:" in result["conclusion"].upper():
                verdict_line = [l for l in result["conclusion"].split("\n") if l.upper().startswith("VERDICT:")]
                if verdict_line:
                    verdict = verdict_line[0].split(":", 1)[1].strip().upper()

            color = verdict_color.get(verdict, "#d97706")

            reasoning, key_risk = "", ""
            for line in result["conclusion"].split("\n"):
                if line.upper().startswith("REASONING:"):
                    reasoning = line.split(":", 1)[1].strip()
                elif line.upper().startswith("KEY RISK:"):
                    key_risk = line.split(":", 1)[1].strip()

            st.markdown(f"""
            <div style="
                background: #ffffff;
                border: 1.5px solid {color};
                border-left: 5px solid {color};
                border-radius: 12px;
                padding: 28px 32px;
                margin-top: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            ">
                <p style="font-size: 11px; color: #94a3b8; margin: 0 0 12px 0; font-weight: 700; letter-spacing: 0.1em;">
                    RECOMMENDATION
                </p>
                <span style="
                    background: {color};
                    color: #ffffff !important;
                    padding: 6px 18px;
                    border-radius: 6px;
                    font-size: 15px;
                    font-weight: 800;
                    letter-spacing: 0.08em;
                ">{verdict}</span>
                <p style="color: #1e293b; font-size: 15px; line-height: 1.8; margin: 20px 0 0 0;">
                    {reasoning}
                </p>
                <div style="
                    background: #f8fafc;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 14px 18px;
                    margin-top: 20px;
                ">
                    <p style="font-size: 11px; color: #94a3b8; font-weight: 700; letter-spacing: 0.08em; margin: 0 0 6px 0;">
                        ⚠️ KEY RISK
                    </p>
                    <p style="color: #475569; font-size: 14px; margin: 0; line-height: 1.6;">
                        {key_risk}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No conclusion available.")

    with tab1:
        for agent_id, arg in result["arguments"].items():
            is_accepted = arg in result["grounded"]
            render_argument_card(agent_id, arg, is_accepted)

    with tab2:
        render_attacks(result["graph"])

    with tab3:
        render_graph(result["graph"], result["grounded"])