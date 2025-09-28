#!/usr/bin/env python3
"""
MailHub - Recruiter Agent for Interview Coordination
Handles back and forth conversations with applicants and coordinates interviews.
"""

import os
import time
import logging
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

from dotenv import load_dotenv
from agentmail import AgentMail
from agentmail.core.api_error import ApiError
from anthropic import Anthropic

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EmailCategory(Enum):
    """Email categorization types"""
    RECEIVE_TIMES_FROM_APPLICANT = "Receive times from applicant"
    RECEIVES_CONFIRMATION_FROM_INTERVIEWER = "Receives confirmation from Interviewer"
    RECEIVES_DENIAL_FROM_INTERVIEWER = "Receives denial from Interviewer"
    RECEIVES_QUESTION_FROM_APPLICANT = "Receives question from applicant"
    RECEIVES_SPAM = "Receives Spam"

@dataclass
class EmailMessage:
    """Email message structure"""
    id: str
    from_email: str
    to_email: str
    subject: str
    content: str
    thread_id: Optional[str] = None

@dataclass
class InterviewState:
    """Track interview coordination state"""
    applicant_email: str
    status: str  # "waiting_for_times", "waiting_for_interviewer_response", "confirmed", "denied"
    proposed_times: Optional[List[str]] = None
    selected_time: Optional[str] = None

class MailHubAgent:
    """Main MailHub agent for handling recruitment emails"""
    
    def __init__(self, agentmail_api_key: str, anthropic_api_key: str):
        """Initialize the MailHub agent"""
        self.agentmail_client = AgentMail(api_key=agentmail_api_key)
        self.anthropic_client = Anthropic(api_key=anthropic_api_key)
        self.interviewer_email = "lijackie@umich.edu"
        self.interview_states: Dict[str, InterviewState] = {}
        
        # Create or get the inbox for receiving emails
        self.inbox = self.create_or_get_inbox()
        
        logger.info("MailHub Agent initialized")
    
    def create_or_get_inbox(self):
        """Create or get the AgentMail inbox for receiving emails"""
        try:
            # Try to list existing inboxes first
            inboxes_response = self.agentmail_client.inboxes.list()
            
            # Look for an existing inbox with our domain
            for inbox in inboxes_response.inboxes:
                if "mailhub" in inbox.inbox_id.lower():
                    logger.info(f"Found existing inbox: {inbox.inbox_id}")
                    return inbox
            
            # Create a new inbox if none found
            logger.info("Creating new AgentMail inbox...")
            new_inbox = self.agentmail_client.inboxes.create(
                username="mailhub",
                display_name="MailHub Recruiter Agent"
            )
            logger.info(f"Created new inbox: {new_inbox.inbox_id}")
            return new_inbox
            
        except Exception as e:
            logger.error(f"Error creating/getting inbox: {e}")
            # Return a placeholder if we can't create/get inbox
            return None
    
    def categorize_email(self, email_content: str, sender: str) -> EmailCategory:
        """Use Claude 3.5 to categorize incoming emails"""
        try:
            prompt = f"""
            Analyze this email and categorize it into one of these categories:
            1. "Receive times from applicant" - Email contains available interview times/dates from an applicant
            2. "Receives confirmation from Interviewer" - Email contains confirmation/approval from interviewer
            3. "Receives denial from Interviewer" - Email contains rejection/denial from interviewer
            4. "Receives question from applicant" - Email contains questions from an applicant
            5. "Receives Spam" - Email is spam or irrelevant
            
            Email from: {sender}
            Email content: {email_content}
            
            Respond with ONLY the category name from the list above.
            """
            
            response = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=50,
                messages=[{"role": "user", "content": prompt}]
            )
            
            category_text = response.content[0].text.strip()
            
            # Map response to enum
            for category in EmailCategory:
                if category.value.lower() in category_text.lower():
                    logger.info(f"Email categorized as: {category.value}")
                    return category
            
            # Default to spam if no match
            logger.warning(f"Could not categorize email, defaulting to spam. Response: {category_text}")
            return EmailCategory.RECEIVES_SPAM
            
        except Exception as e:
            logger.error(f"Error categorizing email: {e}")
            return EmailCategory.RECEIVES_SPAM
    
    def send_email(self, to_email: str, subject: str, content: str, thread_id: Optional[str] = None) -> bool:
        """Send email using AgentMail"""
        try:
            logger.info(f"Sending email to {to_email}: {subject}")
            logger.info(f"Content: {content}")
            
            # Create a draft first
            draft_data = {
                "to": [to_email],
                "subject": subject,
                "text": content
            }
            
            # For now, we'll log the email content since we need to understand
            # the exact AgentMail API for sending emails
            logger.info(f"Would send email with data: {draft_data}")
            
            # TODO: Implement actual AgentMail send functionality
            # This requires understanding the exact API for sending emails
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def get_new_emails(self) -> List[EmailMessage]:
        """Poll for new emails from AgentMail"""
        try:
            if not self.inbox:
                logger.error("No inbox available for receiving emails")
                return []
            
            logger.info(f"Polling for new emails in inbox: {self.inbox.inbox_id}")
            
            # Get threads (conversations) from AgentMail
            threads_response = self.agentmail_client.threads.list(limit=10)
            
            emails = []
            for thread in threads_response.threads:
                # Get the latest message from each thread
                thread_details = self.agentmail_client.threads.get(thread.thread_id)
                
                # Convert thread to EmailMessage
                email = EmailMessage(
                    id=thread.thread_id,
                    from_email=thread.senders[0] if thread.senders else "unknown",
                    to_email=self.inbox.inbox_id,  # Our AgentMail inbox
                    subject=thread.subject or "No Subject",
                    content=thread.preview or "",
                    thread_id=thread.thread_id
                )
                emails.append(email)
            
            return emails
            
        except Exception as e:
            logger.error(f"Error retrieving emails: {e}")
            return []
    
    def handle_interview_coordination(self, email: EmailMessage) -> None:
        """Handle interview coordination workflow"""
        applicant_email = email.from_email
        
        if applicant_email not in self.interview_states:
            # New applicant - start interview process
            self.interview_states[applicant_email] = InterviewState(
                applicant_email=applicant_email,
                status="waiting_for_times"
            )
            
            # Send initial email to applicant requesting available times
            self.send_email(
                to_email=applicant_email,
                subject="Interview Coordination - Available Times",
                content="test email for coordinating interviews"
            )
            logger.info(f"Started interview process for {applicant_email}")
    
    def handle_question_from_applicant(self, email: EmailMessage) -> None:
        """Handle questions from applicants"""
        # Send automated response
        self.send_email(
            to_email=email.from_email,
            subject="Re: " + email.subject,
            content="test email to applicant for back and forth conversation",
            thread_id=email.thread_id
        )
        logger.info(f"Responded to question from {email.from_email}")
    
    def process_email(self, email: EmailMessage) -> None:
        """Process incoming email based on category"""
        category = self.categorize_email(email.content, email.from_email)
        
        if category == EmailCategory.RECEIVE_TIMES_FROM_APPLICANT:
            # Forward times to interviewer
            self.send_email(
                to_email=self.interviewer_email,
                subject=f"Interview Times from {email.from_email}",
                content=f"Applicant {email.from_email} has provided the following available times:\n\n{email.content}"
            )
            
            # Update state
            if email.from_email in self.interview_states:
                self.interview_states[email.from_email].status = "waiting_for_interviewer_response"
                self.interview_states[email.from_email].proposed_times = [email.content]
            
            logger.info(f"Forwarded times from {email.from_email} to interviewer")
        
        elif category == EmailCategory.RECEIVES_CONFIRMATION_FROM_INTERVIEWER:
            # Interviewer confirmed - notify applicant
            # Extract applicant email from the email content or use a different method
            # For now, we'll need to implement a way to track which applicant this is for
            
            # Send confirmation to applicant
            self.send_email(
                to_email=email.from_email,  # This might need to be the applicant's email
                subject="Interview Confirmed",
                content="test email for coordinating interviews"
            )
            logger.info("Sent interview confirmation to applicant")
        
        elif category == EmailCategory.RECEIVES_DENIAL_FROM_INTERVIEWER:
            # Interviewer denied - ask applicant for new times
            # Similar to confirmation, we need to identify the applicant
            
            self.send_email(
                to_email=email.from_email,  # This might need to be the applicant's email
                subject="Interview Times - Please Provide Alternatives",
                content="test email for coordinating interviews"
            )
            logger.info("Requested new times from applicant")
        
        elif category == EmailCategory.RECEIVES_QUESTION_FROM_APPLICANT:
            self.handle_question_from_applicant(email)
        
        elif category == EmailCategory.RECEIVES_SPAM:
            logger.info(f"Ignoring spam email from {email.from_email}")
    
    def run(self) -> None:
        """Main application loop"""
        logger.info("Starting MailHub Agent...")
        
        while True:
            try:
                # Poll for new emails
                new_emails = self.get_new_emails()
                
                for email in new_emails:
                    logger.info(f"Processing email from {email.from_email}")
                    self.process_email(email)
                
                # Wait before next poll
                time.sleep(30)  # Poll every 30 seconds
                
            except KeyboardInterrupt:
                logger.info("Shutting down MailHub Agent...")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(60)  # Wait longer on error

def main():
    """Main entry point"""
    # Get API keys from environment variables
    agentmail_api_key = os.getenv("AGENTMAIL_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not agentmail_api_key:
        logger.error("AGENTMAIL_API_KEY environment variable not set")
        return
    
    if not anthropic_api_key:
        logger.error("ANTHROPIC_API_KEY environment variable not set")
        return
    
    # Create and run the agent
    agent = MailHubAgent(agentmail_api_key, anthropic_api_key)
    
    # Print the inbox information for Gmail forwarding setup
    if agent.inbox:
        print(f"\n📧 AgentMail Inbox Created: {agent.inbox.inbox_id}")
        print(f"\n📋 To set up Gmail forwarding from MailHub6767@gmail.com:")
        print(f"   1. Go to Gmail settings for MailHub6767@gmail.com")
        print(f"   2. Go to 'Forwarding and POP/IMAP'")
        print(f"   3. Add forwarding address: {agent.inbox.inbox_id}")
        print(f"   4. Verify the forwarding address")
        print(f"   5. Select 'Forward a copy of incoming mail to'")
        print(f"   6. Choose 'Keep Gmail's copy in the Inbox'")
        print(f"   7. Save changes")
        print(f"\n🚀 Starting MailHub Agent...")
    else:
        print("❌ Failed to create AgentMail inbox. Check your API key and try again.")
        return
    
    agent.run()

if __name__ == "__main__":
    main()