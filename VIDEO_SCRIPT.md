# 🎥 Demo Video Script (2-3 minutes)

## Certificate Project: Policy Navigator Agent

### Opening (15 seconds)
**[Screen: GitHub README]**

"Hi! This is my Policy Navigator Agent - a Multi-Agent RAG system built with aiXplain Agentic OS for the certificate program."

"This agent helps users query government regulations and policies using natural language, with real-time verification and automated notifications."

### Architecture Overview (20 seconds)
**[Screen: Architecture diagram in README]**

"The system uses a vector index with aiR embeddings for semantic search, integrated with multiple external APIs and a Slack notification system."

"Let me show you the certificate requirements we've met:"

**[Screen: Certificate checklist]**
- ✅ RAG pipeline with vector index
- ✅ Two data sources: CSV dataset and web scraping
- ✅ Three types of tools: Custom APIs, marketplace tool, and Slack integration
- ✅ Streamlit UI for interaction

### Live Demo (90 seconds)

#### Part 1: Basic Query (20 seconds)
**[Screen: Streamlit UI]**

"Let's start with a basic query using the vector index."

**[Type query]**: "What are the EPA clean air compliance requirements?"

**[Show response appearing]**

"The agent searches the policy knowledge base and returns relevant information with source citations."

#### Part 2: Real-time API Call (30 seconds)
**[Screen: Streamlit UI]**

"Now let's test the external API integration with a real-time verification."

**[Type query]**: "Is Executive Order 14067 still in effect?"

**[Show processing]**

"Watch as the agent:"
1. Searches the knowledge base
2. Calls the Federal Register API
3. Finds the executive order was revoked
4. Returns the answer

**[Show response]**

"Executive Order 14067 was revoked on January 23, 2025."

#### Part 3: Slack Notification (20 seconds)
**[Screen: Split view - Streamlit + Slack]**

"Because this is a policy change, the agent automatically sent a Slack notification."

**[Show Slack channel]**

"Here's the formatted alert with the revocation details - fulfilling our external tool integration requirement."

#### Part 4: Multi-turn Conversation (20 seconds)
**[Screen: Streamlit UI]**

"The agent maintains context for follow-up questions."

**[Type first query]**: "What are OSHA workplace safety requirements?"

**[Show response]**

**[Type follow-up]**: "What are the penalties for non-compliance?"

**[Show response]**

"Notice it understood the context from the previous question."

### Technical Highlights (20 seconds)
**[Screen: Code editor - tools directory]**

"Under the hood, we have:"
- Custom Python tools for Federal Register and CourtListener APIs
- Vector index with 15+ policy documents
- Data from CSV dataset and EPA web scraping
- Slack integration via Composio

### Closing (15 seconds)
**[Screen: GitHub README]**

"All code is on GitHub with comprehensive documentation including setup guides, API integration details, and future improvement suggestions."

"The repository includes everything needed to run this project, from the Streamlit UI to the agent configuration scripts."

**[Screen: Contact section]**

"Thanks for watching! Check out the repository for full details and setup instructions."

---

## 🎬 Recording Tips

### Before Recording:
1. ✅ Close unnecessary browser tabs and applications
2. ✅ Clear Streamlit UI of previous queries
3. ✅ Have Slack channel open in another window
4. ✅ Test all queries work correctly
5. ✅ Check audio levels
6. ✅ Use clean desktop background

### Screen Recording Tools:
- **Windows**: OBS Studio, Loom, or built-in Xbox Game Bar (Win+G)
- **Mac**: QuickTime, Loom, or Screenshot tool
- **Cross-platform**: Loom (easiest), OBS Studio (most features)

### Recording Settings:
- **Resolution**: 1920x1080 or 1280x720
- **Frame rate**: 30 fps
- **Audio**: Clear microphone, no background noise
- **Duration**: 2-3 minutes (aim for 2:30)

### During Recording:
- Speak clearly and at a moderate pace
- Use mouse cursor to highlight important parts
- Pause briefly between sections
- Show results waiting to load (builds anticipation)
- Stay enthusiastic but professional

### After Recording:
1. Review the video
2. Check audio quality
3. Trim any dead space
4. Add captions if possible (YouTube auto-captions work)
5. Upload to YouTube as "Unlisted" or public
6. Add link to README.md

### Video Title:
"Policy Navigator Agent - Multi-Agent RAG System | aiXplain Certificate Project"

### Video Description Template:
```
Policy Navigator Agent - Certificate Project for aiXplain Agentic OS

This demo showcases a Multi-Agent RAG system for government regulation search, featuring:
• Vector index with semantic search
• Real-time API integration (Federal Register, CourtListener)
• Automated Slack notifications
• Multi-turn conversations
• Streamlit UI

Built with:
- aiXplain Agentic OS SDK
- Python 3.8+
- Streamlit
- Multiple data sources (CSV + web scraping)

GitHub: [YOUR_REPO_LINK]
Documentation: See README.md for setup instructions

Certificate Requirements:
✅ RAG Pipeline
✅ Multiple data sources
✅ 3+ tool types
✅ UI implementation
✅ Comprehensive documentation

Timestamp:
0:00 - Introduction
0:15 - Architecture overview
0:35 - Live demo start
0:55 - External API call
1:15 - Slack notification
1:35 - Multi-turn conversation
1:55 - Technical highlights
2:10 - Closing & repository

#aiXplain #AgenticOS #RAG #AI #PolicyTech #MachineLearning
```

---

## 📝 Post-Recording Checklist

- [ ] Video recorded (2-3 minutes)
- [ ] Audio is clear
- [ ] All features demonstrated
- [ ] No sensitive information visible (API keys, etc.)
- [ ] Video uploaded to YouTube/Loom
- [ ] Link added to README.md
- [ ] Video set to Unlisted or Public
- [ ] Description includes GitHub link

---

## 🎯 Key Points to Emphasize

1. **Certificate Requirements Met**: Show checklist clearly
2. **Multiple Data Sources**: Mention CSV dataset + web scraping
3. **Three Tool Types**: Custom APIs + Marketplace + Slack
4. **Real-time Verification**: External API call is important
5. **External Tool Integration**: Slack notification is the key requirement
6. **Professional UI**: Streamlit interface is polished
7. **Documentation**: Comprehensive README and guides

---

## Alternative: Quick Demo (90 seconds)

If short on time, focus on:
1. Project introduction (10s)
2. One query showing vector search (20s)
3. External API call + Slack notification (30s)
4. Show GitHub README with requirements checklist (20s)
5. Closing (10s)

---

**Remember**: The goal is to demonstrate that all certificate requirements are met while showing the agent working smoothly!
