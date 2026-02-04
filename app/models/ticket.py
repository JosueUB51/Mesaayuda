from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.models.db import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)

    ticket_code = Column(String, unique=True)
    subject = Column(Text)

    department = Column(String)
    department_abbr = Column(String)

    emotion = Column(String)
    confidence = Column(String)

    summary = Column(Text)   # 👈 ESTA ES LA QUE FALTABA

    created_at = Column(DateTime, default=datetime.utcnow)
