"""
services/prompt.py
Builds the system prompt and user prompt sent to Claude.
Keeping prompts here means you can tune them without touching any other file.
"""


# ── System prompt ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an expert ATS (Applicant Tracking System) analyst and senior career coach
with 15 years of experience reviewing resumes for Fortune 500 hiring pipelines.

Your job is to evaluate resumes exactly the way an ATS parser would — checking
structure, headings, keyword density, formatting signals, and readability — then
provide specific, actionable coaching feedback.

Rules you must follow:
- Respond with ONLY valid JSON. No markdown, no code fences, no commentary.
- Be specific: never say "good" or "bad" without explaining exactly what you saw.
- Every improvement must start with an action verb (Add, Remove, Replace, Move, etc.).
- Score honestly — do not inflate scores to be encouraging."""


# ── User prompt builder ───────────────────────────────────────────────────────

def build_prompt(resume_text: str, job_description: str = "") -> str:
    """
    Build the full user message sent to Claude.
    Includes the resume, optional job description, and the exact JSON schema to return.
    """
    jd_block = _build_jd_block(job_description)

    return f"""Analyze the resume below for ATS (Applicant Tracking System) compatibility.

═══ RESUME TEXT ═══
{resume_text[:6000]}

═══ JOB DESCRIPTION ═══
{jd_block}

═══ INSTRUCTIONS ═══
Return a single JSON object matching EXACTLY this schema (no extra fields):

{{
  "ats_score": <integer 0–100>,
  "verdict": "<one of: ATS-Friendly | Minor Issues | Needs Work | ATS-Incompatible>",
  "summary": "<2–3 sentences: what the ATS will see, overall strengths, biggest risk>",

  "sections": [
    {{
      "section": "<name>",
      "status": "<pass | warn | fail>",
      "feedback": "<1–2 sentences — what you found, what to fix>"
    }}
  ],

  "improvements": [
    "<specific action — start with a verb>",
    "<specific action — start with a verb>"
  ],

  "keyword_matches": <list of skill/keyword strings found in BOTH resume and JD, or null if no JD>,
  "keyword_missing": <list of important JD keywords absent from resume, or null if no JD>,

  "red_flags": [
    "<any serious ATS issues e.g. tables, columns, graphics, missing sections>"
  ]
}}

Sections to evaluate (include ALL of these in the sections array):
  1. Contact Information   — email, phone, LinkedIn in plain text near top
  2. Professional Summary  — present, relevant, keyword-rich
  3. Work Experience       — standard heading, reverse chronological, dates, bullet points
  4. Education             — present, standard heading, dates included
  5. Skills                — dedicated section, plain list or simple bullets (not icons/bars)
  6. Formatting & Structure — single column, standard fonts, no tables, no graphics
  7. File Readability      — check for garbled characters, extraction artifacts, missing words

Score guide:
  85–100 → ATS-Friendly       (clean, parseable, strong keywords)
  65–84  → Minor Issues       (mostly good, one or two fixable problems)
  40–64  → Needs Work         (multiple problems that will confuse parsers)
  0–39   → ATS-Incompatible   (severe formatting or content failures)"""


# ── Private helpers ───────────────────────────────────────────────────────────

def _build_jd_block(job_description: str) -> str:
    if not job_description or not job_description.strip():
        return "(No job description provided — skip keyword_matches and keyword_missing, set both to null)"

    # Trim to avoid burning too many tokens on a very long JD
    trimmed = job_description.strip()[:3000]
    if len(job_description.strip()) > 3000:
        trimmed += "\n[truncated for length]"

    return trimmed