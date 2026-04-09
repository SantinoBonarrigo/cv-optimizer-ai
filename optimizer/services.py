import io
import json
import re
from groq import Groq
from pypdf import PdfReader
from django.conf import settings


def extract_pdf_text(pdf_file) -> str:
    """Extract plain text from an uploaded PDF file object."""
    reader = PdfReader(io.BytesIO(pdf_file.read()))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def analyze_cv(job_offer: str, cv_text: str) -> dict:
    """
    Sends the CV and job offer to Groq and parses the response.
    Returns a dict with all analysis fields.
    """
    client = Groq(api_key=settings.GROQ_API_KEY)

    prompt = f"""You are a senior technical recruiter and ATS specialist.
Analyze the following CV against the job offer and return ONLY a valid JSON object with this exact structure:

{{
  "match_score": <integer between 0 and 100 reflecting overall CV-to-job alignment>,
  "job_fit": <one of exactly: "Strong Match", "Moderate Match", "Weak Match">,
  "recommendation": <one of exactly: "Apply", "Apply with improvements", "Do not apply">,
  "explanation": <1-3 sentences explaining WHY this score, fit level, and recommendation were given — be specific about what aligns and what does not>,
  "missing_keywords": [<important technical or professional keywords from the job offer that are NOT present in the CV>],
  "suggestions": [<concrete CV improvement suggestions — always use conditional language: "If you have experience with X, consider adding it explicitly"; never invent experience>],
  "ats_friendly": <true if the CV appears well-structured for ATS parsing, false otherwise>,
  "ats_issues": [<specific structural or formatting problems that hurt ATS parsing, e.g. "No clear Skills section", "Dates formatted inconsistently">],
  "ats_tips": [<specific actionable tips to improve ATS compatibility, e.g. "Add a dedicated Skills section listing tools and technologies as plain text">]
}}

Rules you must follow:
- Do NOT invent skills, tools, or experience that are not present in the CV.
- Use conditional language for suggestions (e.g. "If you have worked with Docker, consider adding it to your Skills section").
- "ats_issues" and "ats_tips" must be empty lists when "ats_friendly" is true.
- "job_fit" and "recommendation" are qualitative judgments — they may reflect factors beyond the numeric score alone.

JOB OFFER:
{job_offer}

CANDIDATE CV:
{cv_text}

Respond ONLY with the JSON — no extra text, no markdown, no explanations."""

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2048,
    )

    raw = response.choices[0].message.content.strip()

    # Strip possible markdown code fences (```json ... ```)
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    data = json.loads(raw)

    return {
        "match_score": int(data["match_score"]),
        "job_fit": data["job_fit"],
        "recommendation": data["recommendation"],
        "explanation": data["explanation"],
        "missing_keywords": data["missing_keywords"],
        "suggestions": data["suggestions"],
        "ats_friendly": bool(data["ats_friendly"]),
        "ats_issues": data.get("ats_issues", []),
        "ats_tips": data.get("ats_tips", []),
    }
