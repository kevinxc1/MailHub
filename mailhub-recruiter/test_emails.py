#!/usr/bin/env python3
"""
Test Email Sender for MailHub Recruitment Agent
Sends various types of test emails to demonstrate the agent's capabilities
"""

import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Sample test emails
TEST_EMAILS = {
    "strong_candidate": {
        "subject": "Software Engineer Application - Jane Doe",
        "content": """Dear Hiring Team,

I am writing to express my strong interest in the Software Engineer position at TechCorp. 

About me:
- 5 years of experience in full-stack development
- Expert in Python, JavaScript, React, and Node.js
- MS in Computer Science from Stanford
- Previous experience at Google and Meta
- Led a team of 4 engineers on a machine learning project
- Published 3 papers on AI/ML at top conferences

I'm particularly excited about TechCorp's mission in AI/ML and would love to contribute to your innovative projects. I have experience with TensorFlow, PyTorch, and have built several production ML systems that serve millions of users.

I'm available for interviews next week and can start immediately.

Best regards,
Jane Doe
jane.doe@email.com
LinkedIn: linkedin.com/in/jane-doe-swe"""
    },
    
    "weak_candidate": {
        "subject": "Job Application",
        "content": """Hi,

I want to apply for job at your company. I just graduated from college and looking for work. I know some Python and have done some projects in school.

I am available anytime and need job soon.

Thanks,
Bob
bob123@email.com"""
    },
    
    "scheduling_response": {
        "subject": "Re: Interview Scheduling",
        "content": """Hi,

Thank you for considering my application! I'm excited about the opportunity.

I'm available for the screening call on:
- Monday 2-5 PM PST
- Tuesday 10 AM - 12 PM PST  
- Wednesday any time after 1 PM PST
- Friday morning before 11 AM PST

Please let me know what works best for your schedule.

Best regards,
Jane Doe"""
    },
    
    "follow_up": {
        "subject": "Following up on my application",
        "content": """Hello,

I submitted my application for the Software Engineer position about a week ago and wanted to follow up on the status.

I'm very interested in the role and the company, and I'm happy to provide any additional information you might need.

Thank you for your time!

Best,
Alex Chen
alex.chen@email.com"""
    },
    
    "question": {
        "subject": "Questions about the role",
        "content": """Hi there,

I'm interested in applying for the Software Engineer position but had a few questions:

1. Is this role remote-friendly?
2. What's the tech stack you're primarily using?
3. What does the typical day look like for this position?
4. Are there opportunities for professional development?

I have 3 years of experience in Python and React, and I'm very interested in AI/ML work.

Thank you!

Sarah Johnson
sarah.j@email.com"""
    }
}

def send_test_email(to_address: str, email_type: str, from_email: str = "test@example.com"):
    """Send a test email of the specified type"""
    
    if email_type not in TEST_EMAILS:
        print(f"❌ Unknown email type: {email_type}")
        return False
    
    email_data = TEST_EMAILS[email_type]
    
    print(f"📧 Sending {email_type} email to {to_address}")
    print(f"📝 Subject: {email_data['subject']}")
    print(f"📄 Content preview: {email_data['content'][:100]}...")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_address
    msg['Subject'] = email_data['subject']
    
    # Add body
    msg.attach(MIMEText(email_data['content'], 'plain'))
    
    # In a real implementation, you'd use SMTP to send
    # For demo purposes, we'll just print what would be sent
    print("=" * 50)
    print("EMAIL CONTENT:")
    print(f"To: {to_address}")
    print(f"From: {from_email}")
    print(f"Subject: {email_data['subject']}")
    print()
    print(email_data['content'])
    print("=" * 50)
    print("✅ Email sent successfully!")
    
    return True

def send_test_sequence(to_address: str):
    """Send a sequence of test emails to demonstrate the full workflow"""
    
    print(f"🚀 Starting test email sequence to: {to_address}")
    print("This will send 5 different types of emails to test the agent\n")
    
    # Send emails with delays
    for i, (email_type, _) in enumerate(TEST_EMAILS.items(), 1):
        print(f"\n📨 Step {i}/5: Sending {email_type.replace('_', ' ')} email")
        send_test_email(to_address, email_type, f"candidate{i}@testmail.com")
        
        if i < len(TEST_EMAILS):
            print("⏳ Waiting 10 seconds before next email...")
            time.sleep(10)
    
    print("\n🎉 Test sequence completed!")
    print("Check your MailHub agent logs to see how it processes these emails.")

def interactive_sender():
    """Interactive email sender"""
    
    print("📧 MailHub Test Email Sender")
    print("=" * 40)
    
    # Get target email address
    to_address = input("Enter the MailHub agent email address: ").strip()
    if not to_address:
        print("❌ No email address provided")
        return
    
    while True:
        print("\nSelect email type to send:")
        print("1. Strong candidate application")
        print("2. Weak candidate application") 
        print("3. Scheduling response")
        print("4. Follow-up email")
        print("5. Question email")
        print("6. Send all emails (sequence)")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-6): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            send_test_email(to_address, "strong_candidate")
        elif choice == "2":
            send_test_email(to_address, "weak_candidate")
        elif choice == "3":
            send_test_email(to_address, "scheduling_response")
        elif choice == "4":
            send_test_email(to_address, "follow_up")
        elif choice == "5":
            send_test_email(to_address, "question")
        elif choice == "6":
            send_test_sequence(to_address)
        else:
            print("❌ Invalid choice. Please try again.")

def main():
    """Main function"""
    print("🧪 MailHub Test Email Generator")
    print("This script helps you test the recruitment agent with sample emails\n")
    
    print("IMPORTANT NOTE:")
    print("This script simulates sending emails by showing what would be sent.")
    print("To actually send emails to your agent, you'll need to:")
    print("1. Get the agent's inbox address (run main.py)")
    print("2. Send emails manually or set up SMTP configuration")
    print("3. Use a service like Gmail, Outlook, or a testing tool\n")
    
    # Check if we're running the interactive mode
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_sender()
    else:
        print("Available email types:")
        for email_type, data in TEST_EMAILS.items():
            print(f"  📧 {email_type}: {data['subject']}")
        
        print(f"\nTo run interactively: python {sys.argv[0]} --interactive")
        print("To send a specific email type: python test_emails.py [email_type] [to_address]")
        
        # If specific args provided
        if len(sys.argv) == 3:
            email_type, to_address = sys.argv[1], sys.argv[2]
            send_test_email(to_address, email_type)

if __name__ == "__main__":
    main()