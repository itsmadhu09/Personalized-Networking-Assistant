"""
fact_checker.py
------------------
Wikipedia API integration: quick reference lookups for fact-checking
topics before a networking event.
"""

import wikipediaapi

_wiki = wikipediaapi.Wikipedia(
    user_agent="PersonalizedNetworkingAssistant/1.0 (student-project)",
    language="en",
)


def check_fact(query: str, sentence_count: int = 3) -> dict:
    """
    Look up `query` on Wikipedia and return a short summary.
    Returns found=False if no matching page exists.
    """
    page = _wiki.page(query)

    if not page.exists():
        return {
            "query": query,
            "summary": "No Wikipedia page found for this query. Try a more specific or differently worded term.",
            "source_url": None,
            "found": False,
        }

    summary_sentences = page.summary.split(". ")
    short_summary = ". ".join(summary_sentences[:sentence_count]).strip()
    if short_summary and not short_summary.endswith("."):
        short_summary += "."

    return {
        "query": query,
        "summary": short_summary,
        "source_url": page.fullurl,
        "found": True,
    }
