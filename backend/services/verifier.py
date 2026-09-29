import json
from difflib import SequenceMatcher
from urllib.parse import urlparse
from datetime import datetime, timezone

from ..schemas import VerifyRequest, VerifyResponse
from .groq_service import analyze_text
from .search_service import search_service
from .sanitize import (
    clean_str, clean_score, clean_str_list, clean_sources,
    clean_claims, clean_timeline, clean_platforms,
)

print("✅ verifier.py is running")


def get_source_from_url(url: str) -> str:
    """
    Extract clean website name from a URL.
    Example:
    https://www.bbc.com/news -> bbc.com
    https://m.youtube.com/... -> youtube.com
    """
    if not url:
        return "Unknown"

    try:
        domain = urlparse(url).netloc.lower()

        for prefix in ("www.", "m.", "mobile.", "amp."):
            if domain.startswith(prefix):
                domain = domain[len(prefix):]

        return domain or "Unknown"

    except Exception:
        return "Unknown"
def similarity(a: str, b: str) -> float:
    """Return similarity score between two strings."""
    return SequenceMatcher(None, (a or "").lower(), (b or "").lower()).ratio()


def find_best_match(ai_source, search_results):
    """
    Match an AI evidence item with the correct search result.
    Priority:
    1. Exact URL
    2. Highest title similarity
    """
    ai_url = (ai_source.get("url") or "").strip()
    ai_title = (ai_source.get("title") or "").strip()

    # 1. Exact URL match
    if ai_url:
        for item in search_results:
            if (item.get("url") or "").strip() == ai_url:
                return item

    # 2. Best title match
    best_item = None
    best_score = 0.0

    for item in search_results:
        score = similarity(ai_title, item.get("title", ""))
        if score > best_score:
            best_score = score
            best_item = item

    # Accept only good matches
    if best_score >= 0.55:
        return best_item

    return None

def verify_content(request: VerifyRequest) -> VerifyResponse:

    if request.type == "news":

        # Collect evidence
        evidence = search_service.search(request.input)

        print("\n========== DEBUNKIFY EVIDENCE ==========\n")
        print(json.dumps(evidence, indent=2))
        print("\n========================================\n")

        # AI analysis
        result = analyze_text(
            text=request.input,
            evidence=evidence,
        )

        # Evidence returned by Groq
        evidence_sources = [
            item for item in (result.get("evidence_sources") or [])
            if isinstance(item, dict)
        ] if isinstance(result.get("evidence_sources"), list) else []

        # Merge Groq output with search results
        if evidence_sources:

            for source in evidence_sources:

                search_item = find_best_match(source, evidence)
                
                if not search_item:
                  continue

                url = search_item.get("url", "")

                # Always derive source from URL when available
                if url:
                    source["source"] = get_source_from_url(url)
                elif (
                    not source.get("source")
                    or source.get("source") == "Unknown"
                ):
                    source["source"] = search_item.get("source", "Unknown")

                if not source.get("url"):
                    source["url"] = url

                if not source.get("snippet"):
                    source["snippet"] = search_item.get("snippet", "")

                if not source.get("published_date"):
                    source["published_date"] = search_item.get(
                        "published_date", ""
                    )

                if (
                    not source.get("credibility")
                    or source.get("credibility") == "Unknown"
                ):
                    source["credibility"] = search_item.get(
                        "credibility", "Unknown"
                    )

        else:

            evidence_sources = [
                {
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("snippet", ""),
                    "source": get_source_from_url(item.get("url", "")),
                    "credibility": item.get("credibility", "Unknown"),
                    "published_date": item.get("published_date", ""),
                }
                for item in evidence
            ]

        print("\n========== FINAL EVIDENCE ==========\n")
        print(json.dumps(evidence_sources, indent=2))
        print("\n====================================\n")
        return VerifyResponse(
            success=True,

            trust_score=clean_score(result.get("trust_score"), 50),
            verdict=clean_str(result.get("verdict"), "Uncertain") or "Uncertain",
            summary=clean_str(result.get("summary")),
            risk_level=clean_str(result.get("risk_level"), "Medium") or "Medium",

            sources_checked=len(evidence),

            last_verified=datetime.now(timezone.utc).isoformat(),

            executive_summary=clean_str(result.get("executive_summary")),

            key_findings=clean_str_list(result.get("key_findings")),

            suspicious_claims=clean_claims(result.get("suspicious_claims")),

            triggered_indicators=clean_str_list(result.get("triggered_indicators")),

            evidence_sources=clean_sources(evidence_sources),

            claim_timeline=clean_timeline(result.get("claim_timeline")),

            similar_claims=clean_str_list(result.get("similar_claims")),

            spreading_on=clean_platforms(result.get("spreading_on")),

            recommendations=clean_str_list(result.get("recommendations")),
        )

    elif request.type == "image":

        return VerifyResponse(
            success=False,

            trust_score=0,
            verdict="Unsupported",

            summary="Use the /verify/image endpoint for image verification.",

            risk_level="Unknown",

            sources_checked=0,

            last_verified=datetime.now(timezone.utc).isoformat(),

            executive_summary="",

            key_findings=[],

            suspicious_claims=[],

            triggered_indicators=[],

            evidence_sources=[],

            claim_timeline=[],

            similar_claims=[],

            spreading_on=[],

            recommendations=[],
        )

    return VerifyResponse(
        success=False,

        trust_score=0,

        verdict="Unsupported",

        summary=f"Verification type '{request.type}' is not supported.",

        risk_level="Unknown",

        sources_checked=0,

        last_verified=datetime.now(timezone.utc).isoformat(),

        executive_summary="",

        key_findings=[],

        suspicious_claims=[],

        triggered_indicators=[],

        evidence_sources=[],

        claim_timeline=[],

        similar_claims=[],

        spreading_on=[],

        recommendations=[],
    )