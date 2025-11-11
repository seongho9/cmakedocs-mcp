import requests


cmake_root: str = "https://cmake.org/cmake/help"

def get_page(path: str) -> str:
    """Fetch a page and return raw HTML content"""
    res = requests.get(f"{cmake_root}/{path}")
    res.encoding = 'utf-8'
    return res.text
