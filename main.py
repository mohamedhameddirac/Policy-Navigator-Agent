"""
Main entry point for Policy Navigator Agent
"""
import os
import sys

def main():
    """Main entry point"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           📋 Policy Navigator Agent                       ║
║           Multi-Agent RAG System                          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

What would you like to do?

1. 🚀 Create new agent (first time setup)
2. 💬 Query existing agent (CLI)
3. 🌐 Launch web interface (Streamlit)
4. ⚙️  Configure environment
5. ℹ️  Show help
6. 🚪 Exit

""")
    
    choice = input("Enter your choice (1-6): ").strip()
    
    if choice == "1":
        print("\n🚀 Creating Policy Navigator Agent...")
        print("This will take a few minutes...\n")
        from src.agents.create_agents import create_complete_agent
        create_complete_agent()
        
    elif choice == "2":
        query = input("\n📝 Enter your question: ")
        agent_id = os.getenv("AGENT_ID")
        if not agent_id:
            print("❌ Error: AGENT_ID not configured. Run setup first (option 4)")
            return
        
        from aixplain.factories import AgentFactory
        api_key = os.getenv("AIXPLAIN_API_KEY")
        if api_key:
            os.environ["AIXPLAIN_API_KEY"] = api_key
        
        print("\n🤖 Querying agent...")
        agent = AgentFactory.get(agent_id)
        response = agent.run(query)
        print(f"\n📋 Response:\n{response.data.output}\n")
        
    elif choice == "3":
        print("\n🌐 Launching web interface...")
        print("Access at: http://localhost:8501\n")
        os.system("streamlit run ui/streamlit_app.py")
        
    elif choice == "4":
        print("\n⚙️  Running configuration setup...")
        os.system("python -m ui.cli setup")
        
    elif choice == "5":
        print("""
📚 Policy Navigator Agent Help

Setup:
  1. Configure .env file with AIXPLAIN_API_KEY
  2. Run: python main.py (choose option 1)
  3. Save Agent ID and Index ID to .env
  
Usage:
  - Web UI: streamlit run ui/streamlit_app.py
  - CLI: python -m ui.cli query -q "your question"
  - Python: See README.md for code examples

Documentation:
  - README.md: Full documentation
  - SETUP.md: Detailed setup guide
  - project-planning-and-arch.md: Architecture details

Support:
  - https://docs.aixplain.com/
  - Create GitHub issue for bugs
        """)
        
    elif choice == "6":
        print("\n👋 Goodbye!\n")
        sys.exit(0)
        
    else:
        print("\n❌ Invalid choice. Please select 1-6.\n")

if __name__ == "__main__":
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
