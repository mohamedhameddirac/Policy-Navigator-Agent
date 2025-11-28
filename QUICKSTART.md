# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API Key
Create `.env` file:
```bash
AIXPLAIN_API_KEY=your_api_key_here
```

Get your API key: https://platform.aixplain.com/

### 3. Create Agent
```bash
python main.py
# Choose option 1
```

Wait ~5 minutes for setup to complete.

### 4. Start Using

**Web Interface:**
```bash
streamlit run ui/streamlit_app.py
```

**Command Line:**
```bash
python -m ui.cli query -q "Is Executive Order 14067 active?"
```

## ✅ Verification

Test your agent:
```python
from aixplain.factories import AgentFactory
import os

os.environ["AIXPLAIN_API_KEY"] = "your_key"
agent = AgentFactory.get("your_agent_id")
response = agent.run("What are EPA regulations?")
print(response.data.output)
```

## 📋 Example Queries

- "Is Executive Order 14067 still in effect?"
- "Has Section 230 been challenged in court?"
- "What are EPA compliance requirements for small businesses?"

## 🆘 Need Help?

- Full documentation: `README.md`
- Setup guide: `SETUP.md`
- Architecture: `project-planning-and-arch.md`
- Issues: Create GitHub issue

---

**You're ready to go! 🎉**
