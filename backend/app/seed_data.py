"""
Seeds the DB with fake customers + historical tickets so the demo doesn't
start empty. Also writes a small CSV to train the ticket classifier on.

Run with: python -m app.seed_data
"""
import random
from datetime import datetime, timedelta

from .database import SessionLocal, init_db, Customer, Ticket
from .services import classifier, sentiment

random.seed(42)

CUSTOMERS = [
    ("Aarav Mehta", "aarav.mehta@example.com", "pro"),
    ("Priya Sharma", "priya.sharma@example.com", "free"),
    ("Rohan Iyer", "rohan.iyer@example.com", "enterprise"),
    ("Sneha Reddy", "sneha.reddy@example.com", "free"),
    ("Vikram Nair", "vikram.nair@example.com", "pro"),
]

# (text, category) pairs used to train the sklearn classifier
TRAINING_DATA = [
    ("I was charged twice for my subscription this month", "billing"),
    ("My invoice shows the wrong amount, please fix it", "billing"),
    ("How do I update my credit card on file", "billing"),
    ("I want a refund for my last payment", "billing"),
    ("Can you cancel my subscription and refund me", "billing"),
    ("The app crashes every time I open the dashboard", "technical"),
    ("I'm getting a 500 error when I try to log in", "technical"),
    ("The export to CSV feature is broken", "technical"),
    ("Page won't load, stuck on a blank screen", "technical"),
    ("API requests are timing out constantly", "technical"),
    ("How do I add a new team member to my workspace", "account"),
    ("I forgot my password and the reset email never arrives", "account"),
    ("How do I change my account email address", "account"),
    ("I can't find where to update my company name", "account"),
    ("Please delete my account and all my data", "account"),
    ("What features are included in the pro plan", "general"),
    ("Do you have an API I can integrate with", "general"),
    ("Is there a mobile app available", "general"),
    ("What are your support hours", "general"),
    ("Can I get a demo of the enterprise plan", "general"),
]

SAMPLE_TICKETS = [
    ("Double charged this month", "I was charged twice for my subscription this month, please refund the extra charge immediately, this is unacceptable"),
    ("App keeps crashing", "The app crashes every time I open the analytics dashboard, very frustrating"),
    ("Can't reset password", "I forgot my password and the reset email never arrives, I've tried 3 times"),
    ("Question about pro plan", "What features are included in the pro plan compared to free?"),
    ("Great support experience", "Just wanted to say the last agent who helped me was fantastic, thank you!"),
    ("API timing out", "Our integration is failing because API requests are timing out constantly since yesterday"),
    ("Need invoice correction", "My invoice shows the wrong amount for this billing cycle, can you correct it"),
    ("How to add team member", "How do I add a new team member to my workspace on the enterprise plan"),
]


def seed():
    init_db()
    db = SessionLocal()

    # Train classifier first so seeded tickets get real predictions
    import pandas as pd
    import os
    os.makedirs("./sample_data", exist_ok=True)
    df = pd.DataFrame(TRAINING_DATA, columns=["text", "category"])
    csv_path = "./sample_data/ticket_training_data.csv"
    df.to_csv(csv_path, index=False)
    acc = classifier.train_from_csv(csv_path)
    print(f"Classifier trained. Training accuracy: {acc:.2f}")

    # Seed customers
    customers = []
    for name, email, plan in CUSTOMERS:
        existing = db.query(Customer).filter(Customer.email == email).first()
        if existing:
            customers.append(existing)
            continue
        c = Customer(name=name, email=email, plan=plan)
        db.add(c)
        db.commit()
        db.refresh(c)
        customers.append(c)

    # Seed tickets spread over the last 14 days
    for i, (subject, message) in enumerate(SAMPLE_TICKETS):
        customer = random.choice(customers)
        sent = sentiment.analyze(message)
        category = classifier.predict(message)
        days_ago = random.randint(0, 13)

        ticket = Ticket(
            customer_id=customer.id,
            subject=subject,
            message=message,
            category=category,
            sentiment=sent["sentiment"],
            sentiment_score=sent["sentiment_score"],
            urgency=sent["urgency"],
            ai_response="(seeded ticket — no AI response generated)",
            kb_confidence=round(random.uniform(0.2, 0.9), 2),
            status=random.choice(["open", "resolved"]),
            created_at=datetime.utcnow() - timedelta(days=days_ago),
        )
        db.add(ticket)

    db.commit()
    print(f"Seeded {len(customers)} customers and {len(SAMPLE_TICKETS)} tickets.")
    db.close()


if __name__ == "__main__":
    seed()
