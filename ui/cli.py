"""
CLI Interface for Policy Navigator Agent
"""
import click
import os
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Load environment
load_dotenv()
init()  # Initialize colorama

@click.group()
def cli():
    """Policy Navigator Agent - Command Line Interface"""
    pass

@cli.command()
@click.option('--query', '-q', prompt='Your question', help='Policy question to ask')
@click.option('--agent-id', '-a', help='Agent ID (uses env var if not provided)')
@click.option('--session-id', '-s', help='Session ID for context')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def query(query, agent_id, session_id, verbose):
    """Query the Policy Navigator Agent"""
    
    # Get agent ID
    agent_id = agent_id or os.getenv("AGENT_ID")
    if not agent_id:
        click.echo(f"{Fore.RED}Error: Agent ID not provided. Set AGENT_ID env var or use --agent-id{Style.RESET_ALL}")
        return
    
    try:
        from aixplain.factories import AgentFactory
        
        # Set API key
        api_key = os.getenv("AIXPLAIN_API_KEY")
        if api_key:
            os.environ["AIXPLAIN_API_KEY"] = api_key
        
        click.echo(f"\n{Fore.CYAN}🤖 Querying agent...{Style.RESET_ALL}")
        
        # Get and run agent
        agent = AgentFactory.get(agent_id)
        response = agent.run(query, session_id=session_id)
        
        # Display response
        click.echo(f"\n{Fore.GREEN}📋 Response:{Style.RESET_ALL}")
        click.echo(f"{response.data.output}\n")
        
        if verbose:
            click.echo(f"{Fore.YELLOW}Metadata:{Style.RESET_ALL}")
            click.echo(f"  Credits used: {response.used_credits}")
            click.echo(f"  Runtime: {response.run_time}s")
            if hasattr(response.data, 'session_id'):
                click.echo(f"  Session ID: {response.data.session_id}")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

@cli.command()
@click.option('--agent-id', '-a', help='Agent ID to check')
def status(agent_id):
    """Check agent status"""
    
    agent_id = agent_id or os.getenv("AGENT_ID")
    if not agent_id:
        click.echo(f"{Fore.RED}Error: Agent ID not provided{Style.RESET_ALL}")
        return
    
    try:
        from aixplain.factories import AgentFactory
        
        api_key = os.getenv("AIXPLAIN_API_KEY")
        if api_key:
            os.environ["AIXPLAIN_API_KEY"] = api_key
        
        agent = AgentFactory.get(agent_id)
        
        click.echo(f"\n{Fore.GREEN}✓ Agent Status{Style.RESET_ALL}")
        click.echo(f"  Name: {agent.name}")
        click.echo(f"  ID: {agent.id}")
        click.echo(f"  Description: {agent.description}")
        click.echo()
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

@cli.command()
def examples():
    """Show example queries"""
    
    examples_list = [
        ("Check Policy Status", "Is Executive Order 14067 still in effect or has it been repealed?"),
        ("Find Case Law", "Has Section 230 ever been challenged in court? What was the outcome?"),
        ("EPA Compliance", "What are compliance requirements for small businesses under EPA clean air regulations?"),
        ("Policy Deadlines", "When does the new privacy policy take effect?"),
        ("Regulation Search", "What are the latest environmental protection regulations?"),
    ]
    
    click.echo(f"\n{Fore.CYAN}📚 Example Queries:{Style.RESET_ALL}\n")
    
    for title, example in examples_list:
        click.echo(f"{Fore.GREEN}{title}:{Style.RESET_ALL}")
        click.echo(f"  {example}\n")

@cli.command()
@click.option('--output', '-o', default='.env', help='Output file path')
def setup(output):
    """Setup configuration"""
    
    click.echo(f"\n{Fore.CYAN}🔧 Policy Navigator Agent Setup{Style.RESET_ALL}\n")
    
    api_key = click.prompt("aiXplain API Key")
    agent_id = click.prompt("Agent ID (optional, press Enter to skip)", default="", show_default=False)
    index_id = click.prompt("Index ID (optional, press Enter to skip)", default="", show_default=False)
    
    config = f"""# aiXplain Configuration
AIXPLAIN_API_KEY={api_key}
AGENT_ID={agent_id}
INDEX_ID={index_id}

# External APIs (optional)
COURTLISTENER_API_KEY=
SLACK_WEBHOOK_URL=

# Settings
DEBUG=False
LOG_LEVEL=INFO
"""
    
    with open(output, 'w') as f:
        f.write(config)
    
    click.echo(f"\n{Fore.GREEN}✓ Configuration saved to {output}{Style.RESET_ALL}")
    click.echo(f"You can now use the CLI with: {Fore.CYAN}python -m ui.cli query{Style.RESET_ALL}\n")

if __name__ == '__main__':
    cli()
