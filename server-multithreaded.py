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


def message(socketNumber, text):
    global clients
    socketNumber = str(socketNumber)
    # Send message to all clients if * is used
    if socketNumber == "*":
        for client in clients:
            client.send(text.encode())
        print("Sending message to all clients –> " + text)
    # Send message to specific client if a number is used
    else:
        try:
            socketNumber = int(socketNumber)
            client = clients[int(socketNumber)]
            client.send(text.encode())
            print("Sending message to " + str(socketNumber) + " –> " + text)
        except ValueError:
            print("Invalid clientID")


def helpClient():
    helptext = "Commands: \n"
    helptext += "––> help - Show this help screen \n"
    helptext += "––> exit - Exit the server\n"
    helptext += "––> list - List all connected clients\n"
    helptext += "––> message id message - Send a message to a specific client or use * for all clients\n"
    helptext += "––> log - Get the request log\n"
    helptext += "––> game - Start a game with a client \n" + linje
    return helptext


def listOfClients(clientSocket):
    clientlist = "Connected clients:  \n"
    i = 0
    for client in clients:
        if client == clientSocket:
            clientlist += "Your clientID is " + str(i)
        else:
            clientlist += "User " + str(i)
        clientlist += "\t"
        i += 1
    return clientlist


def getClientId(clientSocket):
    i = 0
    for client in clients:
        if client == clientSocket:
            return i
        i += 1


def startGame(firstClientNumber, secondClientNumber):
    global clients

    # Save the clientID as an integer
    firstClientNumber = int(firstClientNumber)
    secondClientNumber = int(secondClientNumber)

    # Send message to the secondClient
    message(secondClientNumber,
            str(firstClientNumber) + " wants to play a game with you. Type 'yes' to accept or 'no' to decline")

    # Get the socket number from the clients
    try:
        client1Socket = clients[firstClientNumber]
        client2Socket = clients[secondClientNumber]
    except ValueError:
        print("Invalid clientID")
        return

    gameStarted = False
    while True:
        try:
            firstClientResponse = ""
            secondClientResponse = ""
            # Get the response from the clients
            for chat in clientLogs:
                if chat.clientId == firstClientNumber:
                    firstClientResponse = chat.response
                if chat.clientId == secondClientNumber:
                    secondClientResponse = chat.response

            if firstClientResponse != "" or secondClientResponse != "":
                """firstClientResponse = client1Socket.recv(1024).decode()
                secondClientResponse = client2Socket.recv(1024).decode()"""

                print(firstClientResponse + " " + secondClientResponse)

                if "yes" in secondClientResponse:
                    msg = "Game started"
                    message(firstClientNumber, msg)
                    message(secondClientNumber, msg)
                    gameStarted = True
                    time.sleep()
                elif "no" in secondClientResponse:
                    message(firstClientNumber, "Game declined")
                    message(secondClientNumber, "Game declined")
                    break

                if gameStarted:
                    if firstClientResponse == secondClientResponse:
                        msg = "You both chose " + firstClientResponse + ". It's a tie!"
                        message(firstClientNumber, msg)
                        message(secondClientNumber, msg)
                elif (firstClientResponse == "r" and secondClientResponse == "s") or (
                        firstClientResponse == "s" and secondClientResponse == "p") or (
                        firstClientResponse == "p" and secondClientResponse == "r"):
                    msg = "You chose " + firstClientResponse + " and your opponent chose " + secondClientResponse + ". You won!"
                    message(firstClientNumber, msg)
                    msg = "You chose " + secondClientResponse + " and your opponent chose " + firstClientResponse + ". You lost!"
                    message(secondClientNumber, msg)
                else:
                    msg = "You chose " + firstClientResponse + " and your opponent chose " + secondClientResponse + ". You lost!"
                    message(firstClientNumber, msg)
                    msg = "You chose " + secondClientResponse + " and your opponent chose " + firstClientResponse + ". You won!"
                    message(secondClientNumber, msg)

            clientLogs.clear()
        except socket.error:
            print("Client " + str(addr) + " disconnected from the server")
            clients.remove(clientSocket)
            break


# Keep track of all the clients messages
clientLogs = []


class ClientLog:
    def __init__(self, clientId, response):
        self.clientId = clientId
        self.response = response


# This function handles the client connection, it sends the response to the client and closes the connection
def handleClient(clientSocket, clientIP):
    print("Started new thread for client" + str(
        clientIP) + linje)
    clientID = getClientId(clientSocket)
    # Request log
    chatlog = []
    # Send welcome message to the client
    clientSocket.send("Welcome to the chat! Type 'help' for help. ".encode())
    while True:
        try:
            # Get the request
            clientRequest = clientSocket.recv(1024).decode()
            # Start game
            if clientRequest == "/play":
                startGame(addr)
                break
            # Check if the client wants to exit
            if clientRequest == "exit":
                print("Client " + str(clientIP) + " disconnected from the server")
                clients.remove(clientSocket)
                break
            else:
                clientRequest = clientRequest.replace('HelloServer', '')
                if len(clientRequest) != 0:
                    # Add the request to the logs
                    chatlog.append(clientRequest)
                    clientLogs.append(ClientLog(clientID, clientRequest))
                    print("Client " + str(clientIP) + " sent a request: " + clientRequest)
                    if "help" in clientRequest:
                        clientSocket.send(helpClient().encode())
                    elif "list" in clientRequest:
                        clientSocket.send(listOfClients(clientSocket).encode())
                    elif "msg" in clientRequest or "message" in clientRequest:
                        # Find the client to send the message to
                        toClient = clientRequest.split(" ")[1]
                        text = ""
                        # Get all the words after the clientID
                        for i in range(2, len(clientRequest.split(" "))):
                            if i == 2:
                                text = clientRequest.split(" ")[i]
                            else:
                                text += " " + clientRequest.split(" ")[i]
                        message(toClient, text)
                    elif "game" in clientRequest:
                        # Find the client to send the message to
                        toClient = clientRequest.split(" ")[1]
                        startGame(getClientId(clientSocket), toClient)
                    elif "log" in clientRequest:
                        clientSocket.send(str(chatlog).encode())
        except socket.error:
            print("Client " + str(addr) + " disconnected from the server")
            clients.remove(clientSocket)
            break


game_sessions = {}  # Keep track of players and choices


# This function difines the game logic
def playGame(player1Choice, player2Choice):
    if player1Choice == player2Choice:
        return "Draw"
    elif (player1Choice == "r" and player2Choice == "s") or (player1Choice == "s" and player2Choice == "p") or (
            player1Choice == "p" and player2Choice == "r"):
        return "Player 1 won"
    else:
        return "Player 2 won"


def startGameNew(username):
    if username in game_sessions:
        return "You are already in a game"
    else:
        game_sessions[username] = ""
        return "Waiting for another player to join"


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
    broadcast(clientSocket, addr)
    thread.start_new_thread(handleClient, (clientSocket, addr))
    # Start a new thread to check for disconnected clients if not started
    if len(clients) == 1:
        thread.start_new_thread(checkForConnections, ())
    """if len(games) == 1:
        
        thread.start_new_thread(startGame(), ())"""

# Close the socket
serverSocket.close()
