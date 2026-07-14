"""
Database setup using SQLAlchemy + SQLite.
SQLite is enough here — this isn't the bottleneck of the project, RAG quality is.
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///./support_analyzer.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    plan = Column(String, default="free")  # free / pro / enterprise
    created_at = Column(DateTime, default=datetime.utcnow)

    tickets = relationship("Ticket", back_populates="customer")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    subject = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    category = Column(String, default="uncategorized")   # predicted by classifier
    sentiment = Column(String, default="neutral")          # positive / neutral / negative
    sentiment_score = Column(Float, default=0.0)
    urgency = Column(String, default="normal")             # low / normal / high
    ai_response = Column(Text, nullable=True)
    kb_confidence = Column(Float, default=0.0)             # retrieval confidence -> KB gap detection
    status = Column(String, default="open")                # open / resolved
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="tickets")


class KBDocument(Base):
    __tablename__ = "kb_documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    chunk_count = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
