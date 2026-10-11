"""
app.py — Routes only.
Receives the request, calls parser, calls analyzer, returns response.
"""

import os
import shutil
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from parser import parse_resume
from analyzer import analyze_resume
from prompt import SYSTEM_PROMPT, build_prompt

# ── App setup ────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Resume Analyser",
    description="AI-powered ATS resume analysis using Claude.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Serve the frontend."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@app.get("/health")
def health():
    """Quick check that the server is running."""
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    job_description: str = Form(default=""),
):
    """
    Main route.
    1. Save uploaded file temporarily.
    2. Call parser  → extract plain text.
    3. Call analyzer → get AI feedback from Claude.
    4. Return structured JSON response.
    """

    # ── Step 1: Save file temporarily ────────────────────────────────────────
    allowed_types = {"application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a .pdf or .docx file."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ── Step 2: Parse ─────────────────────────────────────────────────────────
    try:
        resume_text = parse_resume(file_path)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=422, detail=f"Could not parse file: {str(e)}")

    # ── Step 3: Analyze ───────────────────────────────────────────────────────
    try:
        result = analyze_resume(resume_text, job_description)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=502, detail=f"Analysis failed: {str(e)}")

    # ── Step 4: Cleanup & return ──────────────────────────────────────────────
    os.remove(file_path)
    return result


@app.post("/analyze-text")
def analyze_text(
    resume_text: str = Form(...),
    job_description: str = Form(default=""),
):
    """
    Same as /analyze but accepts raw pasted text instead of a file.
    Useful for testing or when the user prefers to paste.
    """
    if len(resume_text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Resume text is too short.")

    result = analyze_resume(resume_text, job_description)
    return result