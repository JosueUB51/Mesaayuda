from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.ticket import Ticket
from app.core.config import settings
from app.services.classifier import is_ambiguous, ClassifierService


class TicketingService:

    def make_code(self, db: Session, dept_abbr: str) -> str:
        date = datetime.utcnow().strftime("%Y%m%d")
        count = db.query(func.count(Ticket.id)).scalar() or 0
        return f"{settings.TICKET_PREFIX}-{date}-{dept_abbr}-{count + 1:04d}"

    def create_ticket(
        self,
        db: Session,
        subject: str,
        department: str,
        department_abbr: str,
        emotion: str,
        confidence: float,
        summary: str
    ) -> Ticket:
        code = self.make_code(db, department_abbr)

        ticket = Ticket(
            ticket_code=code,
            subject=subject,
            department=department,
            department_abbr=department_abbr,
            emotion=emotion,
            confidence=str(confidence),
            summary=summary
        )

        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        return ticket

    def process_message(self, db: Session, text: str):
        # 1️⃣ Ambiguo → IA pregunta como humano
        if is_ambiguous(text):
            return {
                "type": "question",
                "message": "¿Podrías contarme un poco más sobre el problema que tienes?"
            }

        # 2️⃣ Texto claro → USAR IA DE VERDAD
        classifier = ClassifierService()
        result = classifier.classify(text)

        # ⚠️ classify es async
        import asyncio
        if asyncio.iscoroutine(result):
            result = asyncio.run(result)

        # 3️⃣ Crear ticket COMPLETO
        ticket = self.create_ticket(
            db=db,
            subject=text,
            department=result["department"],
            department_abbr=result["department_abbr"],
            emotion=result["emotion"],
            confidence=result["confidence"],
            summary=result["summary"]
        )

        return {
            "type": "ticket",
            "ticket": {
                "ticket_code": ticket.ticket_code,
                "department": ticket.department,
                "department_abbr": ticket.department_abbr,
                "emotion": ticket.emotion,
                "confidence": float(ticket.confidence),
                "original_text": ticket.subject, 
                "summary": ticket.summary,
                "created_time": datetime.now().strftime("%H:%M:%S")
            }
        }
