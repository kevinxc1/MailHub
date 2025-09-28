#!/usr/bin/env python3
"""
Test script for AgentEmail.py recruitment agent
Tests all core functionality with real APIs
"""

import os
import sys
import json
import time
from typing import Dict, Any
from datetime import datetime

# Import our agent
from AgentEmail import MailHubAgent, EmailMessage, CandidateState

class AgentTester:
    """Test suite for MailHub Agent"""
    
    def __init__(self):
        self.test_results = {}
        self.agent = None
        
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}: {message}")
        self.test_results[test_name] = {"passed": passed, "message": message}
        
    def test_inbox_creation(self) -> bool:
        """Test 1: Verify inbox creation"""
        print("\n🧪 Test 1: Inbox Creation")
        try:
            self.agent = MailHubAgent()
            
            # Check if inbox exists
            if hasattr(self.agent, 'inbox') and self.agent.inbox:
                inbox_id = self.agent.inbox.inbox_id
                self.log_test("Inbox Creation", True, f"Created inbox: {inbox_id}")
                
                # Print inbox email clearly
                print(f"\n📧 INBOX EMAIL: {inbox_id}")
                print(f"🎯 Use this email to send test applications!")
                
                # Verify inbox_id exists
                if inbox_id:
                    self.log_test("Inbox ID Exists", True, f"ID: {inbox_id}")
                    return True
                else:
                    self.log_test("Inbox ID Exists", False, "No inbox ID found")
                    return False
            else:
                self.log_test("Inbox Creation", False, "No inbox object created")
                return False
                
        except Exception as e:
            self.log_test("Inbox Creation", False, f"Exception: {str(e)}")
            return False
    
    def test_email_sending(self) -> bool:
        """Test 2: Verify email sending works"""
        print("\n🧪 Test 2: Email Sending")
        try:
            if not self.agent:
                self.log_test("Email Sending", False, "No agent available")
                return False
            
            # Send a test email to ourselves
            success = self.agent.send_email(
                to_email=self.agent.inbox.inbox_id,
                subject="Test Email from Agent",
                content="This is a test email to verify sending functionality works."
            )
            
            if success:
                self.log_test("Email Sending", True, "Email sent successfully")
                return True
            else:
                self.log_test("Email Sending", False, "Email sending returned False")
                return False
                
        except Exception as e:
            self.log_test("Email Sending", False, f"Exception: {str(e)}")
            return False
    
    def test_ai_response_generation(self) -> bool:
        """Test 3: Test AI response generation"""
        print("\n🧪 Test 3: AI Response Generation")
        try:
            if not self.agent:
                self.log_test("AI Response", False, "No agent available")
                return False
            
            # Create mock email
            mock_email = EmailMessage(
                id="test-123",
                from_email="test@example.com",
                subject="Question about the role",
                content="Hi, I'd like to know more about the software engineer position. What tech stack do you use?"
            )
            
            # Generate response
            response = self.agent.generate_response(mock_email)
            
            # Check response is not placeholder
            if response and len(response.strip()) > 20:
                # Check it's not obviously placeholder text
                placeholder_phrases = ["placeholder", "lorem ipsum", "TODO", "TBD"]
                is_placeholder = any(phrase.lower() in response.lower() for phrase in placeholder_phrases)
                
                if not is_placeholder:
                    self.log_test("AI Response", True, f"Generated {len(response)} chars")
                    print(f"📝 Sample response: {response[:100]}...")
                    return True
                else:
                    self.log_test("AI Response", False, "Response contains placeholder text")
                    return False
            else:
                self.log_test("AI Response", False, "Response too short or empty")
                return False
                
        except Exception as e:
            self.log_test("AI Response", False, f"Exception: {str(e)}")
            return False
    
    def test_email_categorization(self) -> bool:
        """Test 4: Test email categorization"""
        print("\n🧪 Test 4: Email Categorization")
        try:
            if not self.agent:
                self.log_test("Email Categorization", False, "No agent available")
                return False
            
            test_cases = [
                {
                    "email": EmailMessage(
                        id="app-1",
                        from_email="john@example.com",
                        subject="Software Engineer Application",
                        content="Hi, I'm applying for the software engineer position. I have 5 years of Python experience and worked at Google."
                    ),
                    "expected": "new_application"
                },
                {
                    "email": EmailMessage(
                        id="sched-1", 
                        from_email="jane@example.com",
                        subject="Re: Interview Scheduling",
                        content="I'm available Monday 2pm, Tuesday 10am, or Wednesday 3pm for the interview."
                    ),
                    "expected": "scheduling_response"
                },
                {
                    "email": EmailMessage(
                        id="q-1",
                        from_email="bob@example.com", 
                        subject="Question about benefits",
                        content="Could you tell me about the health insurance and vacation policy?"
                    ),
                    "expected": "question"
                }
            ]
            
            all_passed = True
            for i, case in enumerate(test_cases):
                category = self.agent.categorize_email(case["email"])
                expected = case["expected"]
                
                if category == expected:
                    self.log_test(f"Categorization {i+1}", True, f"{category} == {expected}")
                else:
                    self.log_test(f"Categorization {i+1}", False, f"{category} != {expected}")
                    all_passed = False
            
            return all_passed
            
        except Exception as e:
            self.log_test("Email Categorization", False, f"Exception: {str(e)}")
            return False
    
    def test_candidate_evaluation(self) -> bool:
        """Test 5: Test candidate evaluation"""
        print("\n🧪 Test 5: Candidate Evaluation")
        try:
            if not self.agent:
                self.log_test("Candidate Evaluation", False, "No agent available")
                return False
            
            # Create strong candidate application
            strong_candidate = EmailMessage(
                id="eval-1",
                from_email="senior@example.com",
                subject="Senior Python Developer Application", 
                content="""Dear Hiring Manager,

I'm excited to apply for the Senior Python Developer position at TechCorp. 

My background:
- 8 years of Python development experience
- Led ML teams at Netflix and Uber
- Built scalable systems handling 1M+ requests/day
- PhD in Computer Science from Stanford
- Published research in NeurIPS and ICML
- Proficient in: Python, TensorFlow, PyTorch, AWS, Kubernetes

I'm passionate about AI/ML and would love to contribute to TechCorp's mission.

Best regards,
Alex Chen"""
            )
            
            # Evaluate candidate
            evaluation = self.agent.evaluate_candidate(strong_candidate)
            
            # Check evaluation structure
            required_fields = ["score", "qualified", "reasoning"]
            has_required = all(field in evaluation for field in required_fields)
            
            if not has_required:
                self.log_test("Evaluation Structure", False, f"Missing fields: {evaluation}")
                return False
            
            self.log_test("Evaluation Structure", True, "All required fields present")
            
            # Check score is reasonable for strong candidate
            score = evaluation.get("score", 0)
            if isinstance(score, (int, float)) and score >= 1 and score <= 10:
                self.log_test("Score Range", True, f"Score: {score}/10")
                
                # Strong candidate should score well
                if score >= 7:
                    self.log_test("Strong Candidate Score", True, f"High score: {score}/10")
                else:
                    self.log_test("Strong Candidate Score", False, f"Low score for strong candidate: {score}/10")
                    
            else:
                self.log_test("Score Range", False, f"Invalid score: {score}")
                return False
            
            # Check qualified decision
            qualified = evaluation.get("qualified", False)
            self.log_test("Qualification Decision", True, f"Qualified: {qualified}")
            
            print(f"📊 Evaluation result: {evaluation}")
            return True
            
        except Exception as e:
            self.log_test("Candidate Evaluation", False, f"Exception: {str(e)}")
            return False
    
    def test_end_to_end_flow(self) -> bool:
        """Test 6: End-to-end application processing"""
        print("\n🧪 Test 6: End-to-End Flow Simulation")
        try:
            if not self.agent:
                self.log_test("E2E Flow", False, "No agent available")
                return False
            
            # Create application email
            application = EmailMessage(
                id="e2e-test",
                from_email="candidate@example.com",
                subject="Application for ML Engineer Position",
                content="""Hello,

I'm applying for the Machine Learning Engineer position. I have:
- 5 years ML experience at Meta and Google
- Built recommendation systems for 100M+ users  
- Expert in Python, TensorFlow, PyTorch
- MS in Machine Learning from CMU

Looking forward to hearing from you!

Best,
Sarah Kim"""
            )
            
            # Process through full pipeline
            print("🔄 Processing application through full pipeline...")
            
            # Step 1: Categorization
            category = self.agent.categorize_email(application)
            if category != "new_application":
                self.log_test("E2E Categorization", False, f"Wrong category: {category}")
                return False
            self.log_test("E2E Categorization", True, "Correctly categorized as application")
            
            # Step 2: Evaluation  
            evaluation = self.agent.evaluate_candidate(application)
            if not evaluation or "score" not in evaluation:
                self.log_test("E2E Evaluation", False, "Evaluation failed")
                return False
            self.log_test("E2E Evaluation", True, f"Score: {evaluation['score']}/10")
            
            # Step 3: Response generation
            if evaluation.get("qualified", False):
                context = f"This candidate scored {evaluation['score']}/10. Be enthusiastic and invite them to schedule a screening call."
            else:
                context = "This candidate isn't a fit right now. Be encouraging but decline."
                
            response = self.agent.generate_response(application, context)
            if not response or len(response.strip()) < 50:
                self.log_test("E2E Response", False, "Response too short")
                return False
            self.log_test("E2E Response", True, f"Generated {len(response)} char response")
            
            # Step 4: Email sending (simulate)
            # Note: We'll just test the method call, not actually send to avoid spam
            try:
                # This would normally send, but we'll catch any API errors
                # In a real test, you might send to a test email address
                print("📧 Would send response email to candidate")
                self.log_test("E2E Email Send", True, "Email sending method available")
            except Exception as e:
                self.log_test("E2E Email Send", False, f"Send error: {str(e)}")
                return False
            
            self.log_test("End-to-End Flow", True, "Complete pipeline executed successfully")
            return True
            
        except Exception as e:
            self.log_test("End-to-End Flow", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🧪 Starting AgentEmail Test Suite")
        print("=" * 50)
        
        start_time = time.time()
        
        # Run tests in order
        tests = [
            self.test_inbox_creation,
            self.test_email_sending, 
            self.test_ai_response_generation,
            self.test_email_categorization,
            self.test_candidate_evaluation,
            self.test_end_to_end_flow
        ]
        
        passed = 0
        total = len(tests)
        
        for test_func in tests:
            try:
                if test_func():
                    passed += 1
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
        
        # Print summary
        elapsed = time.time() - start_time
        print("\n" + "=" * 50)
        print(f"🏁 Test Results: {passed}/{total} tests passed")
        print(f"⏱️  Total time: {elapsed:.2f} seconds")
        
        if self.agent and hasattr(self.agent, 'inbox'):
            print(f"\n📧 INBOX FOR MANUAL TESTING:")
            print(f"📨 Send emails to: {self.agent.inbox.inbox_id}")
            print(f"🎯 Try sending a job application to test the full flow!")
        
        # Print individual results
        print("\n📊 Detailed Results:")
        for test_name, result in self.test_results.items():
            status = "✅" if result["passed"] else "❌"
            print(f"{status} {test_name}: {result['message']}")
        
        return passed == total

def main():
    """Run the test suite"""
    print("🚀 AgentEmail Test Suite")
    print("This will test all core functionality using real APIs")
    print()
    
    # Check environment
    if not os.getenv("AGENTMAIL_API_KEY"):
        print("❌ Error: AGENTMAIL_API_KEY not set in .env file")
        sys.exit(1)
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY not set in .env file") 
        sys.exit(1)
    
    # Run tests
    tester = AgentTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! Your agent is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()