#!/usr/bin/env python3
"""
MailHub - AI Recruitment Agent with AgentMail
Fixed version with proper email sending and AI responses
"""

import os
import time
import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

from dotenv import load_dotenv
from agentmail import AgentMail
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class EmailMessage:
    """Email message structure"""
    id: str
    from_email: str
    subject: str
    content: str
    thread_id: Optional[str] = None
    timestamp: Optional[datetime] = None

@dataclass
class CandidateState:
    """Track candidate through recruitment process"""
    email: str
    status: str  # "new", "screening", "scheduling", "interviewed", "rejected", "hired"
    thread_id: str
    notes: str = ""
    score: Optional[int] = None

class MailHubAgent:
    """AI Recruitment Agent using AgentMail and Claude"""
    
    def __init__(self):
        """Initialize the recruitment agent"""
        # API clients
        self.agentmail = AgentMail(api_key=os.getenv("AGENTMAIL_API_KEY"))
        self.claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Configuration
        self.interviewer_email = os.getenv("INTERVIEWER_EMAIL", "interviewer@company.com")
        
        # State tracking
        self.processed_emails = set()
        self.candidates = {}  # email -> CandidateState
        self.conversations = {}  # thread_id -> conversation history
        
        # Create or get inbox
        self.inbox = self.setup_inbox()
        
    def setup_inbox(self):
        """Use the existing mailhub@agentmail.to inbox instead of creating new ones"""
        try:
            # Try to find existing mailhub inbox
            inboxes_response = self.agentmail.inboxes.list()
            
            for inbox in inboxes_response.inboxes:
                if "mailhub" in inbox.inbox_id.lower():
                    logger.info(f"✅ Using existing inbox: {inbox.inbox_id}")
                    print(f"\n📧 Send applications to: {inbox.inbox_id}")
                    return inbox
            
            # If not found, use a simple object with the known address
            class ExistingInbox:
                def __init__(self):
                    self.inbox_id = "mailhub@agentmail.to"
                    self.created_at = None
            
            logger.info("✅ Using mailhub@agentmail.to")
            print(f"\n📧 Send applications to: mailhub@agentmail.to")
            return ExistingInbox()
            
        except Exception as e:
            logger.warning(f"Could not list inboxes: {e}")
            # Fallback to known address
            class ExistingInbox:
                def __init__(self):
                    self.inbox_id = "mailhub@agentmail.to"
            
            logger.info("✅ Using mailhub@agentmail.to (fallback)")
            print(f"\n📧 Send applications to: mailhub@agentmail.to")
            return ExistingInbox()
    
    def generate_response(self, email: EmailMessage, context: str = "") -> str:
        """Generate AI response using Claude"""
        
        # Get conversation history if it exists
        history = ""
        if email.thread_id and email.thread_id in self.conversations:
            history = f"Previous conversation:\n{self.conversations[email.thread_id]}\n\n"
        
        # Generate response
        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            system="""You are a friendly, professional AI recruiter for a tech startup.
                    
Company: TechCorp (AI/ML startup, remote-first, great culture)
Hiring for: Software Engineers, ML Engineers, Product Managers
Process: Initial screen → Technical interview → Culture fit → Offer

Your personality:
- Warm and enthusiastic with qualified candidates
- Professional but not robotic
- Encourage candidates even when rejecting
- Always provide clear next steps
- Use the candidate's name when you know it

Remember previous conversation context when provided.""",
            messages=[
                {
                    "role": "user",
                    "content": f"""{history}{context}

Email from: {email.from_email}
Subject: {email.subject}
Content: {email.content}

Write a response email that's helpful and professional."""
                }
            ]
        )
        
        return response.content[0].text
    
    def send_email(self, to_email: str, subject: str, content: str, message_id: Optional[str] = None, thread_id: Optional[str] = None) -> bool:
        """Send email via AgentMail - uses reply API when message_id provided"""
        try:
            if message_id:
                # Use reply to maintain thread
                response = self.agentmail.inboxes.messages.reply(
                    inbox_id=self.inbox.inbox_id,
                    message_id=message_id,
                    text=content
                )
                logger.info(f"✅ Replied to message {message_id}")
                logger.debug(f"Reply response: {response}")
            else:
                # Fallback: try to create new message (may not work for outbound)
                logger.warning("No message_id - attempting to create new message")
                try:
                    response = self.agentmail.inboxes.messages.send(
                        inbox_id=self.inbox.inbox_id,
                        to=[to_email],
                        subject=subject,
                        text=content
                    )
                    logger.info(f"✅ Sent new message to {to_email}")
                except Exception as send_error:
                    logger.error(f"❌ Send failed: {send_error}")
                    logger.info(f"📧 Would send: {content[:100]}...")
                    return False
            
            # Store in conversation history
            conversation_key = thread_id or message_id or to_email
            if conversation_key:
                if conversation_key not in self.conversations:
                    self.conversations[conversation_key] = ""
                self.conversations[conversation_key] += f"\nOur response:\n{content}\n"
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send email: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            return False
    
    def categorize_email(self, email: EmailMessage) -> str:
        """Categorize the type of email"""
        
        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=50,
            system="""Categorize this email into ONE of these categories:
                    - new_application (someone applying for a job)
                    - scheduling_response (candidate providing availability)
                    - interviewer_feedback (interviewer responding about a candidate)
                    - question (candidate asking questions)
                    - follow_up (candidate following up on application)
                    - other
                    
                    Respond with just the category name.""",
            messages=[
                {
                    "role": "user",
                    "content": email.content
                }
            ]
        )
        
        category = response.content[0].text.strip().lower()
        logger.info(f"📂 Email categorized as: {category}")
        return category
    
    def evaluate_candidate(self, email: EmailMessage) -> Dict:
        """Evaluate a candidate application"""
        
        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            system="""Evaluate this job application. Return a JSON response with:
                    - score (1-10): How qualified is this candidate?
                    - qualified (boolean): Should we move forward?
                    - missing_skills (list): What key skills are missing?
                    - strengths (list): What are their strengths?
                    - next_step (string): What should we do next?
                    - reasoning (string): Brief explanation""",
            messages=[
                {
                    "role": "user",
                    "content": f"Application email:\n{email.content}"
                }
            ]
        )
        
        try:
            evaluation = json.loads(response.content[0].text)
            logger.info(f"📊 Candidate scored: {evaluation.get('score', 'N/A')}/10")
            return evaluation
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse evaluation JSON: {e}")
            logger.error(f"Raw response: {response.content[0].text}")
            return {
                "score": 5,
                "qualified": True,
                "reasoning": "Could not parse evaluation - using default scoring",
                "next_step": "schedule_screen"
            }
        except Exception as e:
            logger.error(f"Error during candidate evaluation: {e}")
            return {
                "score": 3,
                "qualified": False,
                "reasoning": f"Evaluation failed: {str(e)}",
                "next_step": "reject"
            }
    
    def process_new_application(self, email: EmailMessage, message_id: str):
        """Handle new job application"""
        
        # Evaluate candidate
        evaluation = self.evaluate_candidate(email)
        
        # Store candidate state
        self.candidates[email.from_email] = CandidateState(
            email=email.from_email,
            status="screening" if evaluation["qualified"] else "rejected",
            thread_id=email.thread_id or email.id,
            score=evaluation.get("score", 0),
            notes=evaluation.get("reasoning", "")
        )
        
        # Generate appropriate response
        if evaluation["qualified"]:
            context = f"""This candidate scored {evaluation['score']}/10.
            Strengths: {evaluation.get('strengths', [])}
            Be enthusiastic and invite them to schedule a screening call.
            Ask for their availability in the next week."""
        else:
            context = f"""This candidate isn't a fit right now.
            Missing: {evaluation.get('missing_skills', [])}
            Be encouraging and suggest they apply again in the future after gaining more experience."""
        
        response_content = self.generate_response(email, context)
        
        # Send response
        self.send_email(
            to_email=email.from_email,
            subject=f"Re: {email.subject}" if not email.subject.startswith("Re:") else email.subject,
            content=response_content,
            message_id=message_id,
            thread_id=email.thread_id
        )
        
        # If qualified, notify interviewer
        if evaluation["qualified"]:
            self.send_email(
                to_email=self.interviewer_email,
                subject=f"New Qualified Candidate: {email.from_email}",
                content=f"""New candidate scored {evaluation['score']}/10:

From: {email.from_email}
Strengths: {', '.join(evaluation.get('strengths', []))}

Application:
{email.content[:500]}...

They will be scheduling a screening call soon."""
            )
    
    def process_scheduling_response(self, email: EmailMessage, message_id: str):
        """Handle scheduling responses from candidates"""
        
        # Extract availability
        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": f"Extract the available times from this email:\n{email.content}\nList them clearly."
                }
            ]
        )
        
        availability = response.content[0].text
        
        # Forward to interviewer
        self.send_email(
            to_email=self.interviewer_email,
            subject=f"Interview Availability: {email.from_email}",
            content=f"""Candidate has provided availability:

{availability}

Original message:
{email.content}

Please reply with your preferred time."""
        )
        
        # Acknowledge to candidate
        response_content = self.generate_response(
            email,
            "Thank them for the availability and let them know we'll confirm a time within 24 hours."
        )
        
        self.send_email(
            to_email=email.from_email,
            subject=f"Re: {email.subject}",
            content=response_content,
            message_id=message_id,
            thread_id=email.thread_id
        )
        
        # Update candidate state
        if email.from_email in self.candidates:
            self.candidates[email.from_email].status = "scheduling"
    
    def process_email(self, message):
        """Main email processing logic"""
        
        # Skip if already processed
        if message.message_id in self.processed_emails:
            return
        
        # Mark as processed
        self.processed_emails.add(message.message_id)
        
        # Create EmailMessage object
        email = EmailMessage(
            id=message.message_id,
            from_email=getattr(message, 'from_', ''),
            subject=message.subject or "No Subject",
            content=message.text or "",
            thread_id=getattr(message, 'thread_id', None)
        )
        
        logger.info(f"📨 Processing email from: {email.from_email}")
        
        # Store in conversation history
        if email.thread_id:
            if email.thread_id not in self.conversations:
                self.conversations[email.thread_id] = ""
            self.conversations[email.thread_id] += f"\nFrom {email.from_email}:\n{email.content}\n"
        
        # Categorize and route email
        category = self.categorize_email(email)
        
        if category == "new_application":
            self.process_new_application(email, message.message_id)
        elif category == "scheduling_response":
            self.process_scheduling_response(email, message.message_id)
        elif email.from_email == self.interviewer_email:
            # Handle interviewer responses
            self.handle_interviewer_response(email, message.message_id)
        else:
            # General response for questions, follow-ups, etc.
            response_content = self.generate_response(email)
            self.send_email(
                to_email=email.from_email,
                subject=f"Re: {email.subject}",
                content=response_content,
                message_id=message.message_id,
                thread_id=email.thread_id
            )
    
    def handle_interviewer_response(self, email: EmailMessage, message_id: str):
        """Handle responses from interviewer"""
        # This is simplified - in production you'd parse the response
        # and forward confirmation to the right candidate
        logger.info(f"Interviewer responded: {email.subject}")
    
    def run(self):
        """Main loop"""
        print(f"\n🚀 MailHub Agent running!")
        print(f"📧 Inbox: {self.inbox.inbox_id}")
        print(f"⏰ Checking for emails every 10 seconds...")
        print(f"📊 Current candidates: {len(self.candidates)}")
        print(f"🗂️  Processed emails: {len(self.processed_emails)}")
        print(f"\nPress Ctrl+C to stop\n")
        
        while True:
            try:
                # Get messages using correct API structure
                # Note: Using inboxes.messages.list() as per AgentMail API documentation
                messages = self.agentmail.inboxes.messages.list(
                    inbox_id=self.inbox.inbox_id,
                    limit=20
                )
                
                logger.info(f"📥 Found {len(messages.messages)} messages")
                
                # Process each message
                new_messages = 0
                for message in messages.messages:
                    if message.message_id not in self.processed_emails:
                        new_messages += 1
                    self.process_email(message)
                
                if new_messages > 0:
                    logger.info(f"✅ Processed {new_messages} new messages")
                    print(f"📊 Stats - Candidates: {len(self.candidates)} | Processed: {len(self.processed_emails)}")
                
                # Wait before next check
                time.sleep(10)
                
            except KeyboardInterrupt:
                print("\n👋 Shutting down...")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                logger.error(f"Error type: {type(e).__name__}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                print(f"❌ Error occurred: {e}")
                print("Waiting 30 seconds before retrying...")
                time.sleep(30)

def test_claude_model():
    """Quick test to verify Claude model works"""
    try:
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=10,
            system="You are a helpful assistant.",
            messages=[{"role": "user", "content": "test"}]
        )
        print("✅ Claude model claude-sonnet-4-20250514 is working!")
        return True
    except Exception as e:
        print(f"❌ Claude model failed: {e}")
        return False

def main():
    """Entry point"""
    
    # Check for required environment variables
    if not os.getenv("AGENTMAIL_API_KEY"):
        print("❌ Error: AGENTMAIL_API_KEY not set in .env file")
        return
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY not set in .env file")
        return
    
    # Test Claude model first
    print("🧪 Testing Claude model...")
    if not test_claude_model():
        print("❌ Cannot start agent - Claude model not working")
        return
    
    # Create and run agent
    agent = MailHubAgent()
    agent.run()

if __name__ == "__main__":
    main()