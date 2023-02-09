# A server should keep track of the total number of clients, allow clients to send messages and broadcast
# everyone. Below are some key functions you must implement:
# • You should implement a function named broadcast to notify everyone when a client joins (except
# the client who joined).
# • You should also implement a function called game where it will allow two clients to play rock,
# paper, scissors game.

import _thread as thread
import socket
import time

# Define the host and port
host, port = "127.0.0.1", 9091

# Create a socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

linje = "\n_______________________________________________________"

# Try to bind the socket to the host and port, if it fails close the program
try:
    # Bind the socket to the host and port
    serverSocket.bind((host, port))
    print("Serving on " + host + ":" + str(port) + "\n")
except socket.error:
    print("Failed to bind socket, maybe the port is already in use?")
    exit(1)
# Listen for connections
serverSocket.listen()


# This function handles the client connection, it sends the response to the client and closes the connection
def handleclient(clientSocket, clientIP):
    try:
        print("Started new thread for client" + str(
            clientIP) + linje)
        # Get the request
        clientRequest = clientSocket.recv(4096).decode()
        print(clientRequest)
        # Encode the response
        response = "Received request: " + clientRequest
        response = response.encode()
        # Send the response
        clientSocket.sendall(response)
        # Close the connection
        # clientSocket.close()
    except socket.error:
        print("Client " + str(addr) + " disconnected from the server")
        clients.remove(clientSocket)


def broadcast(clientSocket, clientIP):
    if len(clients) > 1:
        print("Broadcasting to everyone exept joined client")
        for client in clients:
            if client != clientSocket:
                broadcastMessage = "New client " + str(clientIP)
                try:
                    time.sleep(0.5)
                    client.send(broadcastMessage.encode())
                except socket.error:
                    print("Unable to send broacast message to " + str(client))


# Check if any clients have disconnected
def checkForConnections():
    global checkForConnectionsThread
    checkForConnectionsThread = True
    print("Started new thread to check for disconnected clients" + linje)
    while True:
        # Sleep for 2 seconds
        time.sleep(2)
        for client in clients:
            try:
                # client.sendall("Hello client".encode())
                client.sendall("420".encode())
            except socket.error:
                print("Client " + str(addr) + " disconnected from the server")
                clients.remove(client)
        if len(clients) == 0:
            break
    print("No connections" + linje)
    checkForConnectionsThread = False


# List of clients
clients = []

checkForConnectionsThread = False
# This loop will run forever, accepting connections and serving creating a new thread for each connection
while True:
    # Accept a connections
    clientSocket, addr = serverSocket.accept()
    # Add the client to the list of clients
    clients.append(clientSocket)
    print("Client connected to the server" + str(addr))
    broadcast(clientSocket, addr)
    # thread.start_new_thread(handleclient, (clientSocket, addr))
    # Start a new thread to check for disconnected clients if not started
    # not checkForConnectionsThread and
    if len(clients) == 1:
        thread.start_new_thread(checkForConnections, ())

# Close the socket
serverSocket.close()
