# AI Customer Support Analyzer

An AI-powered customer support application that combines Retrieval-Augmented Generation (RAG), ticket classification, sentiment analysis, customer history management, and an analytics dashboard.

The system answers customer queries using a company knowledge base, automatically classifies support tickets, analyzes sentiment and urgency, stores customer interactions, and provides insights through an interactive dashboard.

The project is built entirely using open-source tools and runs locally without requiring any paid API services.

---

## Architecture

```
React (Vite + Tailwind + Recharts)
            │
         REST API
            │
            ▼
      FastAPI Backend
            │
   ┌────────┼─────────────┬──────────────┐
   ▼        ▼              ▼              ▼
 Ollama   ChromaDB       SQLite      Scikit-learn
(Local LLM) (Vector DB)  (Database)  (Ticket Classification)
```

---

## Features

- Retrieval-Augmented Generation (RAG) using ChromaDB and Sentence Transformers
- Local LLM inference using Ollama (Llama 3.2)
- Automatic ticket classification using TF-IDF and Logistic Regression
- Sentiment and urgency detection using VADER
- Customer history tracking
- Knowledge base document upload and retrieval
- Interactive analytics dashboard with charts
- Knowledge gap detection based on retrieval confidence

---

## Tech Stack

### Frontend
- React.js
- Tailwind CSS
- Recharts

### Backend
- FastAPI
- SQLAlchemy
- SQLite

### AI & Machine Learning
- Ollama (Llama 3.2)
- ChromaDB
- Sentence Transformers
- Scikit-learn
- VADER Sentiment Analyzer

---

## Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Ollama installed locally

### 1. Pull the model

```bash
ollama pull llama3.2:3b
ollama serve
```

### 2. Backend

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt

python -m app.seed_data

uvicorn app.main:app --reload
```

Backend runs at:

```
http://localhost:8000
```

API documentation:

```
http://localhost:8000/docs
```

### 3. Upload the Knowledge Base

Upload the sample company document after starting the backend.

```bash
curl -F "file=@../sample_data/company_policies.txt" http://localhost:8000/api/kb/upload
```

You can also upload documents from the Knowledge Base page in the frontend.

### 4. Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## Demo

1. Upload a company policy document.
2. Select a customer from the Support Console.
3. Ask questions related to the uploaded document.
4. View generated responses with retrieved document references.
5. Explore the Analytics dashboard to monitor ticket trends, sentiment distribution, category-wise statistics, and knowledge base gaps.

---

## Project Structure

```
backend/
│
├── app/
│   ├── routers/
│   ├── services/
│   ├── database.py
│   ├── main.py
│   ├── schemas.py
│   └── seed_data.py
│
frontend/
│
├── src/
│   ├── components/
│   ├── pages/
│   ├── api.js
│   └── App.jsx
│
sample_data/
└── company_policies.txt
```

---

## Future Improvements

- PostgreSQL support for production deployment
- User authentication and role-based access
- Feedback mechanism for AI-generated responses
- Streaming responses from the LLM
- OCR support for scanned PDF documents
- Fine-tuning the ticket classifier using real support data

---

## License

This project is intended for learning and portfolio purposes.
