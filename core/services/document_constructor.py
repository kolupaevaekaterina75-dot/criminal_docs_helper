# core/services/document_constructor.py

from typing import Dict, Any
from django.conf import settings
from docxtpl import DocxTemplate
from pathlib import Path
from .models import Document, Participant

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
            "location": document.location,
            "start_time": document.start_time.strftime("%H:%M"),
            "end_time": document.end_time.strftime("%H:%M"),
            "investigator_position": document.investigator.position,
            "investigator_rank": document.investigator.rank,
            "investigator_name": document.investigator.full_name,
            "witness1_full_name": document.witness1.full_name,
            "witness1_address": document.witness1.address,
            "witness2_full_name": document.witness2.full_name,
            "witness2_address": document.witness2.address,
            "specialist_full_name": document.specialist.full_name,
            "specialist_position": document.specialist.position,
            "other_participants": document.other_participants,
            "location_description": document.location_description,
            "lighting": document.lighting,
            "weather_conditions": document.weather_conditions,
            "temperature": document.temperature,
            "place_description": document.place_description,
            "found_items": document.found_items,
            "technical_means": document.technical_means,
            "phototable_number": document.phototable_number,
            "remarks": document.remarks
        }


class ExplanationConstructor(BaseDocumentConstructor):
    def __init__(self):
        super().__init__("explanation.docx")

    def build_context(self, document: Document) -> Dict[str, Any]:
        participant = document.participant
        return {
            "date": document.issue_date.strftime("%d.%m.%Y"),
            "location": document.location,
            "place": document.place,
            "start_time": document.start_time.strftime("%H:%M"),
            "end_time": document.end_time.strftime("%H:%M"),
            "full_name": document.person.full_name,
            "birth_date": document.person.birth_date.strftime("%d.%m.%Y"),
            "birth_place": document.person.birth_place,
            "address": document.person.address,
            "phone": document.person.phone,
            "citizenship": document.person.citizenship,
            "education": document.person.education,
            "marital_status": document.person.marital_status,
            "employment": document.person.employment,
            "work_phone": document.person.work_phone,
            "military_duty": document.person.military_duty,
            "criminal_record": document.person.criminal_record,
            "document_type": document.person.document_type,
            "document_number": document.person.document_number,
            "explanation_text": document.explanation_text,
            "signature": document.person.signature,
            "investigator_name": document.investigator.full_name,
            "attachments": document.attachments
        }


class VoluntarySurrenderConstructor(BaseDocumentConstructor):
    def __init__(self):
        super().__init__("voluntary_surrender.docx")

    def build_context(self, document: Document) -> Dict[str, Any]:
        person = document.person
        return {
            "date": document.issue_date.strftime("%d.%m.%Y"),
            "location": document.location,
            "investigator_position": document.investigator.position,
            "investigator_rank": document.investigator.rank,
            "investigator_name": document.investigator.full_name,
            "place": document.place,
            "time": document.time.strftime("%H:%M"),
            "authority_name": document.authority_name,
            "person_full_name": person.full_name,
            "birth_date": person.birth_date.strftime("%d.%m.%Y"),
            "birth_place": person.birth_place,
            "address": person.address,
            "employment": person.employment,
            "document_type": person.document_type,
            "document_number": person.document_number,
            "document_issued_by": person.document_issued_by,
            "document_issue_date": person.document_issue_date.strftime("%d.%m.%Y"),
            "crime_description": document.crime_description,
            "read_method": document.read_method,
            "recorded_correctly": document.recorded_correctly,
            "remarks": document.remarks
        }


class ORMInstructionConstructor(BaseDocumentConstructor):
    def __init__(self):
        super().__init__("orm_instruction.docx")
        
    def build_context(self, document: Document) -> Dict[str, Any]:
        return {
            "case_number": document.case_number,
            "investigation_circumstances": document.investigation_circumstances,
            "required_actions": document.required_actions,
            "attachments": document.attachments,
            "investigator_position": document.investigator.position,
            "investigator_rank": document.investigator.rank,
            "investigator_name": document.investigator.full_name,
            "date_day": document.issue_date.strftime("%d"),
            "date_month": document.issue_date.strftime("%m"),
            "date_year": document.issue_date.strftime("%Y"),
            "investigator_initials": document.investigator.initials
        }
