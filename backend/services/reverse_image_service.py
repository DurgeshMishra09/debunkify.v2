import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def reverse_image_search(image_url):
    """
    Perform Google Lens reverse image search using SerpAPI
    and return only the useful information required by Debunkify.
    """

    url = "https://serpapi.com/search"

    params = {
        "engine": "google_lens",
        "url": image_url,
        "api_key": SERPAPI_KEY,
    }

    response = requests.get(url, params=params, timeout=60)

    if response.status_code != 200:
        raise Exception(f"SerpAPI Error: {response.text}")

    data = response.json()

    return {
        "search_information": data.get("search_information", {}),
        "knowledge_graph": data.get("knowledge_graph", {}),
        "exact_matches": data.get("exact_matches", []),
        "visual_matches": data.get("visual_matches", []),
        "related_content": data.get("related_content", []),
        "inline_images": data.get("inline_images", []),
    }