import requests
from .categories import PREDEFINED_CATEGORIES

def fetch_home_books(limit=10):
    res = requests.get(f'https://openlibrary.org/search.json?q=bestseller&limit={limit}')
    data = res.json()

    return [
        {
            "title": book.get("title"),
            "year": book.get("first_publish_year"),
            "pages": book.get("number_of_pages_median"),
            "cover": f"https://covers.openlibrary.org/b/id/{book['cover_i']}-M.jpg" if 'cover_i' in book else None,
            "bookLink": book.get("key")
        }
        for book in data.get("docs", [])
    ]



def search_books_service(query):
    res = requests.get(f"https://openlibrary.org/search.json?q={query}")
    data = res.json()

    return [
        {
            "title": book.get("title"),
            "year": book.get("first_publish_year"),
            "pages": book.get("number_of_pages_median"),
            "cover": f"https://covers.openlibrary.org/b/id/{book['cover_i']}-M.jpg" if 'cover_i' in book else None,
            "bookLink": book.get("key")
        }
        for book in data.get("docs", [])[:10]
    ]


import requests


def get_book_detail(book_link):
    url = f"https://openlibrary.org{book_link}.json"
    res = requests.get(url)

    if res.status_code != 200:
        return None

    data = res.json()
    return {
        "title": data.get("title"),
        "pages": data.get("number_of_pages"),
        "year": data.get("created", {}).get("value", "")[:4],
        "size": None,
        "lang": None,
        "cover": f"https://covers.openlibrary.org/b/id/{data.get('covers', [])[0]}-M.jpg" if data.get(
            "covers") else None,
        "categories": [{"tag": subject, "link": f"/category/{subject.replace(' ', '_')}"} for subject in
                       data.get("subjects", [])]
    }


def get_all_categories():
    return PREDEFINED_CATEGORIES


def fetch_books_by_category(category_link):
    url = f"https://openlibrary.org{category_link}.json?limit=10"
    res = requests.get(url)

    if res.status_code != 200:
        return []

    works = res.json().get("works", [])

    return [
        {
            "title": book.get("title"),
            "year": book.get("first_publish_year"),
            "pages": None,
            "cover": f"https://covers.openlibrary.org/b/id/{book['cover_id']}-M.jpg" if book.get("cover_id") else None,
            "bookLink": book.get("key"),
            "description": book.get("description") if isinstance(book.get("description"), str) else (
                book.get("description", {}).get("value") if isinstance(book.get("description"), dict) else None
            )
        }
        for book in works
    ]
