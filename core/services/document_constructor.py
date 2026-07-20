# core/services/document_constructor.py

from typing import Dict, Any
from django.conf import settings
from docxtpl import DocxTemplate
from pathlib import Path
from .models import Document

class BaseDocumentConstructor:
    def __init__(self, template_name: str):
        self.template_name = template_name

    def generate_document(self, document: Document) -> str:
        template_path = Path(settings.BASE_DIR) / "media" / "templates" / self.template_name
        doc = DocxTemplate(template_path)
        
        context = self.build_context(document)
        output_path = self.save_document(doc, document)
        
        return str(output_path.relative_to(settings.BASE_DIR))

    def build_context(self, document: Document) -> Dict[str, Any]:
        raise NotImplementedError

    def save_document(self, doc: DocxTemplate, document: Document) -> Path:
        output_dir = Path(settings.MEDIA_ROOT) / "documents"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        file_name = f"doc_{document.id}_{document.case_number.replace('/', '_')}.docx"
        output_path = output_dir / file_name
        doc.save(output_path)
        return output_path


class ReportConstructor(BaseDocumentConstructor):
    def __init__(self):
        super().__init__("report.docx")
        self.required_fields = [
            "recipient_position",
            "date",
            "author_position",
            "author_rank",
            "author_name",
            "information_source",
            "crime_description"
        ]

    def build_context(self, document: Document) -> Dict[str, Any]:
        return {
            "recipient_position": document.recipient_position,
            "date_day": document.issue_date.strftime("%d"),
            "date_month": document.issue_date.strftime("%m"),
            "date_year": document.issue_date.strftime("%Y"),
            "author_position": document.author.position,
            "author_rank": document.author.rank,
            "author_name": document.author.full_name,
            "information_source": document.information_source,
            "crime_description": document.crime_description
        }


class InspectionProtocolConstructor(BaseDocumentConstructor):
    def __init__(self):
        super().__init__("inspection_protocol.docx")

    def build_context(self, document: Document) -> Dict[str, Any]:
        return {
            "date": document.issue_date.strftime("%d.%m.%Y"),
            "start_time": document.start_time.strftime("%H:%M"),
            "end_time": document.end_time.strftime("%H:%M"),
            "location": document.location,
            "author": document.author.full_name,
            "content": document.content,
            "witnesses": document.witnesses,
            "participants": document.participants
        }


class ExplanationConstructor(BaseDocumentConstructor):
    def __init__(self):
        super().__init__("explanation.docx")

    def build_context(self, document: Document) -> Dict[str, Any]:
        return {
            "date": document.issue_date.strftime("%d.%m.%Y"),
            "person_name": document.person_name,
            "person_address": document.person_address,
            "content": document.content
        }


class VoluntarySurrenderConstructor(BaseDocumentConstructor):
    def __init__(self):
        super().__init__("voluntary_surrender.docx")

    def build_context(self, document: Document) -> Dict[str, Any]:
        return {
            "date": document.issue_date.strftime("%d.%m.%Y"),
            "offense_date": document.offense_date.strftime("%d.%m.%Y"),
            "offense_description": document.offense_description,
            "author": document.author.full_name
        }


class ExpertOrderConstructor(BaseDocumentConstructor):
    def __init__(self):
        super().__init__("expert_order.docx")

    def build_context(self, document: Document) -> Dict[str, Any]:
        return {
            "date": document.issue_date.strftime("%d.%m.%Y"),
            "case_number": document.case_number,
            "expert_name": document.expert_name,
            "expert_type": document.expert_type,
            "subject_matter": document.subject_matter,
            "materials": document.materials,
            "questions": document.questions,
            "investigator": document.investigator.full_name,
            "investigator_position": document.investigator.position,
            "recipient": document.recipient
        }
