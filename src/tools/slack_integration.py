"""
Slack integration tool for sending policy updates and notifications
"""
import requests
from typing import Dict, Any
import logging
from ..utils.helpers import setup_logger, safe_api_call
from ..config import SLACK_WEBHOOK_URL

logger = setup_logger(__name__)


class SlackIntegration:
    """Send notifications to Slack"""
    
    def __init__(self, webhook_url: str = None):
        """
        Initialize Slack integration
        
        Args:
            webhook_url: Slack incoming webhook URL
        """
        self.webhook_url = webhook_url or SLACK_WEBHOOK_URL
        if not self.webhook_url:
            logger.warning("No Slack webhook URL configured")
        logger.info("SlackIntegration initialized")
    
    @safe_api_call
    def send_notification(
        self,
        title: str,
        content: str,
        source: str = "Policy Navigator Agent",
        url: str = None
    ) -> Dict[str, Any]:
        """
        Send policy update to Slack channel
        
        Args:
            title: Notification title
            content: Notification content
            source: Source of information
            url: Optional URL for more information
        
        Returns:
            Status dictionary
        """
        if not self.webhook_url:
            return {"error": "No Slack webhook URL configured"}
        
        logger.info(f"Sending Slack notification: {title}")
        
        payload = {
            "text": title,
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": title
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": content
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Source:* {source}"
                        }
                    ]
                }
            ]
        }
        
        if url:
            payload["blocks"].append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<{url}|View Details>"
                }
            })
        
        response = requests.post(self.webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        
        return {
            "status": response.status_code,
            "sent": response.ok,
            "message": "Notification sent successfully"
        }
    
    def send_simple_message(self, message: str) -> Dict[str, Any]:
        """
        Send a simple text message to Slack
        
        Args:
            message: Message text
        
        Returns:
            Status dictionary
        """
        if not self.webhook_url:
            return {"error": "No Slack webhook URL configured"}
        
        payload = {"text": message}
        response = requests.post(self.webhook_url, json=payload, timeout=10)
        
        return {
            "status": response.status_code,
            "sent": response.ok
        }
    
    def send_policy_alert(
        self,
        policy_name: str,
        alert_type: str,
        details: str,
        action_required: bool = False
    ) -> Dict[str, Any]:
        """
        Send a policy alert notification
        
        Args:
            policy_name: Name of the policy
            alert_type: Type of alert (e.g., "New", "Updated", "Deadline")
            details: Alert details
            action_required: Whether action is required
        
        Returns:
            Status dictionary
        """
        emoji = "🚨" if action_required else "ℹ️"
        title = f"{emoji} Policy Alert: {policy_name}"
        
        content = f"*Alert Type:* {alert_type}\n\n{details}"
        
        if action_required:
            content += "\n\n⚠️ *Action Required*"
        
        return self.send_notification(
            title=title,
            content=content,
            source="Policy Navigator Agent"
        )


# Function wrappers for agent integration

def send_slack_notification(
    title: str,
    content: str,
    source: str = "Policy Navigator Agent"
) -> Dict[str, Any]:
    """
    Send policy updates to Slack channel
    
    Args:
        title: Notification title
        content: Notification content  
        source: Source attribution
    
    Returns:
        Status dictionary
    """
    slack = SlackIntegration()
    return slack.send_notification(title, content, source)


def notify_policy_update(policy_name: str, update_details: str) -> Dict[str, Any]:
    """
    Send notification about policy update
    
    Args:
        policy_name: Name of updated policy
        update_details: Details of the update
    
    Returns:
        Status dictionary
    """
    slack = SlackIntegration()
    return slack.send_policy_alert(
        policy_name=policy_name,
        alert_type="Policy Update",
        details=update_details,
        action_required=False
    )


# Example usage
if __name__ == "__main__":
    slack = SlackIntegration()
    
    # Test notification
    print("Testing Slack notification...")
    result = slack.send_notification(
        title="Executive Order 14067 Status Update",
        content="Executive Order 14067 is still active as of November 2025. No amendments have been filed.",
        source="Federal Register API",
        url="https://www.federalregister.com/example"
    )
    print(f"Result: {result}")
