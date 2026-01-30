import subprocess
import urllib.parse


def open_url(url):
    """Open a URL in the default browser."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    subprocess.run(["open", url])
    return f"Opening {url} in your browser."


def open_youtube(query=None):
    """Open YouTube, optionally searching for something."""
    if query:
        encoded = urllib.parse.quote(query)
        url = f"https://www.youtube.com/results?search_query={encoded}"
    else:
        url = "https://www.youtube.com"

    subprocess.run(["open", url])
    return f"Opening YouTube{' search for ' + query if query else ''}."


def open_github():
    """Open GitHub."""
    subprocess.run(["open", "https://github.com"])
    return "Opening GitHub."
