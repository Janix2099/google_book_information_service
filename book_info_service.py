import zmq
import requests

def search_google_books(query, api_key, search_type="intitle"):
    """
    Search for books using the Google Books API.
    """
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"{search_type}:{query}",
        "key": api_key,
        "maxResults": 10 #for brevity (EDIT AS NEEDED)
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        books = []
        for item in data.get("items", []):
            book_info = {
                "title": item["volumeInfo"].get("title"),
                "authors": item["volumeInfo"].get("authors"),
                "publisher": item["volumeInfo"].get("publisher"),
                "publishedDate": item["volumeInfo"].get("publishedDate"),
                "description": item["volumeInfo"].get("description"),
                "pageCount": item["volumeInfo"].get("pageCount"),
                "categories": item["volumeInfo"].get("categories"),
                "averageRating": item["volumeInfo"].get("averageRating"),
                "thumbnail": item["volumeInfo"].get("imageLinks", {}).get("thumbnail"),
            }
            books.append(book_info)
        return books
    else:
        return {"error": f"API request failed with status code {response.status_code}"}

def main():
    API_KEY = "AIzaSyAaxg8TK6jN8tNM4D2ZcY_g5cziQ6m3OG4"
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")  # Bind the server to port 5555 or any server of your choice

    print("Google Books microservice is running...")

    while True:
        # Receive the message
        message = socket.recv_json()
        print(f"Received request: {message}")

        # Extract query parameters
        query = message.get("query", "")
        search_type = message.get("search_type", "intitle")

        # Perform the search
        results = search_google_books(query, API_KEY, search_type)

        # Send the results back to the client
        socket.send_json(results)

if __name__ == "__main__":
    main()
