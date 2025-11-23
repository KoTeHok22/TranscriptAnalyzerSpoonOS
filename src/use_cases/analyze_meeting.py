from typing import Dict, Any
from Core.Domain.domain_entities import AuditResult
from src.Core.Services.standard_cost_calculator import StandardCostCalculator
from src.Infrastructure.Parsers.simple_text_parser import SimpleTextParser


class AnalyzeMeetingUseCase:
    """Use case for analyzing meeting transcripts using LLM and calculating costs."""

    def __init__(self, llm_adapter, cost_calculator: StandardCostCalculator = None,
                 text_parser: SimpleTextParser = None):
        """Initialize the use case.

        Args:
            llm_adapter: The LLM adapter for analysis
            cost_calculator: The cost calculator service
            text_parser: The text parser for preprocessing
        """
        self.llm_adapter = llm_adapter
        self.cost_calculator = cost_calculator or StandardCostCalculator()
        self.text_parser = text_parser or SimpleTextParser()

    async def execute(self, transcript: str) -> Dict[str, Any]:
        """Execute the meeting analysis use case.

        Args:
            transcript: The meeting transcript to analyze

        Returns:
            Dict containing the analysis results and cost calculations
        """
        parsed_content = self.text_parser.parse_transcript(transcript)
        audit_result = await self.llm_adapter.analyze(transcript)
        cost_analysis = self.cost_calculator.calculate_costs(audit_result)

        result = {
            'audit_result': audit_result,
            'cost_analysis': cost_analysis,
            'parsed_content': parsed_content,
            'success': True
        }

        return result