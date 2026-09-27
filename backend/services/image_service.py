import json
import os
import tempfile

from dotenv import load_dotenv
from groq import Groq

from .cloudinary_service import upload_image
from .reverse_image_service import reverse_image_search

load_dotenv()

try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception as e:
    print("⚠️ Groq client could not be initialised:", e)
    client = None


def analyze_uploaded_image(upload_file):
    """
    Debunkify Reverse Image Search

    Flow

    Upload Image
            ↓
    Cloudinary
            ↓
    Google Lens
            ↓
    Groq Investigation
            ↓
    Investigation Report
    """

    suffix = os.path.splitext(upload_file.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp:

        temp.write(upload_file.file.read())

        temp_path = temp.name

    try:

        if client is None:
            raise Exception(
                "Image analysis is unavailable because the GROQ_API_KEY is "
                "missing or invalid on the server."
            )

        # ------------------------------------
        # Upload Image
        # ------------------------------------

        upload_result = upload_image(temp_path)

        image_url = upload_result["url"]

        # ------------------------------------
        # Reverse Image Search
        # ------------------------------------

        serp_result = reverse_image_search(image_url)

        search_information = serp_result.get(
            "search_information",
            {}
        )

        knowledge_graph = serp_result.get(
            "knowledge_graph",
            {}
        )

        exact_matches = serp_result.get(
            "exact_matches",
            []
        )[:5]

        visual_matches = serp_result.get(
            "visual_matches",
            []
        )[:10]

        related_content = serp_result.get(
            "related_content",
            []
        )[:10]

        # ------------------------------------
        # Dynamically Calculate Confidence Score
        # ------------------------------------
        # Formula based on quantity and quality of search hits found
        match_count = len(exact_matches) + len(visual_matches) + len(related_content)
        has_knowledge_graph = 1 if knowledge_graph else 0
        
        # Base calculation
        calculated_score = min(95, max(15, (match_count * 6) + (has_knowledge_graph * 25)))
        if match_count == 0:
            calculated_score = 10

        # ------------------------------------
        # Prepare compact investigation data
        # ------------------------------------

        compact_data = {
            "best_guess": search_information,

            "knowledge_graph": knowledge_graph,

            "exact_matches": [
                {
                    "title": item.get("title"),
                    "source": item.get("source"),
                    "snippet": item.get("snippet"),
                    "url": item.get("url") or item.get("link"),
                }
                for item in exact_matches
            ],

            "visual_matches": [
                {
                    "title": item.get("title"),
                    "source": item.get("source"),
                    "snippet": item.get("snippet"),
                    "url": item.get("url") or item.get("link"),
                }
                for item in visual_matches
            ],

            "related_content": [
                {
                    "title": item.get("title"),
                    "source": item.get("source"),
                    "snippet": item.get("snippet"),
                    "url": item.get("url") or item.get("link"),
                }
                for item in related_content
            ]
        }

        # ------------------------------------
        # AI Investigation Prompt
        # ------------------------------------

        prompt = f"""
You are Debunkify AI.

You are an expert in:

- Reverse Image Search
- OSINT
- Digital Investigation
- Fact Checking
- Misinformation Detection

IMPORTANT

Do NOT analyse whether the image is AI-generated.

Do NOT analyse whether the image is edited.

That belongs to another Debunkify feature.

Your job is ONLY to investigate the history and context of the uploaded image.

Return ONLY valid JSON matching this exact structure:

{{
    "confidence_score": {calculated_score},

    "image_category": "",

    "image_subject": "",

    "verdict": "",

    "summary": "",

    "original_context": "",

    "first_seen": "",

    "last_seen": "",

    "executive_summary": "",

    "key_findings": [],

    "original_sources": [],

    "timeline": [],

    "false_claims": [],

    "viral_platforms": [
        {{
            "platform": "Example Platform Name",
            "spread_percentage": 85
        }}
    ],

    "recommendations": []
}}

Instructions

1. Use the pre-calculated confidence_score provided above ({calculated_score}). Do not change it.

2. First classify the uploaded image.

Possible image_category values:

- Celebrity
- Person
- Landmark
- Monument
- Building
- Nature
- Animal
- Vehicle
- Food
- Document
- Product
- Artwork
- Meme
- Screenshot
- Logo
- Infographic
- Unknown

3.image_subject should contain the specific name.

Examples:

Celebrity → Virat Kohli

Landmark → Taj Mahal

Monument → India Gate

Person → Unknown Person

Animal → Bengal Tiger

Document → Aadhaar Card

Logo → OpenAI Logo

Meme → Drake Meme

Nature → Sunset Beach

4. Identify the original context.

5. The executive_summary must be detailed (120–200 words).

It should read like a professional investigation report and include:

- What the uploaded image appears to depict.
- The identified subject and image category.
- The likely original context or purpose of the image.
- Whether reliable reverse image search results were found.
- Whether the image has appeared on multiple websites or platforms.
- Any important historical context.
- Whether there is evidence of misleading use or false claims.
- A concise overall conclusion about the image's authenticity and context.

Write in natural, professional English. Do not use bullet points. Return a single well-structured paragraph.

6. Estimate when the image first appeared.

7. Mention the latest appearance.

8. List trustworthy original sources.

9. Detect misleading captions or false claims.

10. Build a timeline if possible.

11. Estimate major platforms where the image spread, providing each platform as an object containing "platform" (string) and "spread_percentage" (integer from 0 to 100).

12. Never invent facts. If info is unavailable, return "Unknown".

Return only valid JSON.

Google Lens Investigation Data

{json.dumps(compact_data, indent=2)}
"""
        # ------------------------------------
        # AI Investigation
        # ------------------------------------

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            temperature=0.3,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        text = response.choices[0].message.content.strip()

        if text.startswith("```json"):
            text = (
                text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        elif text.startswith("```"):
            text = (
                text
                .replace("```", "")
                .strip()
            )

        # ------------------------------------
        # Parse JSON
        # ------------------------------------

        try:

            result = json.loads(text)

        except Exception:

            result = {
                "confidence_score": calculated_score,

                "image_category": "Unknown",

                "image_subject": "Unknown",

                "verdict": "Unknown",

                "summary": text,

                "original_context": "Unknown",

                "first_seen": "Unknown",

                "last_seen": "Unknown",

                "executive_summary": "A detailed professional investigation summary of approximately 120–200 words.",

                "key_findings": [],

                "original_sources": [],

                "timeline": [],

                "false_claims": [],

                "viral_platforms": [],

                "recommendations": []
            }

        # Force enforce the computed score so it's guaranteed to be unique per image search volume
        result["confidence_score"] = calculated_score

        result.setdefault("image_category", "Unknown")
        result.setdefault("image_subject", "Unknown")

        result["success"] = True

        # ------------------------------------
        # Attach raw search data
        # ------------------------------------

        result["search_information"] = search_information
        result["knowledge_graph"] = knowledge_graph
        result["exact_matches"] = exact_matches
        result["visual_matches"] = visual_matches
        result["related_content"] = related_content

        return result

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
            "confidence_score": 0,
            "image_category": "Unknown",
            "image_subject": "Unknown",
            "verdict": "Error",
            "summary": "Unable to investigate the uploaded image.",
            "original_context": "Unknown",
            "first_seen": "Unknown",
            "last_seen": "Unknown",
            "executive_summary": "",
            "key_findings": [],
            "original_sources": [],
            "timeline": [],
            "false_claims": [],
            "viral_platforms": [],
            "recommendations": [],
            "search_information": {},
            "knowledge_graph": {},
            "exact_matches": [],
            "visual_matches": [],
            "related_content": []
        }

    finally:

        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass
