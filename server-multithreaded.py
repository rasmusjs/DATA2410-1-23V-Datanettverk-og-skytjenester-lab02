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
host, port = "127.0.0.1", 9090

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


def helpClient():
    helptext = "Commands: \n"
    helptext += "––> help - Show this help screen \n"
    helptext += "––> exit - Exit the server\n"
    helptext += "––> list - List all connected clients\n"
    helptext += "––> nick yournickname - Set a nickname\n"
    helptext += "––> broadcast - Broadcast a message to all clients\n"
    helptext += "––> message - Send a message to a specific client\n"
    helptext += "––> game - Start a game with a client \n" + linje
    return helptext


nicknames = []


class Client:

    def __init__(self, numb, nickname, clientSocket):
        self.numb = numb
        self.nickname = nickname
        self.clientSocket = clientSocket


def listOfClients(clientSocket):
    clientlist = "Connected clients: "
    for client in nicknames:
        if client.clientSocket == clientSocket:
            clientlist += "You "
        clientlist += client.nickname
    return clientlist


# This function handles the client connection, it sends the response to the client and closes the connection
def handleClient(clientSocket, clientIP):
    print("Started new thread for client" + str(
        clientIP) + linje)
    # Send help text to client
    clientSocket.send(helpClient().encode())
    while True:
        try:
            # Get the request
            clientRequest = clientSocket.recv(1024).decode()

            # Check if the client wants to exit
            if clientRequest == "exit":
                print("Client " + str(clientIP) + " disconnected from the server")
                clients.remove(clientSocket)
                break
            else:
                clientRequest = clientRequest.replace('HelloServer', '')
                if len(clientRequest) != 0:
                    print("Client " + str(clientIP) + " sent a request: " + clientRequest)
                    if "help" in clientRequest:
                        clientSocket.send(helpClient().encode())
                """ elif "nick" in clientRequest:
                     clientRequest = clientRequest.split(" ")
                     for client in nicknames:
                         if client.clientSocket == clientSocket:
                             client.nickname = clientRequest[1]
                             clientSocket.send("Nickname changed to " + clientRequest[1] + linje)
                 elif clientRequest == "list":
                     clientSocket.send(listOfClients(clientSocket).encode())"""
        except socket.error:
            print("Client " + str(addr) + " disconnected from the server")
            clients.remove(clientSocket)
            break


def broadcast(clientSocket, clientIP):
    if len(clients) > 1:
        for client in clients:
            if client != clientSocket:
                broadcastMessage = "New client  " + str(clientIP) + " connected to the server"
                try:
                    time.sleep(0.5)
                    client.send(broadcastMessage.encode())
                except socket.error:
                    print("Unable to send broacast message to " + str(client))


# Check if any clients have disconnected
def checkForConnections():
    print("Started new thread to check for disconnected clients" + linje)
    while True:
        # Sleep for 2 seconds
        time.sleep(2)
        for client in clients:
            try:
                client.sendall("HelloClient".encode())
            except socket.error:
                print("Client " + str(addr) + " disconnected from the server")
                clients.remove(client)
        if len(clients) == 0:
            break
    print("No connections" + linje)


# List of active clients
clients = []
messages = []

# This loop will run forever, accepting connections and serving creating a new thread for each connection
while True:
    # Accept a connections
    clientSocket, addr = serverSocket.accept()
    # Add the client to the list of clients
    clients.append(clientSocket)
    # nicknames.append((len(clients), "Client " + str(len(clients)), clientSocket))
    broadcast(clientSocket, addr)
    thread.start_new_thread(handleClient, (clientSocket, addr))
    # Start a new thread to check for disconnected clients if not started
    if len(clients) == 1:
        thread.start_new_thread(checkForConnections, ())

# Close the socket
serverSocket.close()
