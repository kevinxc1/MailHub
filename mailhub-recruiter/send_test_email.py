#!/usr/bin/env python3
"""
Send test emails to the AgentEmail recruitment agent
For manual testing of the full email flow
"""

import os
import sys
import time
from dotenv import load_dotenv
from agentmail import AgentMail

# Load environment variables
load_dotenv()

class TestEmailSender:
    """Send test emails to recruitment agent"""
    
    def __init__(self, target_inbox: str):
        """Initialize with target inbox email"""
        self.agentmail = AgentMail(api_key=os.getenv("AGENTMAIL_API_KEY"))
        self.target_inbox = target_inbox
        
        # Create our own sender inbox
        self.sender_inbox = self.create_sender_inbox()
    
    def create_sender_inbox(self):
        """Create inbox for sending test emails"""
        try:
            username = f"test-sender-{int(time.time())}"
            inbox = self.agentmail.inboxes.create(
                username=username,
                display_name="Test Candidate"
            )
            print(f"✅ Created sender inbox: {inbox.inbox_id}")
            return inbox
        except Exception as e:
            print(f"❌ Failed to create sender inbox: {e}")
            sys.exit(1)
    
    def send_job_application(self, candidate_type: str = "strong"):
        """Send a job application email"""
        
        applications = {
            "strong": {
                "subject": "Application for Senior ML Engineer Position",
                "content": """Dear Hiring Manager,

I am writing to express my strong interest in the Senior ML Engineer position at TechCorp.

My Background:
• 7 years of machine learning experience at Meta and Netflix
• Led ML teams that built recommendation systems for 50M+ users
• Expert in Python, TensorFlow, PyTorch, Spark, and AWS
• MS in Computer Science from Stanford
• Published 12 papers in top ML conferences (NeurIPS, ICML)

Key Achievements:
• Improved recommendation CTR by 35% at Netflix
• Built real-time fraud detection system processing 1M+ transactions/day
• Led cross-functional team of 15 engineers and data scientists
• Reduced model training time by 60% through distributed computing

I'm excited about TechCorp's mission to democratize AI and would love to contribute to your cutting-edge ML infrastructure.

I'm available for interviews next week and can start immediately.

Best regards,
Alex Chen
alex.chen.ml@gmail.com
LinkedIn: linkedin.com/in/alexchen-ml
GitHub: github.com/alexchen-ml

P.S. I've attached my resume and portfolio of recent ML projects."""
            },
            
            "medium": {
                "subject": "Software Engineer Application",
                "content": """Hi there,

I saw your job posting for a software engineer role and I'm interested in applying.

About me:
- 3 years experience with Python and JavaScript
- Worked at a startup doing web development
- Bachelor's degree in Computer Science
- Know some machine learning from online courses

I'm a quick learner and excited about working at a tech company. Let me know if you'd like to chat!

Thanks,
Jordan Smith
jordan.smith@email.com"""
            },
            
            "weak": {
                "subject": "Job Application",
                "content": """hello,

i want to apply for the job. i don't have much experience but i'm willing to learn. i know some python from youtube videos and built a simple website once.

please let me know if you're interested.

thanks
mike"""
            }
        }
        
        if candidate_type not in applications:
            print(f"❌ Unknown candidate type: {candidate_type}")
            return False
        
        app = applications[candidate_type]
        
        try:
            # Send email using AgentMail
            response = self.agentmail.inboxes.messages.create(
                inbox_id=self.sender_inbox.inbox_id,
                to=[self.target_inbox],
                subject=app["subject"],
                text=app["content"]
            )
            
            print(f"✅ Sent {candidate_type} candidate application")
            print(f"📧 Subject: {app['subject']}")
            print(f"📨 From: {self.sender_inbox.inbox_id}")
            print(f"📨 To: {self.target_inbox}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send application: {e}")
            return False
    
    def send_scheduling_response(self):
        """Send a scheduling response email"""
        
        content = """Hi,

Thank you for your interest in my application! I'm excited about the opportunity to interview for the ML Engineer position.

Here's my availability for next week:

• Monday, October 2nd: 10am-12pm, 2pm-4pm PST
• Tuesday, October 3rd: 9am-11am, 3pm-5pm PST  
• Wednesday, October 4th: 10am-12pm PST
• Thursday, October 5th: 2pm-6pm PST
• Friday, October 6th: 9am-1pm PST

I'm flexible with the interview format (video call, phone, or in-person if you're in the Bay Area).

Please let me know what works best for your schedule. I'm looking forward to discussing how I can contribute to TechCorp's ML team!

Best regards,
Alex Chen
alex.chen.ml@gmail.com
(555) 123-4567"""

        try:
            response = self.agentmail.inboxes.messages.create(
                inbox_id=self.sender_inbox.inbox_id,
                to=[self.target_inbox],
                subject="Re: Interview Scheduling - ML Engineer Position",
                text=content
            )
            
            print("✅ Sent scheduling response")
            print(f"📧 Subject: Re: Interview Scheduling - ML Engineer Position")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send scheduling response: {e}")
            return False
    
    def send_question(self):
        """Send a general question email"""
        
        content = """Hi,

I submitted my application for the Software Engineer position last week and wanted to ask a few questions about the role:

1. What does the tech stack look like? I saw you mentioned AI/ML but curious about the specific frameworks.

2. Is this role more focused on backend infrastructure, ML research, or product development?

3. What's the team structure like? Would I be working directly with ML researchers?

4. Do you offer any professional development opportunities or conference attendance?

I'm very excited about the possibility of joining TechCorp and contributing to your mission of democratizing AI.

Thanks for your time!

Best regards,
Jordan Smith
jordan.smith@email.com"""

        try:
            response = self.agentmail.inboxes.messages.create(
                inbox_id=self.sender_inbox.inbox_id,
                to=[self.target_inbox],
                subject="Questions about Software Engineer Position",
                text=content
            )
            
            print("✅ Sent question email")
            print(f"📧 Subject: Questions about Software Engineer Position")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send question: {e}")
            return False
    
    def send_follow_up(self):
        """Send a follow-up email"""
        
        content = """Hello,

I wanted to follow up on my application for the ML Engineer position that I submitted two weeks ago.

I remain very interested in the role and would love the opportunity to discuss how my experience building recommendation systems at Netflix could benefit TechCorp's AI platform.

I'm still available for interviews and can provide additional references or work samples if that would be helpful.

Thank you for your consideration, and I look forward to hearing from you soon.

Best regards,
Alex Chen
alex.chen.ml@gmail.com"""

        try:
            response = self.agentmail.inboxes.messages.create(
                inbox_id=self.sender_inbox.inbox_id,
                to=[self.target_inbox],
                subject="Follow-up: ML Engineer Application",
                text=content
            )
            
            print("✅ Sent follow-up email")
            print(f"📧 Subject: Follow-up: ML Engineer Application") 
            return True
            
        except Exception as e:
            print(f"❌ Failed to send follow-up: {e}")
            return False

def main():
    """Interactive test email sender"""
    
    if not os.getenv("AGENTMAIL_API_KEY"):
        print("❌ Error: AGENTMAIL_API_KEY not set in .env file")
        sys.exit(1)
    
    print("🧪 AgentEmail Test Email Sender")
    print("=" * 40)
    
    # Get target inbox
    target_inbox = input("📧 Enter the recruitment agent's inbox email: ").strip()
    if not target_inbox:
        print("❌ No inbox email provided")
        sys.exit(1)
    
    # Create sender
    sender = TestEmailSender(target_inbox)
    
    while True:
        print("\n📧 What type of test email would you like to send?")
        print("1. Strong candidate application")
        print("2. Medium candidate application") 
        print("3. Weak candidate application")
        print("4. Scheduling response")
        print("5. General question")
        print("6. Follow-up email")
        print("7. Send all types (demo)")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-7): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            sender.send_job_application("strong")
        elif choice == "2":
            sender.send_job_application("medium")
        elif choice == "3":
            sender.send_job_application("weak")
        elif choice == "4":
            sender.send_scheduling_response()
        elif choice == "5":
            sender.send_question()
        elif choice == "6":
            sender.send_follow_up()
        elif choice == "7":
            print("🚀 Sending all test email types...")
            sender.send_job_application("strong")
            time.sleep(2)
            sender.send_job_application("medium") 
            time.sleep(2)
            sender.send_job_application("weak")
            time.sleep(2)
            sender.send_scheduling_response()
            time.sleep(2)
            sender.send_question()
            time.sleep(2)
            sender.send_follow_up()
            print("✅ All test emails sent!")
        else:
            print("❌ Invalid choice")
        
        print(f"\n📨 Check your recruitment agent to see how it processes the email!")
        print(f"🎯 Agent inbox: {target_inbox}")

if __name__ == "__main__":
    main()