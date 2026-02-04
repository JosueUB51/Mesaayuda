from pydantic import BaseModel

class CaseCreateRequest(BaseModel):
    text: str
    department: str
    emotion: str | None = None
