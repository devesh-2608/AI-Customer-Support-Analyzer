from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import Counter

from ..database import get_db, Ticket

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    total = len(tickets)

    category_counts = Counter(t.category for t in tickets)
    sentiment_counts = Counter(t.sentiment for t in tickets)
    urgency_counts = Counter(t.urgency for t in tickets)

    resolved = sum(1 for t in tickets if t.status == "resolved")
    resolution_rate = round((resolved / total) * 100, 1) if total else 0

    avg_confidence = round(sum(t.kb_confidence for t in tickets) / total, 3) if total else 0

    # KB gaps: low-confidence tickets -> topics your knowledge base doesn't cover well
    kb_gaps = [
        {"question": t.message, "confidence": t.kb_confidence}
        for t in sorted(tickets, key=lambda x: x.kb_confidence)[:5]
        if t.kb_confidence < 0.4
    ]

    return {
        "total_tickets": total,
        "resolution_rate": resolution_rate,
        "avg_kb_confidence": avg_confidence,
        "category_breakdown": category_counts,
        "sentiment_breakdown": sentiment_counts,
        "urgency_breakdown": urgency_counts,
        "kb_gaps": kb_gaps,
    }


@router.get("/trend")
def trend(db: Session = Depends(get_db)):
    """Ticket volume grouped by date for a time-series chart."""
    rows = (
        db.query(func.date(Ticket.created_at).label("date"), func.count(Ticket.id))
        .group_by(func.date(Ticket.created_at))
        .order_by("date")
        .all()
    )
    return [{"date": str(r[0]), "count": r[1]} for r in rows]
