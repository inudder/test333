#!/usr/bin/env python3
import sys
from publicsuffix2 import PublicSuffixList, fetch

psl = PublicSuffixList(fetch())          # скачиваем PSL один раз

def registrable(url: str) -> str:
    if not url.startswith(("http://", "https://", "ftp://")):
        url = "http://" + url           # чтобы urlparse не упал
    from urllib.parse import urlparse
    host = urlparse(url).hostname or ""
    return psl.get_registry(host, include_private=False, strict=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: rootdomain.py <url>")
        sys.exit(1)
    print(registrable(sys.argv[1]))
