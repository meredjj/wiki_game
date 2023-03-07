excluded_links = ["Special:", "File:", "Category:",
                      "MOS:", "Portal:", "Wikipedia:",
                      "Help:", "Talk:", "Wikipedia_talk:",
                      "Template:", "Template_talk:",
                      "Main_Page", "User:"]

wiki_base = "https://en.wikipedia.org/wiki/"

def valid_url(url: str, visited: dict) -> bool:
    """
    Validate that a given wikipedia URL is compatible with the wiki game
    """
    if wiki_base not in url:
        return False
    if url == wiki_base:
        return False
    if visited is not None:
        if url in visited:
            return False
    for val in excluded_links:
        if val in url:
            return False
    return True