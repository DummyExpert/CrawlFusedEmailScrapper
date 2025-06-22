import re

EMAIL_REGEX = r'[a-zA-Z0-9.\-+_]+@[a-zA-Z0-9.\-+_]+\.[a-zA-Z]+'

def extract_emails_from_html(html: str) -> set[str]:
    """Return a set of emails found within the given HTML string."""
    return set(re.findall(EMAIL_REGEX, html))
