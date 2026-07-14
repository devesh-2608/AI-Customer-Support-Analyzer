from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .routers import knowledge_base, chat, tickets, analytics

app = FastAPI(title="AI Customer Support Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(knowledge_base.router)
app.include_router(chat.router)
app.include_router(tickets.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "AI Customer Support Analyzer API running"}
