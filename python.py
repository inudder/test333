#!/usr/bin/env python3
import sys
from urllib.parse import urlparse
from publicsuffix2 import PublicSuffixList, fetch

# ── качаем Public Suffix List один раз, затем держим его в памяти ──
psl = PublicSuffixList(fetch())

def root_domain(url: str) -> str:
    # если протокол не указан, добавляем, чтобы urlparse не промахнулся
    if not url.startswith(('http://', 'https://', 'ftp://')):
        url = 'http://' + url

    host = urlparse(url).hostname or ''

    # новые версии (≥ 2.0)
    if hasattr(psl, 'get_registered_domain'):
        result = psl.get_registered_domain(host)
    # старые версии (1.x)
    elif hasattr(psl, 'get_sld'):
        result = psl.get_sld(host)
    else:           # совсем старая 0.x
        result = psl.get_public_suffix(host)

    return result or host       # если почему-то не нашли — вернём сам host

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: rootdomain.py <url>')
        sys.exit(1)

    print(root_domain(sys.argv[1]))
