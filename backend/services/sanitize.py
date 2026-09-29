"""Defensive cleaning of AI-generated data before it is validated by the response schema.

LLM output is unreliable: numbers arrive as "85%" or 85.5, strings arrive as null, lists contain
dicts or strings by mistake. One bad field used to make the whole verification fail with a 500.
Everything here is plain Python (no third-party imports) so it is easy to test on its own.
"""


def clean_str(value, default=""):
    if isinstance(value, bool) or value is None:
        return default
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)):
        return str(value)
    return default


def clean_score(value, default=50):
    """Return an int in 0..100 from 85, 85.5, "85", "85%" ... else the default."""
    if isinstance(value, bool) or value is None:
        return default
    try:
        number = float(str(value).strip().rstrip("%").strip())
    except (TypeError, ValueError):
        return default
    if number != number or number in (float("inf"), float("-inf")):
        return default
    return max(0, min(100, int(round(number))))


def clean_str_list(value):
    if not isinstance(value, list):
        return []
    result = []
    for item in value:
        text = clean_str(item)
        if text:
            result.append(text)
    return result


def clean_sources(value):
    if not isinstance(value, list):
        return []
    result = []
    for item in value:
        if not isinstance(item, dict):
            continue
        if not clean_str(item.get("title")) and not clean_str(item.get("url")):
            continue  # nothing to show or link to
        result.append({
            "title": clean_str(item.get("title")),
            "url": clean_str(item.get("url")),
            "snippet": clean_str(item.get("snippet")),
            "source": clean_str(item.get("source")),
            "credibility": clean_str(item.get("credibility")),
            "published_date": clean_str(item.get("published_date")),
        })
    return result


def clean_claims(value):
    if not isinstance(value, list):
        return []
    result = []
    for item in value:
        if not isinstance(item, dict):
            continue
        claim = clean_str(item.get("claim"))
        if not claim:
            continue
        result.append({
            "claim": claim,
            "reason": clean_str(item.get("reason")),
            "confidence": clean_str(item.get("confidence")),
        })
    return result


def clean_timeline(value):
    if not isinstance(value, list):
        return []
    result = []
    for item in value:
        if not isinstance(item, dict):
            continue
        event = clean_str(item.get("event"))
        if event:
            result.append({"date": clean_str(item.get("date")), "event": event})
    return result


def clean_platforms(value):
    if not isinstance(value, list):
        return []
    result = []
    for item in value:
        if not isinstance(item, dict):
            continue
        platform = clean_str(item.get("platform"))
        if platform:
            result.append({"platform": platform, "spread_percentage": clean_score(item.get("spread_percentage"), 0)})
    return result
