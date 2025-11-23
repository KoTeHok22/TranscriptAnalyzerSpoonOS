# SpoonOS Transcript Analyzer

SpoonOS Transcript Analyzer is an advanced AI-powered meeting assistant that automatically processes meeting transcripts to extract key information, generate comprehensive reports, and track action items. Built on the SpoonOS framework, it serves as a perfect meeting companion that creates detailed reports with questions, answers, meetings, and task assignments.

## Features

- **Automatic Transcript Analysis**: Processes meeting transcripts and identifies key information
- **Question Tracking**: Extracts who asked what and who answered with what response
- **Meeting Scheduling**: Identifies where, when, and why meetings are scheduled
- **Task Management**: Tracks who assigns tasks to whom with deadlines
- **Risk Assessment**: Analyzes potential business risks in meetings
- **Cost Analysis**: Provides cost calculations based on audit results
- **Structured Reports**: Generates comprehensive meeting reports in JSON format

## Architecture

The project uses the SpoonOS framework and includes:

- `SpoonTranscriptAnalyzerAgent`: Main AI agent for transcript analysis
- SpoonReactMCP: Core agent class with ReAct loop and MCP support
- ToolManager: For managing tools and resources
- StateGraph: For workflow orchestration
- LLM integration: For advanced analysis and report generation

## Installation

```bash
pip install spoon-ai-sdk
pip install spoon-toolkits
```

## Usage

```python
from spoonos_transcript_analyzer import SpoonTranscriptAnalyzerAgent
import asyncio

async def main():
    agent = SpoonTranscriptAnalyzerAgent()
    await agent.initialize()
    
    transcript = """
    John: What is the project timeline?
    Sarah: We're on track for completion by December.
    Michael: Can Sarah prepare the budget report?
    Sarah: Yes, I'll have it ready by November 15th.
    """
    
    result = await agent.analyze_transcript(transcript)
    print(result)

asyncio.run(main())
```

## Team

- **Mishin Vadim Sergeevich** - Telegram: [@KoTeHok_De](https://t.me/KoTeHok_De)