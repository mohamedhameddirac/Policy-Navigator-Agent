"""
Streamlit Web Interface for Policy Navigator Agent
"""
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Policy Navigator Agent",
    page_icon="📋",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: 700;
    color: #1e3a8a;
    text-align: center;
    margin-bottom: 0.5rem;
    background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sub-header {
    font-size: 1.1rem;
    color: #64748b;
    text-align: center;
    margin-bottom: 2rem;
    font-weight: 400;
}
.answer-box {
    background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%);
    padding: 1.5rem;
    border-radius: 0.75rem;
    border-left: 4px solid #3b82f6;
    margin: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.stButton>button {
    width: 100%;
    border-radius: 0.5rem;
    font-weight: 500;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'show_debug' not in st.session_state:
    st.session_state.show_debug = False
if 'show_metadata' not in st.session_state:
    st.session_state.show_metadata = True

# Title
st.markdown('<div class="main-header">📋 Policy Navigator Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Government Regulation Search</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/us-capitol.png", width=80)
    st.markdown("### About")
    st.markdown("""
    <div style='font-size: 0.9rem; color: #475569;'>
    Policy Navigator Agent provides intelligent access to:
    
    • 📜 Executive Orders & Federal Regulations  
    • ⚖️ Case Law & Court Decisions  
    • 🏛️ Compliance Requirements  
    • 📊 Policy Status Tracking
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ Configuration")
    agent_id = st.text_input("Agent ID", value=os.getenv("AGENT_ID", ""), type="password")
    
    # Advanced options
    with st.expander("🔧 Advanced Options"):
        st.session_state.show_debug = st.checkbox("Show Debug Info", value=st.session_state.show_debug)
        st.session_state.show_metadata = st.checkbox("Show Metadata", value=st.session_state.show_metadata)
    
    # Slack Integration
    with st.expander("📢 Slack Notifications"):
        st.write("Send custom alerts to Slack:")
        slack_title = st.text_input("Alert Title", placeholder="Policy Update")
        slack_message = st.text_area("Message", placeholder="Important policy information...", height=100)
        if st.button("📨 Send to Slack", use_container_width=True):
            if slack_title and slack_message:
                try:
                    from src.tools.slack_integration import SlackIntegration
                    slack = SlackIntegration()
                    result = slack.send_notification(slack_title, slack_message)
                    if result.get('sent'):
                        st.success("✅ Notification sent to Slack!")
                    else:
                        st.error(f"❌ Failed: {result.get('error', 'Unknown error')}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please enter both title and message")
    
    st.markdown("---")
    st.markdown("### 💡 Quick Examples")
    if st.button("📜 Check EO Status", use_container_width=True):
        st.session_state.example_query = "Is Executive Order 14067 still active?"
    if st.button("⚖️ Find Case Law", use_container_width=True):
        st.session_state.example_query = "Has Section 230 been challenged in court?"
    if st.button("🏭 EPA Compliance", use_container_width=True):
        st.session_state.example_query = "What are compliance requirements for small businesses under EPA clean air regulations?"
    
    st.markdown("---")
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.session_id = None
        st.rerun()

# Main content
st.markdown("### 🔍 Ask Your Question")
query_input = st.text_area(
    "Query Input",
    value=st.session_state.get('example_query', ''),
    height=120,
    placeholder="e.g., Is Executive Order 14067 still in effect? What are the current EPA regulations for emissions?",
    label_visibility="collapsed"
)

# Clear example after use
if 'example_query' in st.session_state:
    del st.session_state.example_query

col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([2, 2, 2, 4])
with col_btn1:
    search_button = st.button("🔍 Search", type="primary", use_container_width=True)
with col_btn2:
    maintain_context = st.checkbox("💬 Context", value=True, help="Maintain conversation context for follow-up questions")

st.markdown("---")

# Process query
if search_button and query_input:
    if not agent_id:
        st.error("Please enter your Agent ID in the sidebar")
    else:
        try:
            # Import aixplain
            from aixplain.factories import AgentFactory
            
            # Set API key
            api_key = os.getenv("AIXPLAIN_API_KEY")
            if api_key:
                os.environ["AIXPLAIN_API_KEY"] = api_key
            
            # Get agent
            with st.spinner("🤖 Analyzing your query..."):
                agent = AgentFactory.get(agent_id)
                
                # Run agent
                response = agent.run(
                    query_input,
                    session_id=st.session_state.session_id if maintain_context else None
                )
                
                # Show debug info only if enabled
                if st.session_state.show_debug:
                    with st.expander("🔧 Debug Information", expanded=False):
                        st.write("**Response Type:**", type(response))
                        st.write("**Response Attributes:**", dir(response))
                        st.json({"raw_response": str(response)})
                
                # Extract response data
                output_text = None
                credits_used = 0
                runtime = 0
                
                # Try different ways to extract the output
                if hasattr(response, 'data'):
                    if hasattr(response.data, 'output'):
                        output_text = response.data.output
                    elif hasattr(response.data, 'content'):
                        output_text = response.data.content
                    elif isinstance(response.data, str):
                        output_text = response.data
                    else:
                        output_text = str(response.data)
                elif hasattr(response, 'output'):
                    output_text = response.output
                elif hasattr(response, 'content'):
                    output_text = response.content
                elif isinstance(response, str):
                    output_text = response
                else:
                    output_text = str(response)
                
                # Get credits and runtime
                credits_used = getattr(response, 'used_credits', getattr(response, 'credits', 0))
                runtime = getattr(response, 'run_time', getattr(response, 'runtime', 0))
                
                # External Tool Integration: Auto-send to Slack for important findings
                # This satisfies the certificate requirement for external tool integration
                try:
                    from src.tools.slack_integration import SlackIntegration
                    
                    # Check if response contains important policy information
                    important_keywords = ['revoked', 'repealed', 'no longer in effect', 'amended', 
                                        'compliance deadline', 'court decision', 'ruled that', 'rescinded']
                    
                    if any(keyword.lower() in output_text.lower() for keyword in important_keywords):
                        slack = SlackIntegration()
                        slack_result = slack.send_notification(
                            title=f"Policy Alert: {query_input[:60]}...",
                            content=output_text[:800] + "..." if len(output_text) > 800 else output_text,
                            source="Policy Navigator Agent"
                        )
                        if slack_result.get('sent'):
                            st.success("📢 Important finding sent to Slack!")
                except Exception as slack_error:
                    if st.session_state.show_debug:
                        st.warning(f"Slack notification skipped: {str(slack_error)}")
                
                # Update session
                if maintain_context and hasattr(response, 'data') and hasattr(response.data, 'session_id'):
                    st.session_state.session_id = response.data.session_id
                
                # Add to history
                st.session_state.chat_history.append({
                    "query": query_input,
                    "response": output_text,
                    "credits": credits_used,
                    "runtime": runtime
                })
                
                # Display response
                st.markdown("### 📄 Answer")
                st.markdown(f'<div class="answer-box">{output_text}</div>', unsafe_allow_html=True)
                
                # Metadata (only if enabled)
                if st.session_state.show_metadata:
                    st.markdown("---")
                    col_meta1, col_meta2, col_meta3 = st.columns(3)
                    with col_meta1:
                        st.metric("💳 Credits Used", f"{credits_used:.4f}")
                    with col_meta2:
                        st.metric("⏱️ Runtime", f"{runtime:.2f}s")
                    with col_meta3:
                        st.metric("📊 Queries", len(st.session_state.chat_history))
                
                # Sources (if available)
                if hasattr(response, 'details') and response.details:
                    with st.expander("📚 View Sources & Details"):
                        st.json(response.details)
        
        except Exception as e:
            import traceback
            st.error(f"❌ **Error:** {str(e)}")
            if st.session_state.show_debug:
                with st.expander("🔧 View Full Error Details"):
                    st.code(traceback.format_exc())
            else:
                st.info("💡 Enable 'Show Debug Info' in Advanced Options to see detailed error information")

# Chat history
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("### 💬 Recent Conversations")
    
    # Show last 5 conversations
    for i, chat in enumerate(reversed(st.session_state.chat_history[-5:]), 1):
        idx = len(st.session_state.chat_history) - i + 1
        with st.expander(f"💭 Query #{idx}: {chat['query'][:80]}{'...' if len(chat['query']) > 80 else ''}"):
            st.markdown("**🔍 Question:**")
            st.info(chat['query'])
            st.markdown("**📄 Answer:**")
            st.success(chat['response'])
            if st.session_state.show_metadata:
                col1, col2 = st.columns(2)
                with col1:
                    st.caption(f"💳 Credits: {chat['credits']:.4f}")
                with col2:
                    st.caption(f"⏱️ Runtime: {chat['runtime']:.2f}s")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <div style="color: #64748b; font-size: 0.95rem; margin-bottom: 0.5rem;">
        <strong>Policy Navigator Agent</strong> | Powered by aiXplain Agentic OS
    </div>
    <div style="color: #94a3b8; font-size: 0.85rem;">
        <a href="https://docs.aixplain.com" target="_blank" style="color: #3b82f6; text-decoration: none;">📚 Documentation</a> | 
        <a href="https://aixplain.com" target="_blank" style="color: #3b82f6; text-decoration: none;">🌐 aiXplain</a>
    </div>
</div>
""", unsafe_allow_html=True)
