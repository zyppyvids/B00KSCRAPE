import threading
import socket
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# The host and port to run the server on
# 'localhost' and 8000 by default.
# NOTE: If you change these you should change them in the PyClient.py file too.
HOST = "localhost"
PORT = 8000

# Print a welcome message
print(f"OPENED A SERVER ON {HOST} WITH PORT {PORT}.")

# The website to scrape data from
WEBSITE = "http://books.toscrape.com"

# Create a new socket object
server_socket = socket.socket()

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

# Function to handle a new client connection
def handle_client(client_socket):
    try:
        # Receive data from the client in a loop
        while True:
            # Receive data from the client
            request = client_socket.recv(1024)
            
            # If no data was received, the client has closed the connection
            if not request or request.decode().lower() == "exit":
                # Get current time to add to the output of the console
                current_time = datetime.now().strftime("%H:%M:%S")
                
                # Print a message when a client disconnects
                print(f"[{current_time}] Client disconnected: {address}")

                # We close current socket
                client_socket.close()
                break

            # Get data from the given website
            response = requests.get(WEBSITE)

            # Parse the request using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Extract the data from the website
            data = soup.find_all("h3")

            # Extract the titles from the data
            titles = [d.find("a")["title"] for d in data]

            # Extract the specified number of titles from the list of titles
            titles = titles[0:int(request.decode())]

            # Convert the list of titles to a bytes object
            titles = ",".join(titles).encode()

            # Send the titles to the client
            client_socket.send(titles)
    except Exception as e:
        print(e)

# Accept incoming connections in a loop
while True:
    # Accept a new client connection
    client_socket, address = server_socket.accept()
    
    # Get current time to add to the output of the console
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # Print a message when a new client connects
    print(f"[{current_time}] New client connected: {address}")

    # Create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))

    # Start the client thread
    client_thread.start()
