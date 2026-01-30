from duckduckgo_search import DDGS

def search_web(query):
    """Search the web using DuckDuckGo (HTML backend) and return the first result."""
    print(f"🌐 Searching the web for: {query}")
    try:
        # backend='html' is often more reliable against rate limits
        results = DDGS().text(query, max_results=1, backend="html")
        if results:
            first_result = results[0]
            return f"Here is what I found: {first_result['title']}. {first_result['body']} (Source: {first_result['href']})"
        else:
            return "I couldn't find any results for that query."
    except Exception as e:
        print(f"❌ Search error: {e}")
        return "I encountered an error while searching the web."
