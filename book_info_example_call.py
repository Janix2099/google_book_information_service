import zmq

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")  # Connect to the microservice

    print("Welcome to the Google Books Client!")
    print("You can search for books by the following options:")
    print("1. Title")
    print("2. Author")
    print("3. ISBN")

    # Prompt user for input
    search_type_input = input("Enter the number corresponding to your search type (1 for Title, 2 for Author, 3 for ISBN): ")
    search_types = {"1": "intitle", "2": "inauthor", "3": "isbn"}

    if search_type_input not in search_types:
        print("Invalid input. Exiting.")
        return

    search_type = search_types[search_type_input]
    query = input(f"Enter the {search_type.replace('intitle', 'title').replace('inauthor', 'author')} to search for: ")

    # Send request to the server
    request = {"query": query, "search_type": search_type}
    print(f"Sending request: {request}")
    socket.send_json(request)

    # Wait for response
    response = socket.recv_json()
    print("\nSearch Results:")
    if "error" in response:
        print(response["error"])
    elif len(response) > 0:
        for idx, book in enumerate(response, start=1):
            print(f"\nBook {idx}:")
            for key, value in book.items():
                print(f"{key.capitalize()}: {value}")
    else:
        print("No books found.")

if __name__ == "__main__":
    main()
