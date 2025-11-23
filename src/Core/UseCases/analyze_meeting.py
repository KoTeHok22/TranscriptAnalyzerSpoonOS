import os
from typing import Dict, Any
from Core.Interfaces.interfaces import ILLMAnalyzer
from Core.Domain.domain_entities import AuditResult
from Core.Services.standard_cost_calculator import StandardCostCalculator
from Infrastructure.Parsers.simple_text_parser import SimpleTextParser


class AnalyzeMeetingUseCase:
    """Use case for analyzing meeting transcripts."""

    def __init__(
        self,
        llm_analyzer: ILLMAnalyzer,
        cost_calculator: StandardCostCalculator = None,
        text_parser: SimpleTextParser = None
    ):
        """Initialize the use case.

        Args:
            llm_analyzer: The LLM analyzer to use for transcript analysis
            cost_calculator: The cost calculator (optional, will create default if None)
            text_parser: The text parser (optional, will create default if None)
        """
        self.llm_analyzer = llm_analyzer
        self.cost_calculator = cost_calculator or StandardCostCalculator()
        self.text_parser = text_parser or SimpleTextParser()

    async def execute(self, transcript: str) -> Dict[str, Any]:
        """Execute the meeting analysis use case.

        Args:
            transcript: The meeting transcript to analyze

        Returns:
            Dict containing the analysis results and cost calculations
        """
        parsed_data = self.text_parser.parse_transcript(transcript)
        audit_result = await self.llm_analyzer.analyze(transcript)
        cost_data = self.cost_calculator.calculate_costs(audit_result)

        return {
            'transcript_summary': parsed_data,
            'audit_result': audit_result,
            'cost_analysis': cost_data,
            'analysis_complete': True
        }