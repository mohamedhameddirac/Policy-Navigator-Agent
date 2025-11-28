"""
Recreate the Policy Navigator Agent with updated Slack integration instructions
"""
import os
from dotenv import load_dotenv, set_key

# Load environment first
load_dotenv()

# Set API key before importing aixplain
os.environ["AIXPLAIN_API_KEY"] = os.getenv("AIXPLAIN_API_KEY")

from src.agents.create_agents import PolicyAgentCreator
from src.config import AGENT_CONFIG

print("=" * 70)
print("RECREATING POLICY NAVIGATOR AGENT WITH SLACK INTEGRATION")
print("=" * 70)

# Get existing IDs
old_agent_id = os.getenv("AGENT_ID")
index_id = os.getenv("INDEX_ID")

print(f"\nCurrent Agent ID: {old_agent_id}")
print(f"Vector Index ID: {index_id}")

if not index_id:
    print("\n❌ No INDEX_ID found. Please run init.py first.")
    exit(1)

print("\n" + "-" * 70)
input("Press Enter to recreate the agent with Slack integration enabled...")
print("-" * 70)

# Initialize setup
setup = PolicyAgentCreator()

# Load existing index
print("\n1. Loading existing vector index...")
from aixplain.factories import IndexFactory
setup.index = IndexFactory.get(index_id)
print(f"   ✓ Index loaded: {index_id}")

# Create custom tools (including Slack)
print("\n2. Creating custom tools...")
custom_tools = setup.create_custom_tools()

# Create new agent with updated instructions
print("\n3. Creating new agent with Slack integration...")
# Use a unique name for the new agent
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d-%H%M")
setup.agent_name = f"Policy Navigator Agent v2-{timestamp}"
new_agent = setup.create_agent(custom_tools)

# Update .env file with new agent ID
print("\n4. Updating .env file...")
env_file = ".env"
set_key(env_file, "AGENT_ID", new_agent.id)
print(f"   ✓ New Agent ID: {new_agent.id}")

print("\n" + "=" * 70)
print("✅ AGENT SUCCESSFULLY RECREATED!")
print("=" * 70)

print(f"""
Old Agent ID: {old_agent_id}
New Agent ID: {new_agent.id}
Index ID:     {index_id}

The agent now includes:
✓ Vector knowledge base (RAG)
✓ Federal Register API tool
✓ CourtListener case law tool
✓ Slack Notifier tool (with automatic usage instructions)
✓ Google Search tool

NEXT STEPS:
1. Restart Streamlit: streamlit run ui/streamlit_app.py
2. Test with query: "Is Executive Order 14067 still in effect?"
3. Check your Slack channel for automatic notification!

Note: The old agent ({old_agent_id}) is still on the platform.
You can delete it from: https://platform.aixplain.com/dashboard/agents
""")
