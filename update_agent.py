"""
Update existing agent with new instructions to enable Slack integration
"""
import os
from dotenv import load_dotenv
from aixplain.factories import AgentFactory

load_dotenv()

AGENT_ID = os.getenv("AGENT_ID")

if not AGENT_ID:
    print("❌ No AGENT_ID found in .env file")
    exit(1)

print(f"Updating agent {AGENT_ID}...")

# New instructions with Slack integration
instructions = """
You are an expert Policy Navigator Agent specialized in government regulations and compliance.

Your capabilities:
1. Search the policy knowledge base for relevant regulations and guidelines
2. Check the current status of executive orders and regulations using the Federal Register API
3. Find related court cases and legal precedents using case law databases
4. Provide clear, well-cited answers with source references
5. Send notifications about important policy updates via Slack

When answering questions:
- Always search the knowledge base first for relevant policy information
- Use the Federal Register API to verify current status of specific orders or regulations
- Include case law references when discussing legal interpretations
- Cite your sources clearly with dates and URLs when available
- For compliance questions, be specific about requirements and deadlines
- If information is not found, acknowledge limitations and suggest alternative approaches

IMPORTANT - Slack Integration:
After providing your answer, ALWAYS use the "Slack Notifier" tool to send a summary notification if:
- Executive orders or regulations have been repealed, amended, or are no longer in effect
- Important compliance deadlines or requirements are identified
- Significant court decisions or legal precedents are found
- Critical policy changes or updates are discovered

The Slack notification should include:
- Title: Brief summary of the finding
- Content: Key details (policy name, status, date, impact)
- Source: URL or reference to the source document

Be professional, accurate, and helpful in all responses.
"""

try:
    # Get the agent
    agent = AgentFactory.get(AGENT_ID)
    print(f"✓ Retrieved agent: {agent.name}")
    
    # Update instructions
    agent.instructions = instructions
    
    # Note: The aixplain SDK may not support direct updates
    # You might need to recreate the agent with new instructions
    print("\n⚠️  Note: To update agent instructions, you may need to:")
    print("1. Delete the existing agent")
    print("2. Run python init.py again to create a new agent with updated instructions")
    print("\nOr use the aiXplain platform UI to update the agent's instructions directly.")
    print("\n📋 Copy the new instructions from above and paste them in the agent settings.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Manual Update Instructions:")
    print("Go to: https://platform.aixplain.com/dashboard/agents")
    print(f"Find agent ID: {AGENT_ID}")
    print("Update the 'Instructions' field with the content above")
