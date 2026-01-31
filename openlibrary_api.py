import requests
API_HEADERS = {
    "User-Agent": "BookManager/1.0 (maxtp26@gmail.com)"
}
def search_book(query):
    try:
        request = requests.get(f"https://openlibrary.org/search.json?q={query}&fields=key,title,author_name,publish_date,editions&lang=en", headers=API_HEADERS)
    except Exception:
        return None
    request_dict = request.json()
    try:
        author = request_dict["docs"][0]["author_name"][0]
    except (KeyError, IndexError, TypeError):
        author = None
    try:
        title = request_dict["docs"][0]["title"]
    except (KeyError, IndexError, TypeError):
        title = None
    try:
        year = request_dict["docs"][0]["publish_date"][0]
    except (KeyError, IndexError, TypeError):
        year = None
    try:
        edition_key = request_dict["docs"][0]["editions"]["docs"][0]["key"]
        print(edition_key)
        try:
            edition_request = requests.get(f"https://openlibrary.org{edition_key}.json", headers=API_HEADERS)
        except requests.exceptions.RequestException:
            return None
        edition_request_dict = edition_request.json()
        if "publishers" in edition_request_dict:
            publisher = edition_request_dict["publishers"][0]
        else: 
            publisher = None
        if "isbn_13" in edition_request_dict:
            isbn = edition_request_dict["isbn_13"][0]
        elif "isbn_10" in edition_request_dict:
            isbn = edition_request_dict["isbn_10"][0]
        else:
            isbn = None
    except (KeyError, IndexError, TypeError):
        publisher = None
        isbn = None
    return {"isbn": isbn, "title": title, "author": author, "publisher": publisher, "year": year}
