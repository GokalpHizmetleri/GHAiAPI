from fastapi import FastAPI, Request
import requests
import json
import os

app = FastAPI()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

@app.get("/")
def home():
    return {"status": "ok", "model": "smollm", "service": "Ollama FastAPI Proxy"}

@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    prompt = data.get("prompt", "")
    if not prompt:
        return {"error": "prompt required"}
    payload = {"model": "smollm", "prompt": prompt}
    r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, stream=False)
    try:
        res = r.text
        return json.loads(res)
    except Exception:
        return {"response": res}
