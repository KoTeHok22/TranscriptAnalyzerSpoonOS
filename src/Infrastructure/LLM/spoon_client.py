import asyncio
import json
import re
from typing import Dict, Any
from Core.Interfaces.interfaces import ILLMAnalyzer
from Core.Domain.domain_entities import AuditResult
from spoon_ai.llm import get_global_registry
from spoon_ai.schema import Message


class SpoonLLMClient:
    """SpoonAI LLM Client implementing the ILLMAnalyzer interface."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.registry = get_global_registry()
        self.provider = None

    async def initialize(self):
        """Initialize the SpoonAI provider."""
        try:
            provider_name = self.config.get('provider', 'openai')
            self.provider = self.registry.get_provider(provider_name, self.config)
            await self.provider.initialize(self.config)
        except Exception as e:
            raise ConnectionError(f"Failed to initialize SpoonAI provider: {str(e)}")

    async def analyze(self, transcript: str) -> AuditResult:
        """Analyze a transcript using SpoonAI and return an audit result."""
        if not self.provider:
            await self.initialize()

        try:
            system_instruction = (
                "You are an expert Project Management Auditor and Meeting Analyst. "
                "Your goal is to extract structured data from meeting transcripts."
            )

            user_prompt = f"""
            Analyze the following meeting transcript.
            
            TRANSCRIPT:
            {transcript}

            INSTRUCTIONS:
            1. Identify risks, issues, and overall sentiment.
            2. Extract specific interactions:
               - **Questions**: Who asked, who answered, and what was said.
               - **Meetings**: New meetings scheduled (who, when, where, purpose).
               - **Tasks**: Tasks assigned (who assigned, to whom, description, deadline).
            
            OUTPUT FORMAT:
            You MUST respond with a VALID JSON object ONLY. Do not wrap it in markdown code blocks. 
            Use the following structure:
            {{
                "risk_analysis": {{
                    "score": <float 0.0-1.0>,
                    "risk_factors": ["<string>", ...],
                    "recommendations": ["<string>", ...],
                    "summary": "<string>",
                    "confidence": <float 0.0-1.0>
                }},
                "meeting_report": {{
                    "questions": [
                        {{ "questioner": "<name>", "responder": "<name>", "question": "<text>", "answer": "<text>" }}
                    ],
                    "meetings": [
                        {{ "scheduler": "<name>", "datetime": "<date/time>", "location": "<text>", "purpose": "<text>" }}
                    ],
                    "tasks": [
                        {{ "assigner": "<name>", "assignee": "<name>", "task": "<text>", "deadline": "<date/time or 'None'>" }}
                    ]
                }}
            }}
            """

            messages = [
                Message(role="system", content=system_instruction),
                Message(role="user", content=user_prompt)
            ]

            response = await self.provider.chat(messages)
            
            return self._parse_llm_json(response.content)

        except Exception as e:
            print(f"Analysis failed: {e}")
            return AuditResult(
                risk_score=0.0,
                risk_factors=["Analysis Failed"],
                recommendations=["Check LLM connection or prompt"],
                summary=f"Error during analysis: {str(e)}",
                confidence=0.0,
                details="{}"
            )

    def _parse_llm_json(self, content: str) -> AuditResult:
        """Parse the JSON response from LLM and convert to AuditResult."""
        try:
            clean_content = content.strip()
            if clean_content.startswith("```json"):
                clean_content = clean_content[7:]
            if clean_content.endswith("```"):
                clean_content = clean_content[:-3]
            
            data = json.loads(clean_content)
            
            risk_data = data.get("risk_analysis", {})
            report_data = data.get("meeting_report", {})

            result = AuditResult(
                risk_score=risk_data.get("score", 0.5),
                risk_factors=risk_data.get("risk_factors", []),
                recommendations=risk_data.get("recommendations", []),
                summary=risk_data.get("summary", "No summary provided"),
                confidence=risk_data.get("confidence", 0.5),
                details=json.dumps(report_data) 
            )
            
            result.raw_report = report_data 
            
            return result

        except json.JSONDecodeError:
            print("Failed to parse JSON from LLM response. Raw content:")
            print(content)
            return AuditResult(
                risk_score=0.5,
                risk_factors=["JSON Parsing Error"],
                recommendations=["Review LLM output format"],
                summary="The model returned an invalid JSON format.",
                confidence=0.0,
                details="{}"
            )