import os
import shutil
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="HeadphoneAI - RAG + MCP Demo")

# Mount static UI
ui_path = os.path.join(os.path.dirname(__file__), "ui")
app.mount("/ui", StaticFiles(directory=ui_path), name="ui")

# In-memory state per session (single user demo)
_state = {
    "api_key": None,
    "agent": None,
    "chat_history": [],
    "ingested": False,
}


class SetupRequest(BaseModel):
    api_key: str


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    chat_history: list


@app.get("/")
def root():
    return FileResponse(os.path.join(ui_path, "index.html"))


@app.post("/setup")
def setup(req: SetupRequest):
    """Ingest CSV into ChromaDB and initialise agent."""
    try:
        from rag.ingest import ingest, load
        from agent.agent import build_agent

        chroma_path = os.path.join(os.path.dirname(__file__), "qdrant_db")

        # Re-ingest if needed
        if not _state["ingested"]:
            if os.path.exists(chroma_path):
                shutil.rmtree(chroma_path)
            ingest(req.api_key)
            _state["ingested"] = True

        _state["api_key"] = req.api_key
        _state["agent"] = build_agent(req.api_key)
        _state["chat_history"] = []

        return {"status": "ready", "message": "Catalogue indexed. Ready to chat!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Send a message to the agent."""
    if not _state["agent"]:
        raise HTTPException(status_code=400, detail="Run /setup first with your API key.")

    try:
        from agent.agent import run_agent
        response, history = run_agent(
            _state["agent"],
            req.message,
            _state["chat_history"]
        )
        _state["chat_history"] = history
        return ChatResponse(response=response, chat_history=history)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reset")
def reset():
    """Reset chat history and agent state."""
    _state["agent"] = None
    _state["api_key"] = None
    _state["chat_history"] = []
    _state["ingested"] = False
    return {"status": "reset"}
