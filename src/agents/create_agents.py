"""
Create and configure Policy Navigator Agent with vector index and tools
"""
import os
from typing import List, Dict, Any
import logging
from aixplain.factories import IndexFactory, AgentFactory
from aixplain.modules.model.record import Record
from aixplain.enums import Function, Supplier

from ..config import AIXPLAIN_API_KEY, AGENT_CONFIG, SLACK_WEBHOOK_URL
from ..utils.helpers import setup_logger
from ..data_ingestion.dataset_loader import DatasetLoader
from ..data_ingestion.web_scraper import PolicyWebScraper
from ..config import RAW_DATA_DIR

logger = setup_logger(__name__)


class PolicyAgentCreator:
    """Create and configure the Policy Navigator Agent"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize agent creator
        
        Args:
            api_key: aiXplain API key
        """
        self.api_key = api_key or AIXPLAIN_API_KEY
        if self.api_key:
            os.environ["AIXPLAIN_API_KEY"] = self.api_key
        else:
            logger.warning("No aiXplain API key provided")
        
        self.index = None
        self.agent = None
        self.agent_name = "Policy Navigator Agent"  # Default name, can be overridden
        logger.info("PolicyAgentCreator initialized")
    
    def create_vector_index(self, name: str = "Policy Knowledge Base") -> Any:
        """
        Create vector index for policy documents
        
        Args:
            name: Index name
        
        Returns:
            Created index object
        """
        logger.info(f"Creating vector index: {name}")
        
        try:
            self.index = IndexFactory.create(
                name=name,
                description="Government regulations, compliance policies, and public health guidelines"
            )
            
            logger.info(f"Vector index created with ID: {self.index.id}")
            print(f"✓ Vector Index Created: {self.index.id}")
            return self.index
            
        except Exception as e:
            logger.error(f"Error creating vector index: {e}")
            raise
    
    def ingest_sample_data(self):
        """Load and ingest sample policy data into the index"""
        if not self.index:
            raise ValueError("Index not created. Call create_vector_index() first.")
        
        logger.info("Ingesting sample data...")
        
        # Create sample dataset
        loader = DatasetLoader(RAW_DATA_DIR)
        df = loader.create_sample_dataset()
        
        # Prepare records
        policy_records = loader.prepare_policy_records(df)
        
        # Convert to aixplain Record format
        records = []
        for policy in policy_records:
            record = Record(
                id=policy['id'],
                value=policy['text'],
                value_type="text",
                attributes=policy['attributes']
            )
            records.append(record)
        
        # Upsert to index
        logger.info(f"Upserting {len(records)} records to index...")
        self.index.upsert(records)
        
        # Verify count
        count = self.index.count()
        logger.info(f"Index now contains {count} documents")
        print(f"✓ Ingested {count} policy documents")
        
        return count
    
    def ingest_scraped_data(self):
        """Scrape and ingest web data"""
        if not self.index:
            raise ValueError("Index not created. Call create_vector_index() first.")
        
        logger.info("Scraping and ingesting web data...")
        
        # Scrape documents
        scraper = PolicyWebScraper(RAW_DATA_DIR / "scraped_policies", delay=0.5)
        documents = scraper.scrape_all_sources(
            search_terms=["environmental protection", "clean air act", "compliance"]
        )
        
        # Save scraped data
        scraper.save_documents(documents, "scraped_policies.json")
        
        # Convert to Record format
        records = []
        for doc in documents:
            record = Record(
                id=doc.get('id', doc.get('title', '')[:50].replace(' ', '_')),
                value=doc.get('text', doc.get('title', '')),
                value_type="text",
                attributes={
                    'category': doc.get('category', 'Unknown'),
                    'agency': doc.get('agency', 'Unknown'),
                    'date': doc.get('date', ''),
                    'type': doc.get('type', 'Document')
                }
            )
            records.append(record)
        
        # Upsert to index
        logger.info(f"Upserting {len(records)} scraped records to index...")
        self.index.upsert(records)
        
        count = self.index.count()
        logger.info(f"Index now contains {count} documents after scraping")
        print(f"✓ Added {len(records)} scraped documents (Total: {count})")
        
        return len(records)
    
    def create_custom_tools(self) -> List[Any]:
        """
        Create custom tools including Composio Slack integration
        
        Returns:
            List of tool objects
        """
        logger.info("Creating custom tools...")
        
        tools = []
        
        # Add authenticated Composio Slack integration
        try:
            from aixplain.factories import AgentFactory
            
            # Wrap Slack integration ID as agent tool
            # The integration ID acts as a model that the agent can call
            slack_tool = AgentFactory.create_model_tool("6929b47e938ddf0df24f223f")
            
            tools.append(slack_tool)
            logger.info("✓ Authenticated Slack integration added as agent tool")
            print(f"✓ Added Slack Notifier tool (Integration ID: 6929b47e938ddf0df24f223f)")
            print(f"  Type: Connected Slack Integration")
        except Exception as e:
            logger.error(f"Error adding Slack integration: {e}")
            print(f"⚠ Slack integration not available: {e}")
            import traceback
            print(traceback.format_exc())
        
        print(f"✓ Created {len(tools)} integration tools")
        return tools
    
    def create_agent(self, custom_tools: List[Any] = None) -> Any:
        """
        Create the Policy Navigator Agent
        
        Args:
            custom_tools: List of custom tools to add
        
        Returns:
            Created agent object
        """
        if not self.index:
            raise ValueError("Index not created. Call create_vector_index() first.")
        
        logger.info("Creating Policy Navigator Agent...")
        
        # Prepare tools
        tools = []
        
        # 1. Vector index tool (RAG)
        index_tool = AgentFactory.create_model_tool(self.index.id)
        tools.append(index_tool)
        logger.info("✓ Added vector index tool")
        
        # 2. Custom Python tools
        if custom_tools:
            tools.extend(custom_tools)
            logger.info(f"✓ Added {len(custom_tools)} custom tools")
        
        # 3. Marketplace tools (optional - add if available)
        try:
            # Web search tool for additional context
            from aixplain.factories import ToolFactory
            web_search_tool = ToolFactory.get("65c51c556eb563350f6e1bb1")
            tools.append(web_search_tool)
            logger.info("✓ Added Google Search marketplace tool")
        except Exception as e:
            logger.warning(f"Could not add marketplace tool: {e}")
        
        # Agent instructions
        instructions = """
        You are an expert Policy Navigator Agent specialized in government regulations and compliance.
        
        Your capabilities:
        1. Search the policy knowledge base for relevant regulations and guidelines
        2. Check the current status of executive orders and regulations using the Federal Register API
        3. Find related court cases and legal precedents using case law databases
        4. Provide clear, well-cited answers with source references
        5. Send notifications to Slack about important policy updates
        
        When answering questions:
        - Always search the knowledge base first for relevant policy information
        - Use the Federal Register API to verify current status of specific orders or regulations
        - Include case law references when discussing legal interpretations
        - Cite your sources clearly with dates and URLs when available
        - For compliance questions, be specific about requirements and deadlines
        - If information is not found, acknowledge limitations and suggest alternative approaches
        
        CRITICAL - Slack Notification Requirement:
        After providing your answer, you MUST use the 'utilities-aixplain-policynavigator' tool (Slack) to send a notification if ANY of these conditions are met:
        - Executive orders or regulations have been REVOKED, REPEALED, or are NO LONGER IN EFFECT
        - Important compliance deadlines or requirements are identified
        - Significant court decisions or legal precedents are found
        - Critical policy changes or updates are discovered
        
        To send a Slack notification, use:
        Action: utilities-aixplain-policynavigator
        Action Input: {
            "action": "SLACK_SEND_MESSAGE",
            "channel": "C0A17LR6T6U",
            "markdown_text": "## [Brief Title]\\n\\n**Status:** [Current status]\\n**Date:** [Date of change]\\n**Impact:** [Brief impact description]"
        }
        
        Be professional, accurate, and helpful in all responses.
        """
        
        # Create agent
        try:
            self.agent = AgentFactory.create(
                name=self.agent_name,
                description="AI assistant for government regulation queries and compliance research",
                instructions=instructions,
                tools=tools,
                llm_id=AGENT_CONFIG.get("llm_id")
            )
            
            logger.info(f"Agent created with ID: {self.agent.id}")
            print(f"✓ Policy Navigator Agent Created: {self.agent.id}")
            
            return self.agent
            
        except Exception as e:
            logger.error(f"Error creating agent: {e}")
            raise
    
    def deploy_agent(self):
        """Deploy the agent"""
        if not self.agent:
            raise ValueError("Agent not created. Call create_agent() first.")
        
        logger.info("Deploying agent...")
        
        try:
            self.agent.deploy()
            logger.info("Agent deployed successfully")
            print(f"✓ Agent Deployed Successfully")
            print(f"\nAgent ID: {self.agent.id}")
            print(f"Index ID: {self.index.id if self.index else 'N/A'}")
            
        except Exception as e:
            logger.error(f"Error deploying agent: {e}")
            raise
    
    def test_agent(self, query: str = "Is Executive Order 14067 still active?"):
        """
        Test the agent with a sample query
        
        Args:
            query: Test query
        """
        if not self.agent:
            raise ValueError("Agent not created")
        
        logger.info(f"Testing agent with query: {query}")
        print(f"\n🔍 Testing agent with query: '{query}'")
        
        try:
            response = self.agent.run(query)
            print(f"\n📝 Agent Response:")
            print(response.data.output)
            print(f"\n💰 Credits used: {response.used_credits}")
            print(f"⏱️  Runtime: {response.run_time}s")
            
            return response
            
        except Exception as e:
            logger.error(f"Error testing agent: {e}")
            print(f"❌ Error: {e}")
            raise


def create_complete_agent():
    """
    Create a complete Policy Navigator Agent with index and tools
    
    Returns:
        Tuple of (agent_creator, agent, index)
    """
    print("=" * 60)
    print("Policy Navigator Agent - Setup")
    print("=" * 60)
    
    creator = PolicyAgentCreator()
    
    # Step 1: Create vector index
    print("\n[1/5] Creating vector index...")
    index = creator.create_vector_index()
    
    # Step 2: Ingest data
    print("\n[2/5] Ingesting sample data...")
    creator.ingest_sample_data()
    
    print("\n[2.5/5] Scraping and ingesting web data...")
    creator.ingest_scraped_data()
    
    # Step 3: Create custom tools
    print("\n[3/5] Creating custom tools...")
    custom_tools = creator.create_custom_tools()
    
    # Step 4: Create agent
    print("\n[4/5] Creating agent...")
    agent = creator.create_agent(custom_tools)
    
    # Step 5: Deploy agent
    print("\n[5/5] Deploying agent...")
    creator.deploy_agent()
    
    print("\n" + "=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print(f"\n📋 Save these IDs to your .env file:")
    print(f"AGENT_ID={agent.id}")
    print(f"INDEX_ID={index.id}")
    print("\n")
    
    return creator, agent, index


# Example usage
if __name__ == "__main__":
    creator, agent, index = create_complete_agent()
    
    # Test the agent
    print("\nTesting agent...")
    creator.test_agent("What are the compliance requirements for clean air regulations?")
