import os


def generate_web_url(path: str) -> str:
    """
    Generates a web url, path must start with / or empty string if you only want the web url
    """
    return f"{os.getenv('UI_DOMAIN_NAME')}{path}"
