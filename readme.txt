# Google Books Microservice

This microservice allows you to query the Google Books API programmatically via ZeroMQ. It acts as an intermediary, handling requests and formatting responses for your application.
Make sure to connect the server to whatever you prefer, right now we are just using localhost @ 5555.

## How It Works
- The **Client** sends a request to the microservice via a ZeroMQ `REQ` socket.
- The **Server** processes the request, queries the Google Books API, and returns the results to the client via a ZeroMQ `REP` socket.

---

## Prerequisites
1. Install the required Python packages:
   ```bash
   pip install pyzmq requests
   ```

2. Ensure the Google Books API is enabled and the API key is configured in the server script (`book_info_service.py`).

---

## Requesting Data
To request data from the microservice:

1. Connect to the server via ZeroMQ at `tcp://localhost:5555`.
2. Send a JSON object with the following structure:
   ```json
   {
       "query": "search term here",
       "search_type": "intitle" // or "inauthor" or "isbn"
   }
   ```

### Example Request (Python)
Here’s how to send a request programmatically:

```python
import zmq

# Create a ZeroMQ context and REQ socket
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")  # Connect to the microservice

# Prepare the request
request = {
    "query": "Star Wars",
    "search_type": "intitle"
}

# Send the request
socket.send_json(request)

# Wait for a response
response = socket.recv_json()
print("Response:", response)
```

---

## Receiving Data
The microservice will return a JSON response containing the requested book data. The response structure is as follows:
- For successful requests, you will receive a list of book objects:
  ```json
  [
      {
          "title": "Book Title",
          "authors": ["Author Name"],
          "publisher": "Publisher Name",
          "publishedDate": "2024-01-01",
          "description": "Book description...",
          "pageCount": 300,
          "categories": ["Fiction"],
          "averageRating": 4.5,
          "thumbnail": "http://example.com/thumbnail.jpg"
      },
      ...
  ]
  ```
- For failed requests, you will receive an error object:
  ```json
  {
      "error": "API request failed with status code 403"
  }
  ```

### Example Response Handling (Python)
Here’s how to receive and process the response programmatically:

```python
# Wait for the server's response
response = socket.recv_json()

# Process the response
if isinstance(response, list):
    for idx, book in enumerate(response, start=1):
        print(f"Book {idx}:")
        print(f"  Title: {book['title']}")
        print(f"  Authors: {book['authors']}")
        print(f"  Publisher: {book['publisher']}")
        print(f"  Published Date: {book['publishedDate']}")
else:
    print("Error:", response.get("error"))
```

---

## Server Setup
1. Run the server script:
   ```bash
   python book_info_service.py
   ```

2. The server will start listening on `tcp://*:5555`.

---

## Client Setup
Use the provided example client (`client.py`) or implement your own using the above instructions.

---
