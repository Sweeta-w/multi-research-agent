import os

import streamlit as st

from crew.research_crew import (
    AGENT_ORDER,
    build_crew,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResearchFlow AI",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(99, 102, 241, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(14, 165, 233, 0.08),
                transparent 30%
            ),
            #f8fafc;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ---------- HERO ---------- */

    .hero {
        padding: 2.5rem 1rem 2rem 1rem;
        text-align: center;
    }

    .hero-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 999px;
        background: rgba(99, 102, 241, 0.10);
        color: #4f46e5;
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: clamp(2.2rem, 6vw, 4.4rem);
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -0.045em;
        color: #0f172a;
        margin: 0;
    }

    .hero-title span {
        color: #4f46e5;
    }

    .hero-subtitle {
        max-width: 720px;
        margin: 1.2rem auto 0 auto;
        color: #64748b;
        font-size: clamp(1rem, 2vw, 1.18rem);
        line-height: 1.7;
    }

    /* ---------- CARDS ---------- */

    .glass-card {
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid rgba(226, 232, 240, 0.95);
        border-radius: 22px;
        padding: 1.4rem;
        box-shadow:
            0 10px 35px rgba(15, 23, 42, 0.06);
        backdrop-filter: blur(12px);
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 750;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }

    .section-description {
        color: #64748b;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }

    /* ---------- AGENT STATUS ---------- */

    .agent-card {
        display: flex;
        align-items: center;
        gap: 0.9rem;
        padding: 0.9rem;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        background: #ffffff;
        margin-bottom: 0.7rem;
    }

    .agent-icon {
        width: 42px;
        height: 42px;
        min-width: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        background: #eef2ff;
        font-size: 1.2rem;
    }

    .agent-name {
        font-weight: 700;
        color: #0f172a;
        font-size: 0.92rem;
    }

    .agent-description {
        color: #64748b;
        font-size: 0.78rem;
        margin-top: 0.15rem;
    }

    /* ---------- STATUS ---------- */

    .working {
        border: 1px solid #818cf8;
        background: #eef2ff;
    }

    .completed {
        border: 1px solid #bbf7d0;
        background: #f0fdf4;
    }

    .waiting {
        opacity: 0.62;
    }

    /* ---------- REPORT ---------- */

    .report-container {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 22px;
        padding: clamp(1.2rem, 4vw, 2.5rem);
        box-shadow:
            0 15px 45px rgba(15, 23, 42, 0.06);
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.8rem;
        padding-top: 2rem;
    }

    /* ---------- MOBILE ---------- */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            padding-top: 1rem;
        }

        .glass-card {
            border-radius: 16px;
            padding: 1rem;
        }

        .report-container {
            border-radius: 16px;
            padding: 1rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            ✦ MULTI-AGENT RESEARCH SYSTEM
        </div>

        <h1 class="hero-title">
            Research smarter with<br>
            <span>AI teammates.</span>
        </h1>

        <p class="hero-subtitle">
            A CrewAI-powered research team that plans your question,
            searches for evidence, checks the findings, and writes
            a structured research report.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# INPUT AREA
# ============================================================

left, right = st.columns(
    [1.55, 1],
    gap="large",
)


with left:

    st.markdown(
        """
        <div class="glass-card">

            <div class="section-title">
                What do you want to research?
            </div>

            <div class="section-description">
                Ask a focused question. Your AI research team
                will investigate it step by step.
            </div>

        """,
        unsafe_allow_html=True,
    )

    topic = st.text_area(
        "Research question",
        placeholder=(
            "Example: How is generative AI changing "
            "software development?"
        ),
        height=150,
        label_visibility="collapsed",
    )

    start = st.button(
        "🚀 Start Research",
        type="primary",
        use_container_width=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


with right:

    st.markdown(
        """
        <div class="glass-card">

            <div class="section-title">
                Your research team
            </div>

            <div class="section-description">
                Four specialized agents work sequentially.
            </div>

        """,
        unsafe_allow_html=True,
    )

    for agent in AGENT_ORDER:

        st.markdown(
            f"""
            <div class="agent-card">

                <div class="agent-icon">
                    {agent["icon"]}
                </div>

                <div>
                    <div class="agent-name">
                        {agent["name"]}
                    </div>

                    <div class="agent-description">
                        {agent["description"]}
                    </div>
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# RESEARCH EXECUTION
# ============================================================

if start:

    if not topic.strip():

        st.warning(
            "Please enter a research question first."
        )

        st.stop()

    if not os.getenv("GROQ_API_KEY"):

        st.error(
            "GROQ_API_KEY is missing. "
            "Add it in Streamlit Secrets."
        )

        st.stop()

    if not os.getenv("SERPER_API_KEY"):

        st.error(
            "SERPER_API_KEY is missing. "
            "Add it in Streamlit Secrets."
        )

        st.stop()

    st.divider()

    st.subheader("Research progress")

    current_status = st.empty()

    progress_bar = st.progress(
        0
    )

    status_cards = []

    for _ in AGENT_ORDER:

        status_cards.append(
            st.empty()
        )

    # --------------------------------------------------------
    # UI STATUS FUNCTION
    # --------------------------------------------------------

    def update_status(completed_agent, next_agent):

        completed_lower = completed_agent.lower()

        if "planner" in completed_lower:

            completed_index = 0
            next_index = 1

        elif "research" in completed_lower:

            completed_index = 1
            next_index = 2

        elif "fact" in completed_lower:

            completed_index = 2
            next_index = 3

        else:

            completed_index = 3
            next_index = 4

        # Completed agent

        agent = AGENT_ORDER[completed_index]

        status_cards[completed_index].markdown(
            f"""
            <div class="agent-card completed">

                <div class="agent-icon">
                    ✓
                </div>

                <div>

                    <div class="agent-name">
                        {agent["name"]} — Completed
                    </div>

                    <div class="agent-description">
                        {agent["description"]}
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        # Next agent

        if next_index < len(AGENT_ORDER):

            next_agent_data = AGENT_ORDER[next_index]

            current_status.markdown(
                f"""
                <div class="glass-card">

                    <strong>
                        {next_agent_data["icon"]}
                        Currently working:
                        {next_agent_data["name"]}
                    </strong>

                    <div style="color:#64748b;margin-top:6px;">
                        {next_agent_data["description"]}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

            status_cards[next_index].markdown(
                f"""
                <div class="agent-card working">

                    <div class="agent-icon">
                        {next_agent_data["icon"]}
                    </div>

                    <div>

                        <div class="agent-name">
                            {next_agent_data["name"]} — Working
                        </div>

                        <div class="agent-description">
                            {next_agent_data["description"]}
                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

            progress_bar.progress(
                next_index / len(AGENT_ORDER)
            )

    # --------------------------------------------------------
    # INITIAL STATE
    # --------------------------------------------------------

    current_status.markdown(
        """
        <div class="glass-card">

            <strong>
                🧭 Currently working: Research Planner
            </strong>

            <div style="color:#64748b;margin-top:6px;">
                Breaking your research question into focused areas.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    status_cards[0].markdown(
        """
        <div class="agent-card working">

            <div class="agent-icon">
                🧭
            </div>

            <div>

                <div class="agent-name">
                    Research Planner — Working
                </div>

                <div class="agent-description">
                    Breaking the research question into focused areas.
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    for index in range(1, len(AGENT_ORDER)):

        agent = AGENT_ORDER[index]

        status_cards[index].markdown(
            f"""
            <div class="agent-card waiting">

                <div class="agent-icon">
                    {agent["icon"]}
                </div>

                <div>

                    <div class="agent-name">
                        {agent["name"]}
                    </div>

                    <div class="agent-description">
                        Waiting for previous agent.
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # RUN CREW
    # --------------------------------------------------------

    try:

        research_crew = build_crew(
            status_callback=update_status
        )

        result = research_crew.kickoff(
            inputs={
                "topic": topic.strip()
            }
        )

        progress_bar.progress(1.0)

        current_status.success(
            "✅ All research agents completed."
        )

        st.divider()

        st.subheader("Research Report")

        st.markdown(
            '<div class="report-container">',
            unsafe_allow_html=True,
        )

        st.markdown(
            result.raw
            if hasattr(result, "raw")
            else str(result)
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    except Exception as error:

        current_status.error(
            "Research stopped because an error occurred."
        )

        st.error(
            f"Error: {error}"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        ResearchFlow AI · CrewAI + Groq · Built for evidence-driven research
    </div>
    """,
    unsafe_allow_html=True,
)