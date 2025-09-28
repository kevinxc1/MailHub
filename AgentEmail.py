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
        """Create or retrieve AgentMail inbox"""
        try:
            # Try to create a new inbox with unique username
            username = f"recruiter-{int(time.time())}"
            inbox = self.agentmail.inboxes.create(
                username=username,
                display_name="AI Recruiter"
            )
            logger.info(f"✅ Created inbox: {inbox.inbox_id}")
            print(f"\n📧 Send applications to: {inbox.inbox_id}")
            return inbox
            
        except Exception as e:
            logger.error(f"Error creating inbox: {e}")
            # Try to get existing inbox
            try:
                inboxes = self.agentmail.inboxes.list()
                if inboxes.inboxes:
                    inbox = inboxes.inboxes[0]
                    logger.info(f"Using existing inbox: {inbox.inbox_id}")
                    return inbox
            except:
                raise Exception("Could not create or get inbox")
    
    def generate_response(self, email: EmailMessage, context: str = "") -> str:
        """Generate AI response using Claude"""
        
        # Get conversation history if it exists
        history = ""
        if email.thread_id and email.thread_id in self.conversations:
            history = f"Previous conversation:\n{self.conversations[email.thread_id]}\n\n"
        
        # Generate response
        response = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[
                {
                    "role": "system",
                    "content": """You are a friendly, professional AI recruiter for a tech startup.
                    
Company: TechCorp (AI/ML startup, remote-first, great culture)
Hiring for: Software Engineers, ML Engineers, Product Managers
Process: Initial screen → Technical interview → Culture fit → Offer

Your personality:
- Warm and enthusiastic with qualified candidates
- Professional but not robotic
- Encourage candidates even when rejecting
- Always provide clear next steps
- Use the candidate's name when you know it

Remember previous conversation context when provided."""
                },
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
    
    def send_email(self, to: str, subject: str, content: str, thread_id: Optional[str] = None) -> bool:
        """Actually send email via AgentMail"""
        try:
            # Send the email
            response = self.agentmail.messages.send(
                inbox_id=self.inbox.inbox_id,
                to=[to],
                subject=subject,
                text=content,
                thread_id=thread_id
            )
            
            logger.info(f"✅ Email sent to {to}")
            
            # Store in conversation history
            if thread_id:
                if thread_id not in self.conversations:
                    self.conversations[thread_id] = ""
                self.conversations[thread_id] += f"\nOur response:\n{content}\n"
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send email: {e}")
            return False
    
    def categorize_email(self, email: EmailMessage) -> str:
        """Categorize the type of email"""
        
        response = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=50,
            messages=[
                {
                    "role": "system",
                    "content": """Categorize this email into ONE of these categories:
                    - new_application (someone applying for a job)
                    - scheduling_response (candidate providing availability)
                    - interviewer_feedback (interviewer responding about a candidate)
                    - question (candidate asking questions)
                    - follow_up (candidate following up on application)
                    - other
                    
                    Respond with just the category name."""
                },
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
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[
                {
                    "role": "system",
                    "content": """Evaluate this job application. Return a JSON response with:
                    - score (1-10): How qualified is this candidate?
                    - qualified (boolean): Should we move forward?
                    - missing_skills (list): What key skills are missing?
                    - strengths (list): What are their strengths?
                    - next_step (string): What should we do next?
                    - reasoning (string): Brief explanation"""
                },
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
        except:
            return {
                "score": 5,
                "qualified": True,
                "reasoning": "Could not parse evaluation",
                "next_step": "schedule_screen"
            }
    
    def process_new_application(self, email: EmailMessage):
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
            to=email.from_email,
            subject=f"Re: {email.subject}" if not email.subject.startswith("Re:") else email.subject,
            content=response_content,
            thread_id=email.thread_id
        )
        
        # If qualified, notify interviewer
        if evaluation["qualified"]:
            self.send_email(
                to=self.interviewer_email,
                subject=f"New Qualified Candidate: {email.from_email}",
                content=f"""New candidate scored {evaluation['score']}/10:

From: {email.from_email}
Strengths: {', '.join(evaluation.get('strengths', []))}

Application:
{email.content[:500]}...

They will be scheduling a screening call soon."""
            )
    
    def process_scheduling_response(self, email: EmailMessage):
        """Handle scheduling responses from candidates"""
        
        # Extract availability
        response = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
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
            to=self.interviewer_email,
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
            to=email.from_email,
            subject=f"Re: {email.subject}",
            content=response_content,
            thread_id=email.thread_id
        )
        
        # Update candidate state
        if email.from_email in self.candidates:
            self.candidates[email.from_email].status = "scheduling"
    
    def process_email(self, message):
        """Main email processing logic"""
        
        # Skip if already processed
        if message.id in self.processed_emails:
            return
        
        # Mark as processed
        self.processed_emails.add(message.id)
        
        # Create EmailMessage object
        email = EmailMessage(
            id=message.id,
            from_email=message.from_email,
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
            self.process_new_application(email)
        elif category == "scheduling_response":
            self.process_scheduling_response(email)
        elif email.from_email == self.interviewer_email:
            # Handle interviewer responses
            self.handle_interviewer_response(email)
        else:
            # General response for questions, follow-ups, etc.
            response_content = self.generate_response(email)
            self.send_email(
                to=email.from_email,
                subject=f"Re: {email.subject}",
                content=response_content,
                thread_id=email.thread_id
            )
    
    def handle_interviewer_response(self, email: EmailMessage):
        """Handle responses from interviewer"""
        # This is simplified - in production you'd parse the response
        # and forward confirmation to the right candidate
        logger.info(f"Interviewer responded: {email.subject}")
    
    def run(self):
        """Main loop"""
        print(f"\n🚀 MailHub Agent running!")
        print(f"📧 Inbox: {self.inbox.inbox_id}")
        print(f"⏰ Checking for emails every 10 seconds...")
        print(f"\nPress Ctrl+C to stop\n")
        
        while True:
            try:
                # Get messages
                messages = self.agentmail.messages.list(
                    inbox_id=self.inbox.inbox_id,
                    limit=20
                )
                
                # Process each message
                for message in messages.messages:
                    self.process_email(message)
                
                # Wait before next check
                time.sleep(10)
                
            except KeyboardInterrupt:
                print("\n👋 Shutting down...")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(30)

def main():
    """Entry point"""
    
    # Check for required environment variables
    if not os.getenv("AGENTMAIL_API_KEY"):
        print("❌ Error: AGENTMAIL_API_KEY not set in .env file")
        return
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY not set in .env file")
        return
    
    # Create and run agent
    agent = MailHubAgent()
    agent.run()

if __name__ == "__main__":
    main()