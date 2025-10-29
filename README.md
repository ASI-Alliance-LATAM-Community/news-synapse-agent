<div align="center">

<img src="./docs/images/agent-image.jpg" alt="News Synapse" width="140">

<p></p>

<h1>News Synapse</h1>

<h2>
BGI Hackathon 2025
</br></br>
🥈 2nd Place in the Decentralized News & Media Integrity Track
</h2>

</div>

Designed to build an expansive rather than retracting collective imagination, this agent aims to enrich public discourse by complexifying news and media while countering social polarization and binary thinking.

The agent is designed to detect and amplify content and news that transcend ideological polarization, promoting nuanced thinking and exploring the gray areas, with the goal of bringing minds closer together rather than driving them apart. The agent curates cultural content that fosters complex, non-dual thought, challenges stereotypes, and builds bridges between cultures. It is trained with the works of high-level authors and philosophers who question simplistic paradigms and confront the status quo from hegemonic media, while being equipped to detect and filter hateful, racist, or misogynistic language.

## Philosophy & Purpose

This agent is designed to:
- Detect and amplify content that transcends ideological polarization
- Promote nuanced thinking and explore gray areas
- Bring minds closer together rather than driving them apart
- Curate cultural content that fosters complex, non-dual thought
- Challenge stereotypes and build bridges between cultures
- Filter hateful, racist, or misogynistic language

The agent is trained with works from high-level authors and philosophers who question simplistic paradigms and confront the status quo of hegemonic media.

## Getting Started

### 1) Clone the repository

```bash
git clone https://github.com/ASI-Alliance-LATAM-Community/news-synapse-agent.git
cd news-synapse-agent
```

### 2) Set up the agent environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3) Configure environment variables

Create a `.env` file in the root directory and add your API keys:

```env
ASI1_API_KEY=your_asi1_api_key_here // https://asi1.ai/chat
MEDIACLOUD_API_KEY=your_mediacloud_api_key_here // https://www.mediacloud.org/
```

### 4) Run the agent

```bash
cd src/
python3 agent.py
```

## Features

- **Philosophical Integration**: Applies perspectives from 16 carefully selected thinkers including Socrates, Nietzsche, Foucault, bell hooks, James Baldwin, and more
- **News Search & Analysis**: Real-time news search with philosophical analysis using MediaCloud API
- **Offensive Language Detection**: Sophisticated detection and alternative suggestions for problematic language
- **Cultural Bridge Building**: Actively works to challenge stereotypes and build understanding between perspectives
- **Critical Thinking Enhancement**: Questions assumptions, examines power dynamics, and challenges binary thinking
- **Multi-perspective Analysis**: Considers multiple cultural perspectives on every topic

## Project Structure

```
├── src/
│   ├── agent.py                    # Main agent implementation
│   ├── tools.py                    # Tool definitions for news search
│   ├── philosophical_framework.py  # Core philosophical reasoning system
│   ├── cultural_bridge.py         # Cultural bridge building logic
│   ├── news_bridge.py             # News search and analysis module
│   ├── mediacloud_client.py       # MediaCloud API client
│   └── training_module.py         # Training and learning capabilities
├── requirements.txt               # Python dependencies
├── .env.example                  # Environment variables template
├── AGENTVERSE.md                 # Detailed agent documentation
├── LICENSE.md                    # License information
└── README.md                     # This file
```

## Usage Examples

### News Search Commands

The agent can search for current news and articles using specific trigger phrases:

```
"Search news about cultural bridges"
"Find stories about universities in Latin America"
"Show me latest articles on dialogue between cultures"
"Search news about immigration in the last 15 days, show me 3 stories"
```

### Philosophical Analysis

Ask questions that benefit from multi-perspective analysis:

```
"What are the different perspectives on this social issue?"
"How might different cultures view this topic?"
"What assumptions might I be making about this situation?"
```

### Cultural Bridge Building

Get help navigating cultural differences:

```
"How can I better understand this cultural practice?"
"What might be alternative ways to frame this conversation?"
"Help me see this from multiple cultural perspectives"
```

## Core Technologies

| Component | Purpose |
|-----------|---------|
| **ASI1 AI Model** | Natural language processing and reasoning |
| **MediaCloud API** | Real-time news search and article retrieval |
| **Philosophical Framework** | 16 integrated philosophical perspectives |
| **Cultural Bridge Builder** | Cross-cultural understanding algorithms |
| **uAgents Framework** | Agent communication and protocol handling |

## Requirements

- Python 3.8+
- Virtual environment (recommended)
- ASI1 API key
- MediaCloud API key (optional, for enhanced news search)

## Dependencies

- `uagents` - Agent framework for communication protocols
- `uagents-core` - Core agent functionality and chat protocols
- `requests` - HTTP client for API calls
- `python-dotenv` - Environment variable management

## What Makes This Agent Unique

This agent doesn't just answer questions - it **transforms how you think about questions**. By integrating wisdom from diverse philosophical traditions and actively working to build understanding across differences, every interaction becomes an opportunity for intellectual and emotional growth.

### Key Differentiators:

- **16 Philosophical Perspectives**: Automatically integrates multiple philosophical lenses
- **Real-time Language Analysis**: Detects and suggests alternatives for problematic language
- **Cultural Intelligence**: Builds bridges between different worldviews
- **News Contextualization**: Provides philosophical analysis of current events
- **Anti-polarization**: Actively works against binary thinking and division

## License

MIT License - See LICENSE.md file for details.

## Contributing

We welcome contributions that align with our mission of building cultural bridges and promoting nuanced thinking. Please ensure any contributions:

- Respect diverse perspectives
- Promote understanding over division
- Include appropriate philosophical context
- Follow the existing code structure

---

<p align="center">
  Built with ❤️ for fostering cross-cultural understanding and critical thinking
  <br>
  <em>"The goal isn't to be 'politically correct' but to think more clearly, question assumptions, and build genuine understanding across differences."</em>
</p>

