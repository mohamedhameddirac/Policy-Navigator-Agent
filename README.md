# Policy Navigator Agent 📋

> **Multi-Agent RAG System for Government Regulation Search**
> 
> Certificate Project for aiXplain Agentic OS

An AI-powered agent built with [aiXplain Agentic OS](https://docs.aixplain.com/) that helps users query and extract insights from complex government regulations, compliance policies, and public health guidelines.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![aiXplain](https://img.shields.io/badge/aiXplain-Agentic%20OS-green)](https://docs.aixplain.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)](https://streamlit.io/)

---

## 📹 Demo Video

🎥 **[Watch the 3-minute demo](YOUR_VIDEO_LINK_HERE)**

Quick walkthrough showing:
- Live policy query and retrieval
- External API integration (Federal Register)
- Slack notification for policy changes
- Multi-turn conversation with context

---

## 🎯 What This Agent Does

The Policy Navigator Agent is a comprehensive RAG (Retrieval-Augmented Generation) system that:

1. **🔍 Semantic Search**: Query government regulations and policies using natural language
2. **📊 Real-Time Status Checks**: Verify if executive orders and regulations are active via Federal Register API
3. **⚖️ Case Law Research**: Find related court cases and legal precedents using CourtListener API
4. **🔔 Automated Notifications**: Receive Slack alerts when policies are revoked, amended, or updated
5. **💬 Conversational Interface**: Maintain context across follow-up questions
6. **📚 Multi-Source Knowledge**: Combines structured datasets and web-scraped policy documents

### Example Interactions

**User:** "Is Executive Order 14067 still in effect?"

**Agent:** "Executive Order 14067, titled 'Ensuring Responsible Development of Digital Assets,' is no longer in effect. It was revoked by an executive order issued by President Trump on January 23, 2025."

*[Automatically sends Slack notification about the revocation]*

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│            Policy Navigator Agent                   │
│         (GPT-4o Orchestrator + Tools)               │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┬─────────────┐
        │                     │             │
┌───────▼────────┐   ┌───────▼────────┐   ┌▼──────────┐
│ Vector Index   │   │  External APIs │   │   Slack   │
│  (aiR Model)   │   │  - Fed Register│   │Integration│
│                │   │  - CourtListener   │           │
│  Policy Docs   │   │  - Google Search   │  Notifier │
└────────────────┘   └────────────────┘   └───────────┘
        │
┌───────▼────────────────────────────┐
│  Data Sources:                     │
│  • CSV Dataset (10 policies)       │
│  • Web Scraping (EPA policies)     │
└────────────────────────────────────┘
```

### Certificate Requirements Met ✅

| Requirement | Implementation | Status |
|------------|----------------|--------|
| **RAG Pipeline** | Vector index + Agent orchestration | ✅ |
| **Data Source 1** | CSV dataset (10 policy documents) | ✅ |
| **Data Source 2** | Web scraping (EPA regulations) | ✅ |
| **Tool Type 1** | External APIs (Federal Register, CourtListener) | ✅ |
| **Tool Type 2** | Marketplace Tool (Google Search) | ✅ |
| **Tool Type 3** | Third-party Integration (Slack) | ✅ |
| **UI/CLI** | Streamlit web interface | ✅ |
| **Documentation** | Comprehensive README + setup guides | ✅ |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- aiXplain API key ([Get one here](https://platform.aixplain.com/))
- Optional: Slack workspace for notifications

### 1. Clone the Repository

```bash
git clone https://github.com/mohamedhameddirac/Policy-Navigator-Agent.git
cd Policy-Navigator-Agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# Required:
AIXPLAIN_API_KEY=your_key_here
AIXPLAIN_TEAM_ID=your_team_id

# Optional (for full features):
COURTLISTENER_API_KEY=your_key_here
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_CHANNEL_ID=C0A17LR6T6U
```

### 4. Create the Agent

```bash
python main.py
```

This will:
- Create a vector index for policy documents
- Ingest sample data and scraped policies
- Set up the agent with all tools
- Save agent ID and index ID to `.env`

Expected output:
```
✓ Vector index created: 69299c913363c512376e199c
✓ Ingested 10 policy documents
✓ Scraped 5 EPA regulation pages
✓ Agent created: 6929ba5c67905faafe47d1fa
✓ Configuration saved to .env
```

### 5. Launch the UI

```bash
streamlit run ui/streamlit_app.py
```

Then open http://localhost:8501 in your browser.

---

## 📂 Project Structure

```
policy-navigator-agent/
├── src/
│   ├── agents/
│   │   └── create_agents.py      # Agent creation and configuration
│   ├── data_ingestion/
│   │   ├── dataset_loader.py     # CSV dataset loading
│   │   └── web_scraper.py        # Policy website scraping
│   ├── tools/
│   │   ├── federal_register.py   # Federal Register API tool
│   │   ├── court_listener.py     # CourtListener API tool
│   │   └── slack_integration.py  # Slack notification tool
│   ├── utils/
│   │   └── helpers.py            # Utility functions
│   └── config.py                 # Configuration management
├── ui/
│   ├── streamlit_app.py          # Main Streamlit interface
│   └── cli.py                    # Command-line interface
├── data/
│   ├── raw/
│   │   ├── sample_policies.csv   # Sample policy dataset
│   │   └── scraped_policies/     # Web-scraped content
│   └── processed/                # Processed data cache
├── logs/                         # Application logs
├── main.py                       # Setup and initialization
├── recreate_agent.py             # Agent update utility
├── update_agent.py               # Agent modification script
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── SETUP.md                      # Detailed setup guide
├── QUICKSTART.md                 # Quick start tutorial
├── SLACK_INTEGRATION.md          # Slack setup instructions
├── SUBMISSION_CHECKLIST.md       # Certificate requirements
└── README.md                     # This file
```

---

## 🛠️ Tool Integration Details

### 1. Vector Index (RAG)
- **Model**: aiR embedding model
- **Storage**: aiXplain vector index service
- **Content**: 15+ policy documents from dataset + web scraping
- **Retrieval**: Semantic search with similarity scoring

### 2. External APIs (Custom Python Tools)

#### Federal Register API
```python
# Check current status of executive orders
Tool: federal_register.py
Endpoint: https://www.federalregister.gov/api/v1
Purpose: Verify if regulations are active, repealed, or amended
```

#### CourtListener API
```python
# Find related court cases
Tool: court_listener.py
Endpoint: https://www.courtlistener.com/api/rest/v3
Purpose: Retrieve case law and legal precedents
```

### 3. Marketplace Tool
- **Google Search API**: Web search for recent policy updates and news
- **Integration**: Via aiXplain marketplace (Tool ID: 65c51c556eb563350f6e1bb1)

### 4. Third-Party Integration (Slack)
- **Type**: Authenticated Composio integration
- **Capabilities**: 
  - Automatic notifications for policy changes
  - Manual alerts for compliance deadlines
  - Formatted messages with policy details
- **Setup**: See [SLACK_INTEGRATION.md](SLACK_INTEGRATION.md)

---

## 💡 Example Use Cases

### 1. Policy Status Check
```
Query: "What is the current status of the Clean Air Act amendments?"
Agent: Searches vector index → Finds EPA guidelines → Returns summary with dates
```

### 2. Compliance Research
```
Query: "What are OSHA workplace safety requirements for small businesses?"
Agent: Retrieves OSHA policies → Highlights compliance steps → Cites specific sections
```

### 3. Legal Precedent Search
```
Query: "Has anyone challenged data privacy regulations in court?"
Agent: Uses CourtListener API → Finds relevant cases → Summarizes outcomes
```

### 4. Real-Time Verification
```
Query: "Is Executive Order 14067 still active?"
Agent: Calls Federal Register API → Checks current status → Sends Slack alert if revoked
```

---

## 🔧 Configuration Options

### Agent Customization

Edit `src/agents/create_agents.py` to customize:
- LLM model (default: GPT-4o)
- Temperature and response length
- Tool activation conditions
- Slack notification triggers

### UI Customization

Edit `ui/streamlit_app.py` to modify:
- Layout and styling
- Example queries
- Debug information display
- Metadata visibility

---

## 📊 Data Sources

### Dataset (CSV)
- **File**: `data/raw/sample_policies.csv`
- **Content**: 10 policy documents covering:
  - Environmental regulations (EPA)
  - Workplace safety (OSHA)
  - Data privacy (FTC)
  - Financial compliance (SEC)
  - Transportation rules (DOT)
  - Energy standards (DOE)

### Web Scraping
- **Source**: EPA website (www.epa.gov)
- **Content**: 5+ current EPA regulations
- **Method**: BeautifulSoup4 HTML parsing
- **Output**: `data/raw/scraped_policies/scraped_policies.json`

---

## 🧪 Testing

### Test the Agent Locally

```python
from aixplain.factories import AgentFactory
import os

agent = AgentFactory.get(os.getenv("AGENT_ID"))
response = agent.run("Is Executive Order 14067 still in effect?")
print(response.data.output)
```

### Test Individual Tools

```bash
# Test Federal Register API
python -c "from src.tools.federal_register import FederalRegisterTool; print(FederalRegisterTool().search_documents('14067'))"

# Test CourtListener API
python -c "from src.tools.court_listener import CourtListenerTool; print(CourtListenerTool().search_cases('Section 230'))"
```

---

## 📈 Future Improvements

### Short-term Enhancements
- [ ] **Multi-language support**: Add translation capabilities for international policies
- [ ] **PDF upload**: Allow users to upload their own policy documents
- [ ] **Email notifications**: Alternative to Slack for policy alerts
- [ ] **Advanced filters**: Search by agency, date range, policy type
- [ ] **Export functionality**: Download search results as PDF/CSV

### Long-term Vision
- [ ] **Team agent architecture**: Separate specialized agents for:
  - Document summarization agent
  - Compliance analysis agent
  - Timeline extraction agent
- [ ] **Memory/caching layer**: Store frequently asked queries for faster responses
- [ ] **Analytics dashboard**: Track query patterns and popular topics
- [ ] **API endpoint**: REST API for programmatic access
- [ ] **Mobile app**: iOS/Android companion app
- [ ] **Regulatory change tracking**: Automated monitoring of new policy publications

### Advanced Features
- [ ] **Comparative analysis**: Compare policies across jurisdictions
- [ ] **Deadline calculator**: Auto-calculate compliance deadlines
- [ ] **Document relationship mapping**: Visualize policy connections
- [ ] **Citation validator**: Verify policy references and sources
- [ ] **Batch processing**: Analyze multiple policies simultaneously

---

## 🤝 Contributing

This is a certificate project, but suggestions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **aiXplain Team**: For the Agentic OS platform and SDK
- **Federal Register API**: Public access to government documents
- **CourtListener**: Free Law Project's legal database
- **EPA**: Environmental policy data source
- **Streamlit**: Interactive UI framework

---

## 📧 Contact

**Developer**: Mohamed Hamed
**Email**: [Your Email]
**Project Link**: [https://github.com/mohamedhameddirac/Policy-Navigator-Agent](https://github.com/mohamedhameddirac/Policy-Navigator-Agent)

---

## 📚 Additional Resources

- [aiXplain Documentation](https://docs.aixplain.com/)
- [Federal Register API Docs](https://www.federalregister.gov/developers/documentation/api/v1)
- [CourtListener API Docs](https://www.courtlistener.com/help/api/rest/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Built with ❤️ for the aiXplain Certificate Program**
