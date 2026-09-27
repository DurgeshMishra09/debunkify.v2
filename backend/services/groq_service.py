import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception as e:
    print("⚠️ Groq client could not be initialised:", e)
    client = None


def analyze_text(text: str, evidence: list):

    prompt = f"""
You are Debunkify AI.

You are a professional fact-checking investigator.

Analyse the user's content carefully.

Use the supplied evidence whenever available.

Never fabricate evidence or URLs.

Return ONLY valid JSON.

No markdown.
No explanations.
No extra text.

SCORING RULES

trust_score must be an integer between 0 and 100.

90-100 = Verified

70-89 = Likely True

40-69 = Uncertain

20-39 = Misleading

0-19 = Fake

Populate every possible field.

Return at least:

• 3 key findings

• 3 recommendations

• 2 triggered indicators

If no evidence exists,
return an empty evidence_sources array.

If no timeline can be inferred,
return an empty claim_timeline array.

SPREADING ON RULES

Estimate how widely this claim is currently spreading on different platforms based ONLY on the supplied evidence.

Return ONLY platforms that are supported by the available evidence.

For each platform return:

- platform
- spread_percentage

Rules:

- spread_percentage must be an integer from 0 to 100.
- The percentage is an estimate of how much the claim is circulating on that platform according to the available evidence.
- Do NOT invent platforms.
- Do NOT return duplicate platforms.
- If there is insufficient evidence for a platform, do not include it.
- If no platform can be determined, return an empty array.

Evidence available:

{json.dumps(evidence, indent=2)}

User Content:

{text}

Return JSON in EXACTLY this format:

{{
  "trust_score": 95,

  "verdict": "Verified",

  "summary": "One sentence summary.",

  "risk_level": "Low",

  "executive_summary": "Detailed executive summary.",

  "key_findings": [
    "Finding 1",
    "Finding 2",
    "Finding 3"
  ],

  "suspicious_claims": [
    {{
      "claim": "Claim",
      "reason": "Why it is suspicious",
      "confidence": "High"
    }}
  ],

  "triggered_indicators": [
    "Indicator 1",
    "Indicator 2"
  ],

  "evidence_sources": [
    {{                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
      "title": "Source title",
      "url": "https://example.com",
      "snippet": "Relevant snippet"
    }}
  ],

  "claim_timeline": [
    {{
      "date": "2026-07-25",
      "event": "Timeline event"
    }}
  ],

  "similar_claims": [
    "Claim 1",
    "Claim 2"
  ],

  "spreading_on": [
  {{
    "platform": "Facebook",
    "spread_percentage": 94
  }},
  {{
    "platform": "WhatsApp",
    "spread_percentage": 87
  }},
  {{
    "platform": "YouTube",
    "spread_percentage": 56
  }}
],

  "recommendations": [
    "Recommendation 1",
    "Recommendation 2",
    "Recommendation 3"
  ]
}}
"""

    if client is None:
        return {
            "trust_score": 0,
            "verdict": "Unclear",
            "summary": "Verification is unavailable because the GROQ_API_KEY is missing or invalid on the server.",
            "risk_level": "Unknown",
            "executive_summary": "The backend could not reach the Groq analysis service because it has no valid API key configured. Set GROQ_API_KEY in the backend environment and restart the server.",
            "key_findings": [],
            "suspicious_claims": [],
            "triggered_indicators": [],
            "evidence_sources": [],
            "claim_timeline": [],
            "similar_claims": [],
            "spreading_on": [],
            "recommendations": []
        }

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Debunkify AI. "
                        "Always return valid JSON only."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )
    except Exception as e:
        print("Groq API Error:", e)
        return {
            "trust_score": 0,
            "verdict": "Unclear",
            "summary": f"Verification failed: {e}",
            "risk_level": "Unknown",
            "executive_summary": "The request to the Groq analysis service failed, so no verdict could be produced. This is usually caused by a missing/invalid GROQ_API_KEY, an unavailable model, or a network error on the server.",
            "key_findings": [],
            "suspicious_claims": [],
            "triggered_indicators": [],
            "evidence_sources": [],
            "claim_timeline": [],
            "similar_claims": [],
            "spreading_on": [],
            "recommendations": []
        }

    result = response.choices[0].message.content.strip()

    if result.startswith("```json"):
        result = result.replace("```json", "").replace("```", "").strip()

    elif result.startswith("```"):
        result = result.replace("```", "").strip()

    try:
        data = json.loads(result)

        data.setdefault("trust_score", 50)
        data.setdefault("verdict", "Uncertain")
        data.setdefault("summary", "")
        data.setdefault("risk_level", "Medium")
        data.setdefault("executive_summary", "")
        data.setdefault("key_findings", [])
        data.setdefault("suspicious_claims", [])
        data.setdefault("triggered_indicators", [])
        data.setdefault("evidence_sources", [])
        data.setdefault("claim_timeline", [])
        data.setdefault("similar_claims", [])
        data.setdefault("spreading_on", [])
        data.setdefault("recommendations", [])

        return data

    except Exception:

        return {
            "trust_score": 50,
            "verdict": "Uncertain",
            "summary": "Unable to analyse the content.",
            "risk_level": "Medium",
            "executive_summary": "",
            "key_findings": [],
            "suspicious_claims": [],
            "triggered_indicators": [],
            "evidence_sources": [],
            "claim_timeline": [],
            "similar_claims": [],
            "spreading_on": [],
            "recommendations": []
        }
