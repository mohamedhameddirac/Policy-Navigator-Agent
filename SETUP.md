# Setup Guide - Policy Navigator Agent

## Prerequisites

- Python 3.8 or higher
- pip package manager
- aiXplain API key ([Sign up](https://platform.aixplain.com/))

## Step-by-Step Setup

### 1. Clone and Install

```bash
# Navigate to project directory
cd d:\ai-xplain-crs

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
copy .env.example .env

# Edit .env file and add your keys:
# - AIXPLAIN_API_KEY=your_key_here
# - (Optional) COURTLISTENER_API_KEY=your_key
# - (Optional) SLACK_WEBHOOK_URL=your_webhook
```

### 3. Create Agent and Index

Run the agent creation script:

```bash
python -m src.agents.create_agents
```

This will:
1. ✅ Create vector index
2. ✅ Ingest sample policy data  
3. ✅ Scrape web data
4. ✅ Create custom tools
5. ✅ Deploy agent

**IMPORTANT**: Save the Agent ID and Index ID displayed at the end!

Add them to your `.env` file:
```
AGENT_ID=your_agent_id_here
INDEX_ID=your_index_id_here
```

### 4. Test the Agent

#### Option A: Web Interface
```bash
streamlit run ui/streamlit_app.py
```
Visit `http://localhost:8501`

#### Option B: Command Line
```bash
python -m ui.cli query -q "Is Executive Order 14067 still active?"
```

#### Option C: Python
```python
from aixplain.factories import AgentFactory
import os

os.environ["AIXPLAIN_API_KEY"] = "your_key"
agent = AgentFactory.get("your_agent_id")
response = agent.run("What are EPA compliance requirements?")
print(response.data.output)
```

## Optional Configuration

### CourtListener API (for case law)
1. Sign up at https://www.courtlistener.com/
2. Get API token from account settings
3. Add to `.env`: `COURTLISTENER_API_KEY=your_token`

### Slack Integration (for notifications)
1. Create Slack app and incoming webhook
2. Add to `.env`: `SLACK_WEBHOOK_URL=your_webhook_url`

## Troubleshooting

### "No API key" error
- Make sure `.env` file exists and contains `AIXPLAIN_API_KEY`
- Load it: `from dotenv import load_dotenv; load_dotenv()`

### "Agent not found" error
- Verify AGENT_ID in `.env` matches deployed agent
- Check agent exists: `python -m ui.cli status`

### Import errors
- Reinstall dependencies: `pip install -r requirements.txt --upgrade`
- Verify Python version: `python --version` (should be 3.8+)

### Slow response times
- First query may take longer (cold start)
- Subsequent queries will be faster
- Index needs ~5 minutes after creation for optimal performance

## Next Steps

1. **Customize the agent**: Edit instructions in `src/agents/create_agents.py`
2. **Add more data**: Use data ingestion scripts to add datasets
3. **Extend tools**: Create new custom tools in `src/tools/`
4. **Deploy**: Consider hosting on cloud platform for 24/7 availability

## Support

- Documentation: https://docs.aixplain.com/
- Issues: Create GitHub issue
- Community: Join aiXplain Discord

---

**You're all set! 🎉 Start querying government regulations with AI.**
