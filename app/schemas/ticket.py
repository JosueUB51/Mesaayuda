from pydantic import BaseModel

class TicketCreateRequest(BaseModel):
    subject: str


class TicketResponse(BaseModel):
    ticket_code: str
    department: str
    department_abbr: str
    emotion: str
    confidence: float

    # 🔥 CAMPOS QUE TE FALTABAN
    original_text: str
    summary: str
    created_time: str

class NeedsMoreInfoResponse(BaseModel):
    status: str
    message: str
