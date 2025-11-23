import re
from typing import Dict, List, Any


class SimpleTextParser:
    """Simple text parser for extracting structured information from raw text."""

    def __init__(self):
        """Initialize the text parser."""
        pass

    def parse_transcript(self, text: str) -> Dict[str, Any]:
        """Parse a transcript and extract structured information.

        Args:
            text: The raw text to parse

        Returns:
            Dict containing structured information from the text
        """
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        word_count = len(text.split())
        char_count = len(text)
        paragraph_count = len(paragraphs)

        key_terms = ['risk', 'issue', 'problem', 'concern', 'opportunity', 'solution', 'decision']
        found_terms = []
        for term in key_terms:
            if term.lower() in text.lower():
                found_terms.append(term)

        return {
            'original_text': text,
            'paragraphs': paragraphs,
            'sentences': sentences,
            'word_count': word_count,
            'char_count': char_count,
            'paragraph_count': paragraph_count,
            'key_terms_found': found_terms,
            'structured_content': self._structure_content(paragraphs)
        }

    def _structure_content(self, paragraphs: List[str]) -> List[Dict[str, Any]]:
        """Structure the content by identifying paragraph types.

        Args:
            paragraphs: List of paragraphs

        Returns:
            List of dictionaries containing structured paragraph information
        """
        structured = []
        for i, paragraph in enumerate(paragraphs):
            para_type = self._identify_paragraph_type(paragraph)
            structured.append({
                'index': i,
                'content': paragraph,
                'type': para_type,
                'word_count': len(paragraph.split())
            })
        return structured

    def _identify_paragraph_type(self, text: str) -> str:
        """Identify the type of paragraph based on content.

        Args:
            text: The paragraph text

        Returns:
            String representing the identified type
        """
        text_lower = text.lower()

        if any(keyword in text_lower for keyword in ['meeting', 'discussion', 'talk', 'confer']):
            return 'meeting_summary'
        elif any(keyword in text_lower for keyword in ['risk', 'danger', 'threat', 'concern']):
            return 'risk_section'
        elif any(keyword in text_lower for keyword in ['solution', 'fix', 'resolve', 'address']):
            return 'solution_section'
        elif any(keyword in text_lower for keyword in ['decision', 'agree', 'determine', 'choose']):
            return 'decision_section'
        elif any(keyword in text_lower for keyword in ['action', 'task', 'step', 'do']):
            return 'action_items'
        else:
            return 'general_content'