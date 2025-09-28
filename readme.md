# MailHub - AI Recruitment Agent 🤖📧

An intelligent recruitment agent built with AgentMail and Claude AI for automated job application processing, candidate evaluation, and interview coordination.

## Features ✨

- **Smart Email Processing**: Automatically categorizes and processes job applications
- **AI-Powered Evaluation**: Uses Claude AI to score and evaluate candidates
- **Interview Coordination**: Handles scheduling between candidates and interviewers  
- **Conversation Tracking**: Maintains context across email threads
- **Real-time Processing**: Continuously monitors for new applications
- **State Management**: Tracks candidates through the recruitment pipeline

## Quick Start 🚀

1. **Clone and Setup**
   ```bash
   git clone <repository>
   cd mhacks25
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the Agent**
   ```bash
   ./run.sh
   ```

## Manual Setup 🔧

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Add your API keys to .env

# Run the agent
python3 AgentEmail.py
```

## Configuration 📝

Create a `.env` file with:

```bash
# AgentMail API Configuration
AGENTMAIL_API_KEY=your_agentmail_api_key_here

# Anthropic Claude API Configuration  
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Interviewer Configuration
INTERVIEWER_EMAIL=interviewer@company.com
```

## How It Works 🔄

### Email Processing Pipeline

1. **Inbox Creation**: Creates unique AgentMail inbox for receiving applications
2. **Email Categorization**: AI categorizes emails as applications, scheduling, or questions
3. **Candidate Evaluation**: Claude AI scores candidates and determines qualification
4. **Response Generation**: Sends personalized, contextual responses
5. **Interview Coordination**: Facilitates scheduling between candidates and interviewers

### Candidate States

- `new` → `screening` → `scheduling` → `interviewed` → `hired`/`rejected`

### Email Categories

- **new_application**: Initial job applications
- **scheduling_response**: Candidate availability responses  
- **interviewer_feedback**: Responses from interviewer
- **question**: General candidate questions
- **follow_up**: Application status inquiries

## Architecture 🏗️

```
MailHub Agent
├── AgentMail SDK - Email infrastructure
├── Claude AI - Response generation & evaluation  
├── State Management - Candidate tracking
└── Conversation Context - Thread history
```

## Usage Examples 📋

### Starting the Agent
```bash
./run.sh
```

The agent will:
1. Create an inbox and display the email address
2. Start monitoring for new emails every 10 seconds
3. Process applications and send automated responses
4. Coordinate interview scheduling

### Sending Test Applications

Send emails to the generated inbox address with job applications. The agent will:
- Evaluate the candidate automatically
- Send personalized responses
- Notify interviewers of qualified candidates
- Handle follow-up questions

## Development 💻

### Project Structure
```
mhacks25/
├── AgentEmail.py      # Main agent implementation
├── requirements.txt   # Python dependencies  
├── .env.example      # Environment template
├── run.sh           # Execution script
└── README.md        # This file
```

### Key Classes
- `MailHubAgent`: Main agent orchestrator
- `EmailMessage`: Email data structure
- `CandidateState`: Candidate tracking

### Logging
The agent provides detailed logging for debugging:
- Email processing events
- AI evaluation results  
- Error handling and recovery
- Performance statistics

## Hackathon Submission 🏆

Built for the AgentMail hackathon - demonstrating automated recruitment workflows with:
- Intelligent email processing
- AI-powered candidate evaluation
- Seamless interview coordination
- Production-ready error handling

## License 📄

MIT License - see LICENSE file for details