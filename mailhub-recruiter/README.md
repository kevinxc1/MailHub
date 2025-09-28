# MailHub - AI Recruitment Agent 🤖📧

An intelligent recruitment agent built with AgentMail and Claude AI for automated job application processing, candidate evaluation, and interview coordination.

## 🚀 Quick Start

1. **Install dependencies**
   ```bash
   cd mailhub-recruiter
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys:
   # AGENTMAIL_API_KEY=your_key
   # ANTHROPIC_API_KEY=your_key  
   # INTERVIEWER_EMAIL=interviewer@company.com
   ```

3. **Run the agent**
   ```bash
   python main.py
   ```

4. **Test with demo emails**
   ```bash
   # Quick demo of AI features
   python demo.py
   
   # Generate test emails
   python test_emails.py --interactive
   ```

## ✨ Features

- **Smart Email Processing**: Automatically categorizes and processes job applications
- **AI-Powered Evaluation**: Uses Claude AI to score and evaluate candidates (1-10 scale)
- **Interview Coordination**: Handles scheduling between candidates and interviewers  
- **Conversation Tracking**: Maintains context across email threads
- **Real-time Processing**: Continuously monitors for new applications
- **State Management**: Tracks candidates through the recruitment pipeline

## 🔄 How It Works

### Email Processing Pipeline

1. **Inbox Creation**: Creates unique AgentMail inbox for receiving applications
2. **Email Categorization**: AI categorizes emails as applications, scheduling, or questions
3. **Candidate Evaluation**: Claude AI scores candidates and determines qualification
4. **Response Generation**: Sends personalized, contextual responses
5. **Interview Coordination**: Facilitates scheduling between candidates and interviewers

### Candidate Journey

```
New Application → AI Evaluation → Response Sent
     ↓
Qualified? → Yes → Screening Invite → Scheduling → Interview Confirmed
     ↓
     No → Polite Rejection with Encouragement
```

### Email Categories

- **new_application**: Initial job applications
- **scheduling_response**: Candidate availability responses  
- **interviewer_feedback**: Responses from interviewer
- **question**: General candidate questions
- **follow_up**: Application status inquiries

## 📁 Project Structure

```
mailhub-recruiter/
├── main.py               # Main agent implementation
├── requirements.txt      # Dependencies
├── .env.example         # Environment template
├── README.md            # This documentation
├── demo.py              # Quick demo of AI features
└── test_emails.py       # Script to generate test emails
```

## 🧪 Testing & Demo

### Quick Demo
```bash
python demo.py
```
Shows AI evaluation and response generation without running the full agent.

### Test Email Generator
```bash
# Interactive mode
python test_emails.py --interactive

# Send specific email type
python test_emails.py strong_candidate agent@example.com
```

Generates realistic test emails including:
- Strong candidate applications
- Weak candidate applications
- Scheduling responses
- Follow-up emails
- Question emails

## 🏗️ Architecture

```
MailHub Agent
├── AgentMail SDK - Email infrastructure
├── Claude AI - Response generation & evaluation  
├── State Management - Candidate tracking
└── Conversation Context - Thread history
```

### Key Classes

- `MailHubAgent`: Main agent orchestrator
- `EmailMessage`: Email data structure  
- `CandidateState`: Candidate tracking through pipeline

## 📊 Candidate Evaluation

The AI evaluates candidates on:

- **Technical Skills**: Programming languages, frameworks, tools
- **Experience Level**: Years of experience, previous roles
- **Education**: Degree, university, relevant coursework
- **Project Portfolio**: GitHub, publications, side projects
- **Communication**: Writing quality, professionalism
- **Cultural Fit**: Remote work, startup experience, enthusiasm

**Scoring**: 1-10 scale with automatic qualification threshold

## 🔧 Configuration

### Environment Variables

```bash
# Required
AGENTMAIL_API_KEY=your_agentmail_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional
INTERVIEWER_EMAIL=interviewer@company.com  # Default: interviewer@company.com
```

### Company Profile

The agent represents **TechCorp**, an AI/ML startup with:
- Remote-first culture
- Hiring for: Software Engineers, ML Engineers, Product Managers
- Process: Initial screen → Technical interview → Culture fit → Offer

*Customize in `main.py` line 108-120*

## 🚀 Usage Examples

### Starting the Agent
```bash
python main.py
```

Output:
```
🚀 MailHub Agent running!
📧 Inbox: recruiter-1234567890@agentmail.io
⏰ Checking for emails every 10 seconds...
📊 Current candidates: 0
🗂️  Processed emails: 0
```

### Candidate Interaction Flow

1. **Application Received**
   ```
   📨 Processing email from: jane.doe@email.com
   📂 Email categorized as: new_application
   📊 Candidate scored: 8/10
   ✅ Email sent to jane.doe@email.com
   ```

2. **Scheduling Response**
   ```
   📧 Interview Availability: jane.doe@email.com
   ✅ Email sent to interviewer@company.com
   ✅ Email sent to jane.doe@email.com
   ```

## 🐛 Troubleshooting

### Common Issues

**Import Errors**
```bash
pip install -r requirements.txt
```

**API Key Errors**
- Check `.env` file exists and has correct keys
- Verify API keys are valid and have sufficient credits

**No Emails Received**
- Check the inbox address in agent logs
- Ensure emails are sent to the correct address
- Wait 10 seconds for processing cycle

### Debug Mode

Add this to your `.env`:
```bash
LOG_LEVEL=DEBUG
```

## 🏆 Hackathon Highlights

Built for the AgentMail hackathon, demonstrating:

- **Production-Ready**: Comprehensive error handling and logging
- **AI-Powered**: Intelligent candidate evaluation and response generation
- **Scalable**: Handles multiple candidates and conversation threads
- **User-Friendly**: Easy setup with demo scripts and documentation
- **Feature-Complete**: Full recruitment pipeline from application to interview scheduling

## 📄 License

MIT License - see LICENSE file for details

---

**Ready to revolutionize recruitment with AI? Get started in 2 minutes! 🚀**