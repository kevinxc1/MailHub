# MailHub - AI Recruitment Agent

An intelligent recruitment agent built with AgentMail and Claude AI for automated job application processing, candidate evaluation, and interview coordination.

## Features

- Smart email processing and categorization
- AI-powered candidate evaluation using Claude AI
- Automated interview coordination
- Real-time email monitoring
- Candidate state tracking

## Quick Start

1. Clone and setup:
   ```bash
   git clone <repository>
   cd mhacks25
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. Run the agent:
   ```bash
   ./run.sh
   ```

## Configuration

Create a `.env` file with:

```bash
AGENTMAIL_API_KEY=your_agentmail_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
INTERVIEWER_EMAIL=interviewer@company.com
```

## How It Works

The agent processes emails through a pipeline:
1. Creates AgentMail inbox for applications
2. Categorizes emails (applications, scheduling, questions)
3. Evaluates candidates with Claude AI
4. Sends personalized responses
5. Coordinates interview scheduling

Candidate progression: `new` → `screening` → `scheduling` → `interviewed` → `hired`/`rejected`

## Architecture

```
MailHub Agent
├── AgentMail SDK - Email infrastructure
├── Claude AI - Response generation & evaluation
├── State Management - Candidate tracking
└── Conversation Context - Thread history
```

## Development

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

## License

MIT License - see LICENSE file for details