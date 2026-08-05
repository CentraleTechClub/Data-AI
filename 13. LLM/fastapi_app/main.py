from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from transformers import pipeline, AutoTokenizer
import torch
import os

app = FastAPI()
BASE = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=os.path.join(BASE, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE, "templates"))

# Modèle local chargé depuis le dossier assets.
MODEL_PATH = os.path.join(BASE, "assets", "gemma-3-1b-it")
# GPU si disponible, sinon CPU.
device = 0 if torch.cuda.is_available() else -1
model_dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, clean_up_tokenization_spaces=False)
pipe = pipeline("text-generation", model=MODEL_PATH, tokenizer=tokenizer, device=device, dtype=model_dtype)
# Résoudre le conflit max_length=20 (generation_config du modèle) vs max_new_tokens=300
pipe.model.generation_config.max_length = None
pipe.model.generation_config.max_new_tokens = 300


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "resultat": None})


@app.post("/", response_class=HTMLResponse)
async def ask(request: Request, prompt: str = Form("")):
    prompt = (prompt or "").strip()
    resultat = None
    if prompt:
        messages = [{"role": "user", "content": prompt}]
        output = pipe(messages)
        try:
            resultat = output[0]["generated_text"][-1]["content"]
        except Exception:
            resultat = output[0].get("generated_text") or str(output)
    return templates.TemplateResponse("index.html", {"request": request, "resultat": resultat})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)