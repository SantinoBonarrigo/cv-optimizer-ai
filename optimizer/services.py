import json
import re
from groq import Groq
from django.conf import settings


def analyze_cv(job_offer: str, cv_text: str) -> dict:
    """
    Sends the CV and job offer to Groq and parses the response.
    Returns a dict with: match_score (int), missing_keywords (list), suggestions (list).
    """
    client = Groq(api_key=settings.GROQ_API_KEY)

    prompt = f"""You are an expert in recruitment and CV optimization.
Analyze the following CV against the job offer and return ONLY a valid JSON object with this exact structure:

{{
  "match_score": <integer between 0 and 100>,
  "missing_keywords": [<list of strings with important keywords from the job offer that are NOT present in the CV>],
  "suggestions": [<list of strings with concrete suggestions to improve the CV>]
}}

JOB OFFER:
{job_offer}

CANDIDATE CV:
{cv_text}

Respond ONLY with the JSON — no extra text, no markdown, no explanations."""

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1024,
    )

    raw = response.choices[0].message.content.strip()

    # Strip possible markdown code fences (```json ... ```)
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    data = json.loads(raw)

    return {
        "match_score": int(data["match_score"]),
        "missing_keywords": data["missing_keywords"],
        "suggestions": data["suggestions"],
    }
