from sqlalchemy.orm import Session
from app.models.ticket import Ticket

class TicketRepo:
    def create(self, db: Session, **data):
        ticket = Ticket(**data)
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket
