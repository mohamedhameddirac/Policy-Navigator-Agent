"""
Demo Script for Policy Navigator Agent
This script demonstrates all key features for the certificate project
"""

import os
import time
from dotenv import load_dotenv

# Load environment
load_dotenv()
os.environ["AIXPLAIN_API_KEY"] = os.getenv("AIXPLAIN_API_KEY")

from aixplain.factories import AgentFactory

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def demo_query(agent, query, description):
    """Execute and display a demo query"""
    print(f"📝 {description}")
    print(f"Query: \"{query}\"\n")
    print("🤖 Processing...")
    
    start_time = time.time()
    response = agent.run(query)
    elapsed = time.time() - start_time
    
    print(f"\n✅ Response ({elapsed:.1f}s):")
    print(f"{response.data.output}\n")
    print(f"💳 Credits: {response.used_credits:.4f}")
    print(f"⏱️  Runtime: {response.run_time:.2f}s\n")
    
    return response

def main():
    print_section("Policy Navigator Agent - Certificate Demo")
    
    # Get agent
    agent_id = os.getenv("AGENT_ID").strip("'\"")
    print(f"Loading agent: {agent_id}")
    agent = AgentFactory.get(agent_id)
    
    print(f"✓ Agent loaded: {agent.name}")
    print(f"✓ Tools available: {len(agent.tools)}")
    for tool in agent.tools:
        print(f"  • {tool.name}")
    
    # Demo 1: Vector Index Search
    print_section("Demo 1: Vector Index RAG Search")
    demo_query(
        agent,
        "What are the EPA requirements for clean air compliance?",
        "Testing vector index retrieval with policy dataset"
    )
    
    # Demo 2: External API Integration
    print_section("Demo 2: External API Integration (Federal Register)")
    demo_query(
        agent,
        "Is Executive Order 14067 still in effect?",
        "Real-time API call to verify executive order status"
    )
    
    print("💡 Check your Slack channel - the agent should have sent a notification!")
    
    # Demo 3: Multi-turn Conversation
    print_section("Demo 3: Multi-turn Conversation Context")
    
    response1 = demo_query(
        agent,
        "What are OSHA workplace safety requirements?",
        "Initial query about workplace safety"
    )
    
    session_id = response1.data.session_id
    
    print("\n🔄 Follow-up question with context...")
    response2 = agent.run(
        "What are the penalties for non-compliance?",
        session_id=session_id
    )
    
    print(f"\n✅ Follow-up Response:")
    print(f"{response2.data.output}\n")
    
    # Demo 4: Complex Query with Multiple Tools
    print_section("Demo 4: Complex Query Using Multiple Tools")
    demo_query(
        agent,
        "Find recent court cases related to Section 230 and tell me the current regulatory status",
        "Testing coordinated use of CourtListener API + vector search"
    )
    
    # Summary
    print_section("Demo Complete - Certificate Requirements Met")
    
    print("✅ RAG Pipeline: Vector index with semantic search")
    print("✅ Data Sources:")
    print("   • CSV dataset (10 policy documents)")
    print("   • Web scraping (5+ EPA regulation pages)")
    print("✅ Tool Integration:")
    print("   • Custom Python tools (Federal Register, CourtListener)")
    print("   • Marketplace tool (Google Search)")
    print("   • External integration (Slack notifications)")
    print("✅ UI/CLI: Streamlit web interface + CLI")
    print("✅ Documentation: Comprehensive README and guides")
    
    print("\n🎥 Record this demo for your submission video!")
    print("📧 Submit to: devrel@aixplain.com")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you:")
        print("1. Ran 'python main.py' to create the agent")
        print("2. Set AGENT_ID in your .env file")
        print("3. Have a valid AIXPLAIN_API_KEY")
