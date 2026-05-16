from ddgs import DDGS
from datetime import datetime

def search_web(query, max_results=3):
    """AXIOM searches the web autonomously"""
    try:
        current_year = datetime.now().year
        if str(current_year) not in query and str(current_year-1) not in query:
            query = f"{query} {current_year}"

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return "No results found."

        summary = ""
        for r in results:
            summary += f"Title: {r['title']}\n"
            summary += f"Info: {r['body']}\n\n"

        return summary

    except Exception as e:
        return f"Search failed: {str(e)}"
