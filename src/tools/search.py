from duckduckgo_search import DDGS

def search_web(query, max_results=3):
    """AXIOM searches the web autonomously"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            
        if not results:
            return "I couldn't find anything on that."

        # Format results cleanly
        summary = ""
        for r in results:
            summary += f"Title: {r['title']}\n"
            summary += f"Info: {r['body']}\n\n"

        return summary

    except Exception as e:
        return f"Search failed: {str(e)}"
