from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db, Ticket
from ..schemas import ChatQuery, ChatResponse
from ..services import rag, sentiment, classifier

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/query", response_model=ChatResponse)
def query(payload: ChatQuery, db: Session = Depends(get_db)):
    # 1. Sentiment + urgency (fast, classical NLP)
    sent = sentiment.analyze(payload.question)

    # 2. Category classification (sklearn)
    category = classifier.predict(payload.question)

    # 3. RAG answer (retrieval + local LLM generation)
    rag_result = rag.answer_query(payload.question)

    # 4. Log everything as a ticket -> this is what powers customer history + analytics
    ticket = Ticket(
        customer_id=payload.customer_id,
        subject=payload.question[:60],
        message=payload.question,
        category=category,
        sentiment=sent["sentiment"],
        sentiment_score=sent["sentiment_score"],
        urgency=sent["urgency"],
        ai_response=rag_result["answer"],
        kb_confidence=rag_result["confidence"],
        status="resolved" if rag_result["confidence"] > 0.4 else "open",
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ChatResponse(
        answer=rag_result["answer"],
        sources=rag_result["sources"],
        confidence=rag_result["confidence"],
        category=category,
        sentiment=sent["sentiment"],
        urgency=sent["urgency"],
        ticket_id=ticket.id,
    )
