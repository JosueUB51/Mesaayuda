from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas.ticket import TicketCreateRequest, TicketResponse
from app.models.db import get_db
from app.services.classifier import ClassifierService
from app.services.ticketing import TicketingService
from app.repositories.ticket_repo import TicketRepo

router = APIRouter(prefix="/tickets", tags=["tickets"])


# =========================================================
# FLUJO VIEJO (crear ticket directo – NO SE TOCA)
# =========================================================
@router.post("", response_model=TicketResponse)
async def create_ticket(
    payload: TicketCreateRequest,
    db: Session = Depends(get_db)
):
    classifier = ClassifierService()
    ticketing = TicketingService()
    repo = TicketRepo()

    result = await classifier.classify(payload.subject)

    code = ticketing.make_code(db, result["department_abbr"])

    ticket = repo.create(
        db,
        ticket_code=code,
        subject=payload.subject,
        department=result["department"],
        department_abbr=result["department_abbr"],
        emotion=result["emotion"],
        confidence=str(result["confidence"]),
    )

    return {
        "ticket_code": ticket.ticket_code,
        "department": ticket.department,
        "department_abbr": ticket.department_abbr,
        "emotion": ticket.emotion,
        "confidence": float(ticket.confidence),
        "original_text": payload.subject,
        "summary": result["summary"],
        "created_time": datetime.now().strftime("%H:%M:%S")
    }


# =========================================================
# FLUJO NUEVO (conversación IA)
# =========================================================
@router.post("/message")
def handle_message(
    payload: dict,
    db: Session = Depends(get_db)
):
    text = payload.get("text", "").strip()

    service = TicketingService()
    return service.process_message(db, text)
