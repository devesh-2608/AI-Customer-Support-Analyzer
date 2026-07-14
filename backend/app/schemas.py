from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class CustomerOut(BaseModel):
    id: int
    name: str
    email: str
    plan: str
    created_at: datetime

    class Config:
        from_attributes = True


class TicketCreate(BaseModel):
    customer_id: int
    subject: str
    message: str


class TicketOut(BaseModel):
    id: int
    customer_id: int
    subject: str
    message: str
    category: str
    sentiment: str
    sentiment_score: float
    urgency: str
    ai_response: Optional[str]
    kb_confidence: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatQuery(BaseModel):
    customer_id: int
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float
    category: str
    sentiment: str
    urgency: str
    ticket_id: int
