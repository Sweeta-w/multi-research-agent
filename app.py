import os
import streamlit as st
from crew import execute_stage
from utils.docx_exporter import convert_markdown_to_docx

# Page Configuration
st.set_page_config(
    page_title="InsightEngine | Multi-Agent AI Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Glassmorphism UI & Styling
st.markdown("""
<style>
    /* Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
        color: #c9d1d9;
    }
    
    /* Responsive Agent Cards */
    .agent-status-card {
        background: rgba(22, 27, 34, 0.85);
        border: 1px solid rgba(48, 54, 61, 0.9);
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* Model & Agent Status Badges */
    .badge-model {
        background: rgba(163, 113, 247, 0.15);
        color: #d2a8ff;
        border: 1px solid rgba(163, 113, 247, 0.4);
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 8px;
    }

    .badge-status {
        background: rgba(56, 139, 253, 0.15);
        color: #58a6ff;
        border: 1px solid rgba(56, 139, 253, 0.4);
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 8px;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1.0; }
        100% { opacity: 0.6; }
    }
</style>
""", unsafe_allow_html=True)

# Main Title Header
st.title("⚡ InsightEngine AI Studio")
st.caption("Autonomous Multi-Agent Research Platform built with CrewAI & Groq")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ System Configuration")
    
    # API Key Input
    groq_api_key = st.text_input(
        "Groq API Key", 
        type="password", 
        value=os.environ.get("GROQ_API_KEY", ""),
        help="Enter your Groq API Key to enable high-speed model inference."
    )
    
    # Model Selector
    selected_model = st.selectbox(
        "Active Inference Model",
        options=[
            "openai/gpt-oss-120b",
            "llama3-70b-8192",
            "llama3-8b-8192",
            "mixtral-8x7b-32768"
        ],
        index=0,
        help="Select the underlying LLM model that powers the agent network."
    )
    
    st.markdown("---")
    st.markdown("### 🤖 Assigned Agents")
    st.markdown("""
    1. **Senior Technical Researcher**  
       *Scans and extracts foundational technical facts.*
    2. **Data & Strategy Analyst**  
       *Cross-verifies raw facts and isolates core insights.*
    3. **Lead Technical Writer**  
       *Drafts structured Markdown & Word reports.*
    """)

# UI Display of Model Info
st.markdown(f"""
<div style="margin-bottom: 15px;">
    <span class="badge-model">⚡ ACTIVE LLM: {selected_model}</span>
    <span style="color: #8b949e; font-size: 0.85rem; margin-left: 10px;">Provider: Groq Cloud Inference</span>
</div>
""", unsafe_allow_html=True)

# User Query Input
topic = st.text_input("Research Topic / Query:", placeholder="e.g., Impact of Quantum-Resistant Cryptography on Cloud Security")

col1, col2 = st.columns([1, 4])
with col1:
    start_btn = st.button("🚀 Start Research", type="primary", use_container_width=True)

if start_btn:
    if not groq_api_key.strip():
        st.error("Please enter a valid Groq API Key in the sidebar.")
    elif not topic.strip():
        st.warning("Please provide a topic or query to begin research.")
    else:
        os.environ["GROQ_API_KEY"] = groq_api_key.strip()
        
        status_box = st.empty()
        progress_bar = st.progress(0)
        
        def update_agent_status(agent_title: str, activity_text: str):
            status_box.markdown(f"""
            <div class="agent-status-card">
                <div>
                    <span class="badge-model">MODEL: {selected_model}</span>
                    <span class="badge-status">RUNNING</span>
                </div>
                <h4 style="margin-top: 8px; margin-bottom: 4px; color: #f0f6fc;">{agent_title}</h4>
                <p style="margin: 0; color: #8b949e; font-size: 0.95rem;">{activity_text}</p>
            </div>
            """, unsafe_allow_html=True)

        try:
            # Stage 1: Researcher
            progress_bar.progress(15)
            raw_research = execute_stage("research", topic, selected_model, update_agent_status)
            
            # Stage 2: Analyst
            progress_bar.progress(50)
            analyzed_data = execute_stage("analysis", raw_research, selected_model, update_agent_status)
            
            # Stage 3: Writer
            progress_bar.progress(80)
            final_report = execute_stage("writing", analyzed_data, selected_model, update_agent_status)
            
            progress_bar.progress(100)
            status_box.success("🎉 All agents have finished processing successfully!")
            
            st.markdown("---")
            st.subheader("📄 Generated Research Report")
            
            # Render Markdown on UI
            st.markdown(final_report)
            
            st.markdown("---")
            st.subheader("📥 Export Options")
            
            # Generate Word Document Buffer
            docx_file = convert_markdown_to_docx(topic, final_report)
            
            btn_col1, btn_col2 = st.columns(2)
            
            with btn_col1:
                st.download_button(
                    label="📄 Download Word Document (.docx)",
                    data=docx_file,
                    file_name=f"{topic.lower().replace(' ', '_')}_report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
                
            with btn_col2:
                st.download_button(
                    label="📝 Download Markdown (.md)",
                    data=final_report,
                    file_name=f"{topic.lower().replace(' ', '_')}_report.md",
                    mime="text/markdown",
                    use_container_width=True
                )

        except Exception as e:
            status_box.empty()
            st.error(f"Execution Error: {str(e)}")