from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import json
import os

app = FastAPI()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

# Serve static files for the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    messages = data.get("messages", [])
    if not messages:
        return {"error": "messages required"}

    # Use the chat endpoint of Ollama which supports history
    payload = {
        "model": "smollm",
        "messages": messages,
        "stream": False
    }

    try:
        r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=60)
        r.raise_for_status()
        res = r.json()
        # Extract the message content from the response
        return res
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
