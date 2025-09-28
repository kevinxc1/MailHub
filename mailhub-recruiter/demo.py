#!/usr/bin/env python3
"""
MailHub Recruitment Agent - Quick Demo Script
Demonstrates the key features without running the full agent
"""

import os
import json
from dotenv import load_dotenv
from agentmail import AgentMail
from anthropic import Anthropic

# Load environment variables
load_dotenv()

def demo_candidate_evaluation():
    """Demo the candidate evaluation functionality"""
    print("🧠 Demo: AI Candidate Evaluation")
    print("=" * 50)
    
    # Sample application email
    sample_application = """
    Subject: Software Engineer Application
    
    Hi there,
    
    I'm writing to apply for the Software Engineer position at your company. 
    I have 3 years of experience in Python and JavaScript, and I've worked 
    on several web applications using React and Django. I'm particularly 
    interested in AI/ML projects and have some experience with TensorFlow.
    
    I have a Computer Science degree from UC Berkeley and have worked at 
    two startups previously. I'm excited about the opportunity to work 
    with your team!
    
    Best regards,
    John Smith
    john.smith@email.com
    """
    
    print(f"📧 Sample Application:\n{sample_application}")
    print("\n" + "=" * 50)
    
    # Initialize Claude
    try:
        claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Evaluate the candidate
        response = claude.messages.create(
            model="claude-3-5-sonnet-20250118",
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
                    "content": f"Application email:\n{sample_application}"
                }
            ]
        )
        
        evaluation = json.loads(response.content[0].text)
        
        print("🎯 AI Evaluation Results:")
        print(f"📊 Score: {evaluation.get('score', 'N/A')}/10")
        print(f"✅ Qualified: {'Yes' if evaluation.get('qualified') else 'No'}")
        print(f"💪 Strengths: {', '.join(evaluation.get('strengths', []))}")
        print(f"❌ Missing Skills: {', '.join(evaluation.get('missing_skills', []))}")
        print(f"➡️  Next Step: {evaluation.get('next_step', 'N/A')}")
        print(f"💭 Reasoning: {evaluation.get('reasoning', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your ANTHROPIC_API_KEY is set in .env file")

def demo_response_generation():
    """Demo the AI response generation"""
    print("\n\n🤖 Demo: AI Response Generation")
    print("=" * 50)
    
    try:
        claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Generate a response
        response = claude.messages.create(
            model="claude-3-5-sonnet-20250118",
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
- Use the candidate's name when you know it"""
                },
                {
                    "role": "user",
                    "content": """This candidate scored 7/10.
Strengths: ['Python experience', 'Web development skills', 'AI/ML interest']
Be enthusiastic and invite them to schedule a screening call.
Ask for their availability in the next week.

Email from: john.smith@email.com
Subject: Software Engineer Application
Content: [Application shown above]

Write a response email that's helpful and professional."""
                }
            ]
        )
        
        ai_response = response.content[0].text
        
        print("📝 AI-Generated Response:")
        print("-" * 30)
        print(ai_response)
        print("-" * 30)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your ANTHROPIC_API_KEY is set in .env file")

def demo_agentmail_connection():
    """Demo AgentMail connection"""
    print("\n\n📧 Demo: AgentMail Connection")
    print("=" * 50)
    
    try:
        agentmail = AgentMail(api_key=os.getenv("AGENTMAIL_API_KEY"))
        
        # List existing inboxes
        inboxes = agentmail.inboxes.list()
        print(f"📥 Found {len(inboxes.inboxes)} existing inboxes")
        
        for inbox in inboxes.inboxes:
            print(f"  📧 {inbox.inbox_id}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your AGENTMAIL_API_KEY is set in .env file")

def main():
    """Run the demo"""
    print("🚀 MailHub Recruitment Agent - Demo")
    print("This demo shows key features without running the full agent\n")
    
    # Check environment
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY not set in .env file")
        return
    
    if not os.getenv("AGENTMAIL_API_KEY"):
        print("❌ Error: AGENTMAIL_API_KEY not set in .env file")
        return
    
    # Run demos
    demo_candidate_evaluation()
    demo_response_generation()
    demo_agentmail_connection()
    
    print("\n\n✅ Demo completed!")
    print("To run the full agent: python main.py")

if __name__ == "__main__":
    main()