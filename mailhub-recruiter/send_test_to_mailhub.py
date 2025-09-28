#!/usr/bin/env python3
"""
Send test emails specifically to mailhub@agentmail.to
CRITICAL: Uses ONLY the correct mailhub address, never creates new inboxes
"""

import os
import sys
import time
from dotenv import load_dotenv
from agentmail import AgentMail

# Load environment variables
load_dotenv()

# Configuration
MAILHUB_ADDRESS = "mailhub@agentmail.to"  # The ONLY correct address

class MailHubTestSender:
    """Send test emails specifically to mailhub@agentmail.to"""
    
    def __init__(self):
        """Initialize with MailHub as target"""
        if not os.getenv("AGENTMAIL_API_KEY"):
            print("❌ Error: AGENTMAIL_API_KEY not set in .env file")
            sys.exit(1)
            
        self.agentmail = AgentMail(api_key=os.getenv("AGENTMAIL_API_KEY"))
        self.target_inbox = MAILHUB_ADDRESS
        
        # Create our own sender inbox
        self.sender_inbox = self.create_sender_inbox()
        
        print(f"🎯 Target: {MAILHUB_ADDRESS}")
        print(f"📤 Sender: {self.sender_inbox.inbox_id}")
    
    def create_sender_inbox(self):
        """Create inbox for sending test emails"""
        try:
            username = f"test-sender-{int(time.time())}"
            inbox = self.agentmail.inboxes.create(
                username=username,
                display_name="Test Sender"
            )
            print(f"✅ Created sender inbox: {inbox.inbox_id}")
            return inbox
        except Exception as e:
            print(f"❌ Failed to create sender inbox: {e}")
            sys.exit(1)
    
    def send_application_to_mailhub(self, candidate_type: str = "strong"):
        """Send a job application email to mailhub@agentmail.to"""
        
        applications = {
            "strong": {
                "subject": "Application for Senior ML Engineer Position - MailHub Test",
                "content": f"""Dear MailHub Recruitment Team,

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

---
TEST EMAIL sent to: {MAILHUB_ADDRESS}
Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
Sender: {self.sender_inbox.inbox_id}
"""
            },
            
            "medium": {
                "subject": "Software Engineer Application - MailHub Test",
                "content": f"""Hi MailHub Team,

I saw your job posting for a software engineer role and I'm interested in applying.

About me:
- 3 years experience with Python and JavaScript
- Worked at a startup doing web development
- Bachelor's degree in Computer Science
- Know some machine learning from online courses

I'm a quick learner and excited about working at a tech company. Let me know if you'd like to chat!

Thanks,
Jordan Smith
jordan.smith@email.com

---
TEST EMAIL sent to: {MAILHUB_ADDRESS}
Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
Sender: {self.sender_inbox.inbox_id}
"""
            },
            
            "question": {
                "subject": "Questions about Software Engineer Position - MailHub Test",
                "content": f"""Hi MailHub Team,

I submitted my application for the Software Engineer position and wanted to ask a few questions:

1. What does the tech stack look like? I saw you mentioned AI/ML but curious about the specific frameworks.

2. Is this role more focused on backend infrastructure, ML research, or product development?

3. What's the team structure like? Would I be working directly with ML researchers?

4. Do you offer any professional development opportunities or conference attendance?

I'm very excited about the possibility of joining TechCorp and contributing to your mission of democratizing AI.

Thanks for your time!

Best regards,
Jordan Smith
jordan.smith@email.com

---
TEST EMAIL sent to: {MAILHUB_ADDRESS}
Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
Sender: {self.sender_inbox.inbox_id}
"""
            }
        }
        
        if candidate_type not in applications:
            print(f"❌ Unknown candidate type: {candidate_type}")
            return False
        
        app = applications[candidate_type]
        
        try:
            # Send email using AgentMail send API
            response = self.agentmail.inboxes.messages.send(
                inbox_id=self.sender_inbox.inbox_id,
                to=[self.target_inbox],
                subject=app["subject"],
                text=app["content"]
            )
            
            print(f"✅ Sent {candidate_type} candidate application")
            print(f"📧 Subject: {app['subject']}")
            print(f"📨 From: {self.sender_inbox.inbox_id}")
            print(f"📨 To: {self.target_inbox}")
            print(f"🎯 CRITICAL: Sent to {MAILHUB_ADDRESS} (correct address)")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send application: {e}")
            return False
    
    def send_scheduling_response_to_mailhub(self):
        """Send a scheduling response email to mailhub@agentmail.to"""
        
        content = f"""Hi MailHub Team,

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

---
TEST EMAIL sent to: {MAILHUB_ADDRESS}
Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
Sender: {self.sender_inbox.inbox_id}
"""

        try:
            response = self.agentmail.inboxes.messages.send(
                inbox_id=self.sender_inbox.inbox_id,
                to=[self.target_inbox],
                subject="Re: Interview Scheduling - ML Engineer Position - MailHub Test",
                text=content
            )
            
            print("✅ Sent scheduling response")
            print(f"📧 Subject: Re: Interview Scheduling - ML Engineer Position")
            print(f"🎯 CRITICAL: Sent to {MAILHUB_ADDRESS} (correct address)")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send scheduling response: {e}")
            return False
    
    def verify_mailhub_response(self):
        """Instructions for verifying MailHub response"""
        print(f"\n✅ CHECK YOUR EMAIL FOR RESPONSE FROM: {MAILHUB_ADDRESS}")
        print("=" * 60)
        print("EXPECTED BEHAVIOR:")
        print(f"1. MailHub agent receives email at {MAILHUB_ADDRESS}")
        print("2. Agent processes and categorizes the email")
        print("3. Agent generates appropriate response")
        print(f"4. Agent sends reply FROM {MAILHUB_ADDRESS}")
        print("5. Reply maintains email thread")
        print()
        print("VERIFY:")
        print(f"✅ Response comes from {MAILHUB_ADDRESS}")
        print("✅ Response is relevant to your test email")
        print("✅ Response maintains email thread")
        print("✅ No new timestamp inboxes created")
        print("=" * 60)

def print_instructions():
    """Print manual testing instructions"""
    print("📧 MANUAL TESTING INSTRUCTIONS")
    print("=" * 50)
    print(f"Target Address: {MAILHUB_ADDRESS}")
    print("(This is the ONLY correct address)")
    print()
    print("You can also manually send emails to:")
    print(f"📧 {MAILHUB_ADDRESS}")
    print()
    print("Expected Response:")
    print(f"✅ Response FROM: {MAILHUB_ADDRESS}")
    print("✅ Response is contextual and professional")
    print("✅ Response maintains email thread")
    print("=" * 50)

def main():
    """Interactive test email sender for MailHub"""
    
    print("🧪 MailHub Test Email Sender")
    print("=" * 40)
    print(f"🎯 Target: {MAILHUB_ADDRESS}")
    print("(CRITICAL: Uses ONLY the correct address)")
    print()
    
    # Create sender
    try:
        sender = MailHubTestSender()
    except Exception as e:
        print(f"❌ Failed to initialize sender: {e}")
        sys.exit(1)
    
    while True:
        print(f"\n📧 What type of test email to send to {MAILHUB_ADDRESS}?")
        print("1. Strong candidate application")
        print("2. Medium candidate application") 
        print("3. Question about position")
        print("4. Scheduling response")
        print("5. Send all types (demo)")
        print("6. Verify response instructions")
        print("7. Manual testing instructions")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-7): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            sender.send_application_to_mailhub("strong")
        elif choice == "2":
            sender.send_application_to_mailhub("medium")
        elif choice == "3":
            sender.send_application_to_mailhub("question")
        elif choice == "4":
            sender.send_scheduling_response_to_mailhub()
        elif choice == "5":
            print(f"🚀 Sending all test email types to {MAILHUB_ADDRESS}...")
            sender.send_application_to_mailhub("strong")
            time.sleep(2)
            sender.send_application_to_mailhub("medium") 
            time.sleep(2)
            sender.send_application_to_mailhub("question")
            time.sleep(2)
            sender.send_scheduling_response_to_mailhub()
            print("✅ All test emails sent!")
        elif choice == "6":
            sender.verify_mailhub_response()
        elif choice == "7":
            print_instructions()
        else:
            print("❌ Invalid choice")
        
        if choice in ["1", "2", "3", "4", "5"]:
            print(f"\n📨 Check MailHub agent to see how it processes the email!")
            print(f"🎯 Agent should respond FROM: {MAILHUB_ADDRESS}")

if __name__ == "__main__":
    main()