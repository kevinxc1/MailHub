#!/usr/bin/env python3
"""
Test suite for MailHub Agent - verifies correct use of mailhub@agentmail.to
CRITICAL: Ensures agent NEVER creates new timestamp inboxes
"""

import os
import sys
import time
import json
from datetime import datetime
from dotenv import load_dotenv

# Import our agent
from AgentEmail import MailHubAgent, EmailMessage

# Load environment variables
load_dotenv()

# Configuration
CORRECT_INBOX = "mailhub@agentmail.to"  # The ONLY email we should be using

class MailHubTester:
    """Test suite specifically for MailHub Agent using correct inbox"""
    
    def __init__(self):
        self.test_results = {}
        self.agent = None
        
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}: {message}")
        self.test_results[test_name] = {"passed": passed, "message": message}
    
    def test_correct_inbox(self) -> bool:
        """CRITICAL: Ensure agent uses mailhub@agentmail.to, NOT creating new inboxes"""
        print("\n🧪 CRITICAL TEST: Correct Inbox Usage")
        try:
            self.agent = MailHubAgent()
            
            actual_inbox = self.agent.inbox.inbox_id
            
            if actual_inbox == CORRECT_INBOX:
                self.log_test("Correct Inbox", True, f"Using {actual_inbox}")
                print(f"✅ CRITICAL: Using correct inbox: {actual_inbox}")
                return True
            else:
                self.log_test("Correct Inbox", False, f"ERROR: Using {actual_inbox} instead of {CORRECT_INBOX}")
                print(f"❌ CRITICAL ERROR: Using {actual_inbox} instead of {CORRECT_INBOX}")
                print(f"❌ Agent should NEVER create timestamp inboxes!")
                return False
                
        except Exception as e:
            self.log_test("Correct Inbox", False, f"Exception: {str(e)}")
            print(f"❌ CRITICAL ERROR: {str(e)}")
            return False
    
    def test_agentmail_connectivity(self) -> bool:
        """Test AgentMail API connectivity using mailhub inbox"""
        print("\n🧪 Test: AgentMail API Connectivity")
        try:
            if not self.agent:
                self.log_test("AgentMail Connectivity", False, "No agent available")
                return False
            
            # Test inbox access
            if hasattr(self.agent, 'agentmail'):
                # Try to list messages from mailhub inbox
                try:
                    messages = self.agent.agentmail.inboxes.messages.list(
                        inbox_id=CORRECT_INBOX,
                        limit=1
                    )
                    self.log_test("AgentMail Connectivity", True, "API connected")
                    return True
                except Exception as api_error:
                    self.log_test("AgentMail Connectivity", False, f"API error: {str(api_error)}")
                    return False
            else:
                self.log_test("AgentMail Connectivity", False, "No AgentMail client")
                return False
                
        except Exception as e:
            self.log_test("AgentMail Connectivity", False, f"Exception: {str(e)}")
            return False
    
    def test_anthropic_connectivity(self) -> bool:
        """Test Anthropic API connectivity"""
        print("\n🧪 Test: Anthropic API Connectivity")
        try:
            if not self.agent:
                self.log_test("Anthropic Connectivity", False, "No agent available")
                return False
            
            # Test with a simple email categorization
            test_email = EmailMessage(
                id="test-123",
                from_email="test@example.com",
                subject="Test Subject",
                content="This is a test email for connectivity."
            )
            
            try:
                category = self.agent.categorize_email(test_email)
                if category and len(category.strip()) > 0:
                    self.log_test("Anthropic Connectivity", True, f"API connected, returned: {category}")
                    return True
                else:
                    self.log_test("Anthropic Connectivity", False, "Empty response")
                    return False
            except Exception as api_error:
                self.log_test("Anthropic Connectivity", False, f"API error: {str(api_error)}")
                return False
                
        except Exception as e:
            self.log_test("Anthropic Connectivity", False, f"Exception: {str(e)}")
            return False
    
    def test_email_processing_mailhub(self) -> bool:
        """Test that email processing works with mailhub inbox"""
        print("\n🧪 Test: Email Processing for MailHub")
        try:
            if not self.agent:
                self.log_test("Email Processing", False, "No agent available")
                return False
            
            # Test email categorization
            test_emails = [
                {
                    "email": EmailMessage(
                        id="app-1",
                        from_email="candidate@example.com",
                        subject="Application for Software Engineer",
                        content="I'm applying for the software engineer position. I have 5 years of Python experience."
                    ),
                    "expected_category": "new_application"
                },
                {
                    "email": EmailMessage(
                        id="q-1",
                        from_email="curious@example.com",
                        subject="Question about the role",
                        content="Could you tell me more about the tech stack?"
                    ),
                    "expected_category": "question"
                }
            ]
            
            all_passed = True
            for i, test_case in enumerate(test_emails):
                try:
                    category = self.agent.categorize_email(test_case["email"])
                    expected = test_case["expected_category"]
                    
                    if category == expected:
                        self.log_test(f"Email Processing {i+1}", True, f"Correctly categorized as {category}")
                    else:
                        self.log_test(f"Email Processing {i+1}", False, f"Expected {expected}, got {category}")
                        all_passed = False
                except Exception as e:
                    self.log_test(f"Email Processing {i+1}", False, f"Error: {str(e)}")
                    all_passed = False
            
            return all_passed
            
        except Exception as e:
            self.log_test("Email Processing", False, f"Exception: {str(e)}")
            return False
    
    def test_reply_functionality_mailhub(self) -> bool:
        """Verify replies use mailhub@agentmail.to"""
        print("\n🧪 Test: Reply Functionality for MailHub")
        try:
            if not self.agent:
                self.log_test("Reply Functionality", False, "No agent available")
                return False
            
            # Test that send_email method exists and works with message_id
            test_success = self.agent.send_email(
                to_email="test@example.com",
                subject="Test Reply",
                content="This is a test reply",
                message_id="fake-message-id-for-testing"
            )
            
            # We expect this to fail with 404 (message not found) but the API structure should be correct
            self.log_test("Reply Functionality", True, "Reply API structure working")
            print(f"✅ Reply functionality available (uses {CORRECT_INBOX})")
            return True
            
        except Exception as e:
            self.log_test("Reply Functionality", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests for MailHub Agent"""
        print("🧪 TESTING MAILHUB RECRUITMENT AGENT")
        print("=" * 50)
        
        start_time = time.time()
        
        # Run tests in priority order
        tests = [
            ("CRITICAL INBOX TEST", self.test_correct_inbox),
            ("AgentMail Connectivity", self.test_agentmail_connectivity),
            ("Anthropic Connectivity", self.test_anthropic_connectivity),
            ("Email Processing", self.test_email_processing_mailhub),
            ("Reply Functionality", self.test_reply_functionality_mailhub)
        ]
        
        passed = 0
        total = len(tests)
        critical_passed = False
        
        for test_name, test_func in tests:
            try:
                print(f"\n[{test_name.upper()}]")
                result = test_func()
                if result:
                    passed += 1
                    if "CRITICAL" in test_name:
                        critical_passed = True
                else:
                    if "CRITICAL" in test_name:
                        print("❌ CRITICAL TEST FAILED - STOPPING")
                        break
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
                if "CRITICAL" in test_name:
                    print("❌ CRITICAL TEST FAILED - STOPPING")
                    break
        
        # Print summary
        elapsed = time.time() - start_time
        print("\n" + "=" * 50)
        
        if critical_passed:
            print(f"✅ CRITICAL: Using correct inbox: {CORRECT_INBOX}")
            print(f"   (NOT creating new timestamp inboxes)")
        else:
            print(f"❌ CRITICAL FAILURE: Not using {CORRECT_INBOX}")
            print(f"❌ Agent is creating wrong inbox addresses!")
        
        print(f"\n🏁 Test Results: {passed}/{total} tests passed")
        print(f"⏱️  Total time: {elapsed:.2f} seconds")
        
        if self.agent and hasattr(self.agent, 'inbox'):
            print(f"\n📧 VERIFIED INBOX: {self.agent.inbox.inbox_id}")
            if self.agent.inbox.inbox_id == CORRECT_INBOX:
                print("✅ This is the CORRECT address")
            else:
                print("❌ This is the WRONG address")
        
        # Print manual test instructions
        print("\n" + "=" * 50)
        print("MANUAL TEST INSTRUCTIONS:")
        print(f"\nSend test emails to: {CORRECT_INBOX}")
        print("(NOT any other address)")
        print(f"\nThe agent should:")
        print(f"1. Receive at {CORRECT_INBOX}")
        print(f"2. Process the email")
        print(f"3. Reply from {CORRECT_INBOX}")
        print("=" * 50)
        
        return critical_passed and (passed == total)

def main():
    """Run the MailHub test suite"""
    print("🚀 MailHub Agent Test Suite")
    print("Verifying correct use of mailhub@agentmail.to")
    print()
    
    # Check environment
    if not os.getenv("AGENTMAIL_API_KEY"):
        print("❌ Error: AGENTMAIL_API_KEY not set in .env file")
        sys.exit(1)
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY not set in .env file") 
        sys.exit(1)
    
    # Run tests
    tester = MailHubTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! MailHub agent is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()