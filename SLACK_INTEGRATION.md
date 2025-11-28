# External Tool Integration - Certificate Requirement

## ✅ Requirement Met: Slack Integration

**Requirement:** "The agent should connect with at least one external tool (e.g., Slack, Vercel, Calendar API, Notion) so that users can receive updates, schedule reminders, or take next steps based on the agent's output."

---

## Implementation Overview

### 1. **Slack Tool Integration**

The Policy Navigator Agent is connected to Slack via Incoming Webhooks, enabling automatic notifications to users.

**Location:** `src/tools/slack_integration.py`

**Key Functions:**
```python
def send_slack_notification(title: str, content: str, source: str) -> Dict[str, Any]
def notify_policy_update(policy_name: str, update_details: str) -> Dict[str, Any]
```

### 2. **Agent Configuration**

The Slack tool is registered with the agent during creation:

**File:** `src/agents/create_agents.py` (Lines 190-204)

```python
slack_tool = AgentFactory.create_python_tool(
    name="Slack Notifier",
    description="Send policy updates and alerts to Slack channel...",
    function=send_slack_notification
)
tools.append(slack_tool)
```

### 3. **Automatic Usage**

The agent is instructed to automatically use the Slack tool when:
- Executive orders are repealed, amended, or no longer in effect
- Important compliance deadlines are identified
- Court decisions or legal precedents are found
- Critical policy changes are discovered

**Instructions:** (Lines 234-269 in `create_agents.py`)

---

## How It Works

### User Flow:
1. **User asks a question** via Streamlit UI or CLI
   - Example: "Is Executive Order 14067 still active?"

2. **Agent processes the query:**
   - Searches vector knowledge base
   - Calls Federal Register API tool
   - Analyzes the findings

3. **Agent responds to user** with detailed answer

4. **Agent automatically calls Slack tool** if important information found:
   - Sends notification to configured Slack channel
   - Includes: Title, key details, source, and action items
   - Users in Slack channel receive instant notification

### Example Slack Notification:
```
🔔 Executive Order 14067 Status Update

Executive Order 14067, titled 'Ensuring Responsible Development 
of Digital Assets,' was revoked by executive order issued by 
President Trump on January 23, 2025. 

It is no longer in effect.

Source: Federal Register API
```

---

## Configuration

### Setup (Already Done):
1. ✅ Slack webhook URL configured in `.env`
2. ✅ Tool registered with agent
3. ✅ Agent instructions updated to use tool automatically

### Environment Variable:
```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T0A0BA7RDQE/B0A0GV4LCAG/...
```

---

## Testing

### Automated Test:
```bash
python test_slack.py
```

### Manual Test from UI:
1. Open Streamlit app: http://localhost:8501
2. Sidebar → "📢 Slack Notifications"
3. Enter title and message
4. Click "📨 Send to Slack"

### Test with Agent Query:
```bash
python -m ui.cli query "Is Executive Order 14067 still in effect?"
```

The agent will:
1. Answer the question
2. Automatically send a Slack notification with the findings

---

## Evidence for Certificate Submission

### Screenshots to Include:
1. ✅ Slack channel showing received notifications
2. ✅ Agent logs showing Slack tool usage
3. ✅ Streamlit UI with Slack integration section
4. ✅ Code showing tool registration (`create_agents.py`)
5. ✅ Agent instructions mentioning Slack integration

### Key Files:
- `src/tools/slack_integration.py` - Tool implementation
- `src/agents/create_agents.py` - Tool registration (lines 190-204, 234-269)
- `test_slack.py` - Integration test
- `.env` - Configuration (webhook URL)

---

## Benefits

1. **Real-time Notifications:** Users receive instant updates in Slack
2. **No Polling Required:** Push notifications vs. checking the app
3. **Team Collaboration:** Multiple users can monitor the same channel
4. **Action Items:** Slack messages can include next steps
5. **Audit Trail:** All notifications are logged in Slack history

---

## Alternative Usage

Users can also manually send Slack notifications from the UI for custom alerts about policy changes they're monitoring.

**UI Location:** Sidebar → 📢 Slack Notifications

---

## Conclusion

✅ **External tool requirement fully satisfied** with working Slack integration that:
- Connects to external service (Slack)
- Sends automatic notifications based on agent output
- Enables users to receive updates outside the application
- Provides action items and next steps
- Is configurable and testable

The integration demonstrates practical value by notifying users of critical policy changes in real-time through their preferred communication channel.
