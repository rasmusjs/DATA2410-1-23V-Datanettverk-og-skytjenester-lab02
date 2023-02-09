# Currently, your web server handles only one HTTP request at a time. You should implement a multithreaded server
# that is capable of serving multiple requests simultaneously. Using threading, first create a main thread in which
# your modified server listens for clients at a fixed port. When it receives  a TCP connection request from a client,
# it will set up the TCP connection through another port and services the client request in a separate thread. There
# will be a separate TCP connection in a separate thread for each request/response pair

import _thread as thread
import socket

# Define the host and port
host, port = "127.0.0.1", 9090

# Create a socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
    print("Started new thread for client" + str(clientIP) + "\n_______________________________________________________")
    # Get the request
    clientRequest = clientSocket.recv(4096).decode()
    # Encode the response
    response = "Received request: " + clientRequest
    response = response.encode()
    # Send the response
    clientSocket.sendall(response)
    # Close the connection
    clientSocket.close()


# This loop will run forever, accepting connections and serving creating a new thread for each connection
while True:
    # Accept a connections
    clientSocket, addr = serverSocket.accept()
    thread.start_new_thread(handleclient, (clientSocket, addr))

# Close the socket
serverSocket.close()
