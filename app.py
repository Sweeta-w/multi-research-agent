import os

import streamlit as st

from crew.research_crew import AGENT_ORDER, build_crew


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
# Use st.html() instead of st.markdown() for HTML/CSS.
# ============================================================

st.html(
    """
    <style>

    /* =====================================================
       GLOBAL
    ===================================================== */

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


    /* =====================================================
       HERO
    ===================================================== */

    .hero {
        padding: 2.5rem 1rem 2rem 1rem;
        text-align: center;
    }

    .hero-badge {
        display: inline-block;

        padding: 0.45rem 0.85rem;

        border-radius: 999px;

        background: rgba(99, 102, 241, 0.10);

        border: 1px solid rgba(99, 102, 241, 0.15);

        color: #4f46e5;

        font-size: 0.78rem;

        font-weight: 700;

        letter-spacing: 0.04em;

        margin-bottom: 1rem;
    }

    .hero-title {
        margin: 0;

        font-size: clamp(
            2.3rem,
            6vw,
            4.5rem
        );

        line-height: 1.04;

        font-weight: 800;

        letter-spacing: -0.05em;

        color: #0f172a;
    }

    .hero-title span {
        color: #4f46e5;
    }

    .hero-subtitle {
        max-width: 720px;

        margin: 1.25rem auto 0 auto;

        color: #64748b;

        font-size: clamp(
            0.95rem,
            2vw,
            1.12rem
        );

        line-height: 1.7;
    }


    /* =====================================================
       CARDS
    ===================================================== */

    .glass-card {
        background: rgba(
            255,
            255,
            255,
            0.82
        );

        border: 1px solid
            rgba(
                226,
                232,
                240,
                0.95
            );

        border-radius: 22px;

        padding: 1.4rem;

        box-shadow:
            0 10px 35px
            rgba(
                15,
                23,
                42,
                0.06
            );

        backdrop-filter: blur(12px);

        margin-bottom: 1rem;
    }


    /* =====================================================
       SECTION TEXT
    ===================================================== */

    .section-title {
        font-size: 1.1rem;

        font-weight: 750;

        color: #0f172a;

        margin-bottom: 0.3rem;
    }

    .section-description {
        color: #64748b;

        font-size: 0.88rem;

        line-height: 1.5;

        margin-bottom: 0;
    }


    /* =====================================================
       AGENT CARD
    ===================================================== */

    .agent-card {
        display: flex;

        align-items: center;

        gap: 0.9rem;

        padding: 0.9rem;

        border-radius: 15px;

        border: 1px solid #e2e8f0;

        background: #ffffff;

        margin-bottom: 0.7rem;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .agent-card:hover {
        transform: translateY(-1px);

        box-shadow:
            0 8px 20px
            rgba(
                15,
                23,
                42,
                0.06
            );
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

        font-size: 1.15rem;
    }

    .agent-name {
        font-weight: 700;

        color: #0f172a;

        font-size: 0.92rem;
    }

    .agent-description {
        color: #64748b;

        font-size: 0.78rem;

        line-height: 1.4;

        margin-top: 0.15rem;
    }


    /* =====================================================
       AGENT STATES
    ===================================================== */

    .working {
        border-color: #818cf8;

        background:
            linear-gradient(
                135deg,
                #eef2ff,
                #ffffff
            );

        box-shadow:
            0 0 0 1px
            rgba(
                99,
                102,
                241,
                0.08
            ),
            0 10px 25px
            rgba(
                99,
                102,
                241,
                0.08
            );
    }

    .completed {
        border-color: #bbf7d0;

        background:
            linear-gradient(
                135deg,
                #f0fdf4,
                #ffffff
            );
    }

    .waiting {
        opacity: 0.58;
    }


    /* =====================================================
       CURRENT AGENT
    ===================================================== */

    .current-agent {
        display: flex;

        align-items: center;

        gap: 0.8rem;

        padding: 1rem 1.1rem;

        border-radius: 16px;

        border: 1px solid
            rgba(
                129,
                140,
                248,
                0.35
            );

        background:
            linear-gradient(
                135deg,
                #eef2ff,
                #ffffff
            );

        margin-bottom: 1rem;
    }

    .current-agent-dot {
        width: 11px;

        height: 11px;

        min-width: 11px;

        border-radius: 50%;

        background: #6366f1;

        box-shadow:
            0 0 0 5px
            rgba(
                99,
                102,
                241,
                0.12
            );
    }

    .current-agent-title {
        color: #312e81;

        font-size: 0.95rem;

        font-weight: 750;
    }

    .current-agent-description {
        color: #64748b;

        font-size: 0.8rem;

        margin-top: 0.2rem;
    }


    /* =====================================================
       REPORT
    ===================================================== */

    .report-container {
        background: #ffffff;

        border: 1px solid #e2e8f0;

        border-radius: 22px;

        padding: clamp(
            1.2rem,
            4vw,
            2.5rem
        );

        box-shadow:
            0 15px 45px
            rgba(
                15,
                23,
                42,
                0.06
            );

        line-height: 1.75;
    }


    /* =====================================================
       FOOTER
    ===================================================== */

    .footer {
        text-align: center;

        color: #94a3b8;

        font-size: 0.78rem;

        padding-top: 2.5rem;
    }


    /* =====================================================
       MOBILE
    ===================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }

        .hero {
            padding:
                1.5rem
                0.5rem
                1.5rem;
        }

        .hero-title {
            font-size: 2.5rem;
        }

        .hero-subtitle {
            font-size: 0.95rem;
        }

        .glass-card {
            border-radius: 16px;
            padding: 1rem;
        }

        .report-container {
            border-radius: 16px;
            padding: 1rem;
        }

        .agent-card {
            padding: 0.75rem;
        }

        .agent-icon {
            width: 38px;
            height: 38px;
            min-width: 38px;
        }
    }


    /* =====================================================
       VERY SMALL SCREENS
    ===================================================== */

    @media (max-width: 420px) {

        .hero-title {
            font-size: 2.15rem;
        }

        .hero-badge {
            font-size: 0.7rem;
        }

        .hero-subtitle {
            font-size: 0.88rem;
        }

        .section-title {
            font-size: 1rem;
        }
    }

    </style>
    """
)


# ============================================================
# HERO
# ============================================================

st.html(
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
    """
)


# ============================================================
# MAIN LAYOUT
# ============================================================

left_column, right_column = st.columns(
    [1.55, 1],
    gap="large",
)


# ============================================================
# LEFT — RESEARCH INPUT
# ============================================================

with left_column:

    st.html(
        """
        <div class="glass-card">

            <div class="section-title">
                What do you want to research?
            </div>

            <div class="section-description">
                Ask a focused question. Your AI research team
                will investigate it step by step.
            </div>

        </div>
        """
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

    start_research = st.button(
        "🚀  Start Research",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# RIGHT — RESEARCH TEAM
# ============================================================

with right_column:

    st.html(
        """
        <div class="glass-card">

            <div class="section-title">
                Your research team
            </div>

            <div class="section-description">
                Four specialized agents work sequentially.
            </div>

        </div>
        """
    )

    for agent in AGENT_ORDER:

        st.html(
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
            """
        )


# ============================================================
# START RESEARCH
# ============================================================

if start_research:

    # --------------------------------------------------------
    # VALIDATE QUESTION
    # --------------------------------------------------------

    if not topic.strip():

        st.warning(
            "Please enter a research question first."
        )

        st.stop()


    # --------------------------------------------------------
    # VALIDATE GROQ
    # --------------------------------------------------------

    if not os.getenv("GROQ_API_KEY"):

        st.error(
            "GROQ_API_KEY is missing. "
            "Add it in Streamlit Secrets."
        )

        st.stop()


    # --------------------------------------------------------
    # VALIDATE SERPER
    # --------------------------------------------------------

    if not os.getenv("SERPER_API_KEY"):

        st.error(
            "SERPER_API_KEY is missing. "
            "Add it in Streamlit Secrets."
        )

        st.stop()


    # ========================================================
    # PROGRESS UI
    # ========================================================

    st.divider()

    st.subheader(
        "Research progress"
    )


    current_status = st.empty()


    progress_bar = st.progress(0)


    status_cards = []

    for _ in AGENT_ORDER:

        status_cards.append(
            st.empty()
        )


    # ========================================================
    # STATUS CALLBACK
    # ========================================================

    def update_status(
        completed_agent,
        next_agent,
    ):

        completed_lower = (
            str(completed_agent)
            .lower()
        )


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


        # ----------------------------------------------------
        # COMPLETED
        # ----------------------------------------------------

        completed_data = (
            AGENT_ORDER[
                completed_index
            ]
        )

        status_cards[
            completed_index
        ].markdown(
            f"""
            <div class="agent-card completed">

                <div class="agent-icon">
                    ✓
                </div>

                <div>

                    <div class="agent-name">
                        {completed_data["name"]}
                        — Completed
                    </div>

                    <div class="agent-description">
                        {completed_data["description"]}
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


        # ----------------------------------------------------
        # NEXT AGENT
        # ----------------------------------------------------

        if next_index < len(AGENT_ORDER):

            next_data = (
                AGENT_ORDER[
                    next_index
                ]
            )


            current_status.markdown(
                f"""
                <div class="current-agent">

                    <div class="current-agent-dot">
                    </div>

                    <div>

                        <div class="current-agent-title">
                            {next_data["icon"]}
                            Currently working:
                            {next_data["name"]}
                        </div>

                        <div class="current-agent-description">
                            {next_data["description"]}
                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


            status_cards[
                next_index
            ].markdown(
                f"""
                <div class="agent-card working">

                    <div class="agent-icon">
                        {next_data["icon"]}
                    </div>

                    <div>

                        <div class="agent-name">
                            {next_data["name"]}
                            — Working
                        </div>

                        <div class="agent-description">
                            {next_data["description"]}
                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


            progress_bar.progress(
                int(
                    next_index
                    / len(AGENT_ORDER)
                    * 100
                )
            )


    # ========================================================
    # INITIAL STATE
    # ========================================================

    first_agent = AGENT_ORDER[0]


    current_status.markdown(
        f"""
        <div class="current-agent">

            <div class="current-agent-dot">
            </div>

            <div>

                <div class="current-agent-title">
                    {first_agent["icon"]}
                    Currently working:
                    {first_agent["name"]}
                </div>

                <div class="current-agent-description">
                    {first_agent["description"]}
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # First agent

    status_cards[0].markdown(
        f"""
        <div class="agent-card working">

            <div class="agent-icon">
                {first_agent["icon"]}
            </div>

            <div>

                <div class="agent-name">
                    {first_agent["name"]}
                    — Working
                </div>

                <div class="agent-description">
                    {first_agent["description"]}
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # Waiting agents

    for index in range(
        1,
        len(AGENT_ORDER),
    ):

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


    # ========================================================
    # RUN CREW
    # ========================================================

    try:

        research_crew = build_crew(
            status_callback=update_status
        )


        result = research_crew.kickoff(
            inputs={
                "topic": topic.strip()
            }
        )


        # ----------------------------------------------------
        # COMPLETE
        # ----------------------------------------------------

        progress_bar.progress(100)

        current_status.success(
            "✅ All research agents completed."
        )


        st.divider()

        st.subheader(
            "Research Report"
        )


        # ----------------------------------------------------
        # REPORT CONTAINER
        # ----------------------------------------------------

        st.html(
            """
            <div class="report-container">
            """
        )


        if hasattr(
            result,
            "raw",
        ):

            st.markdown(
                result.raw
            )

        else:

            st.markdown(
                str(result)
            )


        st.html(
            """
            </div>
            """
        )


    # ========================================================
    # ERROR
    # ========================================================

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

st.html(
    """
    <div class="footer">
        ResearchFlow AI · CrewAI + Groq
        · Evidence-driven multi-agent research
    </div>
    """
)