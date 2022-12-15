import socket

class TCPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket()

    def connect(self):
        self.client_socket.connect((self.host, self.port))

    def send(self, data):
        self.client_socket.send(data)

    def receive(self):
        return self.client_socket.recv(1024)

    def close(self):
        self.client_socket.close()

# Instantiate the client and connect to the server
client = TCPClient("localhost", 8000)
client.connect()

# Loop until the user types "exit" or "EXIT"
while True:
    try:
        # Prompt the user to enter a number
        num_titles = input("Enter the number of titles to receive (or 'exit' to quit): ")

        # Send the number of titles to the server
        client.send(num_titles.encode())

        # Check if the user wants to exit
        if num_titles.lower() == "exit":
            break

        # Receive the titles from the server
        titles = client.receive()

        # Convert the titles from a bytes object to a list object
        titles = titles.decode().split(",")

        # Print the titles

        # Printing a starting tag for the titles print
        print(f"- printing the first {num_titles} book titles -")
        
        #Create a title iterator to be used for enumerating the titles when printing them
        title_iterator = 1
        
        for title in titles:
            print(f"{title_iterator}. {title}")
            title_iterator += 1
            if int(title_iterator) > int(num_titles):
                break
        
        # Printing an ending tag for the titles print
        print("-------------------------------------")
    except BrokenPipeError as e:
        print("Connection to the server was lost:", e)

# Close the connection
client.close()
