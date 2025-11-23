import os
import asyncio
import sys
import pathlib
from typing import Dict, Any
import json
from datetime import datetime

src_path = str(pathlib.Path(__file__).parent / "src")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.path.insert(0, src_path)

from dotenv import load_dotenv
load_dotenv()

from src.Infrastructure.LLM.spoon_client import SpoonLLMClient
from src.use_cases.analyze_meeting import AnalyzeMeetingUseCase


async def run_analysis():
    """Run transcript analysis using the proper architecture from src."""
    print("Initializing SpoonOS Transcript Analysis Agent...")

    config = {
        "api_key": os.getenv("SPOON_API_KEY"),
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "base_url": "https://openrouter.ai/api/v1"
    }

    llm_adapter = SpoonLLMClient(config=config)
    app = AnalyzeMeetingUseCase(llm_adapter)

    test_transcripts = [
        {
            "name": "Critical Incident Post-Mortem",
            "transcript": """
            Meeting transcript:
            Attendees: Alex (DevOps), Sarah (CTO), Marcus (Backend)
            Date: 2023-11-02

            Sarah: Why did the payment gateway go down yesterday?
            Alex: It was a memory leak in the legacy microservice. We ignored the refactoring ticket.
            
            Sarah: Marcus, can you take ownership of the rewrite?
            Marcus: Yes, I will do it.
            Sarah: I need it done by next Friday, November 10th.
            
            Alex: We should review the architecture before deploying.
            Sarah: Agreed. Let's meet in the War Room tomorrow at 9:00 AM to review the diagrams.
            """
        },
        {
            "name": "Sales & Engineering Sync",
            "transcript": """
            Meeting transcript:
            Attendees: Elena (Sales), Tom (Eng)
            Date: 2023-11-05

            Elena: Can we deliver the SSO feature by next month for the MegaCorp deal?
            Tom: No, that's impossible without overtime. It's scheduled for Q2.
            
            Elena: What if we hire contractors?
            Tom: We don't have documentation for them. It's a huge risk.
            
            Elena: I'll set up a budget meeting with Finance.
            Tom: When?
            Elena: Let's meet next Tuesday at 2 PM via Zoom.
            
            Tom: Fine. Please send me the contract details.
            Elena: I will email them to you by end of day today.
            """
        }
    ]

    results = []
    for transcript_data in test_transcripts:
        print(f"\nAnalyzing: {transcript_data['name']}")
        
        try:
            result = await app.execute(transcript_data['transcript'])
            result["test_name"] = transcript_data["name"]
            
            audit_result = result.get('audit_result')
            
            meeting_report = {}
            
            if hasattr(audit_result, 'raw_report'):
                meeting_report = audit_result.raw_report
            elif hasattr(audit_result, 'details') and audit_result.details:
                try:
                    meeting_report = json.loads(audit_result.details)
                except:
                    pass
            
            result['meeting_report'] = meeting_report
            
            results.append(result)

            print(f"Completed analysis for: {transcript_data['name']}")
            print(f"Risk Score: {audit_result.risk_score}")
            
            if meeting_report:
                q_count = len(meeting_report.get('questions', []))
                m_count = len(meeting_report.get('meetings', []))
                t_count = len(meeting_report.get('tasks', []))
                print(f"Extracted: {q_count} Questions, {m_count} Meetings, {t_count} Tasks")

        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            import traceback
            traceback.print_exc()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"spoonos_results_{timestamp}.json"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)

    print(f"\nAnalysis completed. Results saved to {filename}")

    try:
        from report_generator import create_meeting_analysis_report
        create_meeting_analysis_report(filename)
        print(f"DOCX report generated: {filename.replace('.json', '_report.docx')}")
    except ImportError:
        print("Note: report_generator.py not found.")
    except Exception as e:
        print(f"Error generating DOCX report: {str(e)}")


if __name__ == "__main__":
    asyncio.run(run_analysis())