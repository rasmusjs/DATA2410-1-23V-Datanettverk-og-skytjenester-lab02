# A server should keep track of the total number of activeSockets, allow activeSockets to send messages and broadcast
# everyone. Below are some key functions you must implement:
# • You should implement a function named broadcast to notify everyone when a client joins (except
# the client who joined).
# • You should also implement a function called game where it will allow two activeSockets to play rock,
# paper, scissors game.

import _thread as thread
import socket
import time

# Define the host and port
host, port = "127.0.0.1", 9091

# Create a socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

line = "\n_______________________________________________________"

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
    global activeSockets
    socketNumber = str(socketNumber)
    # Send message to all activeSockets if * is used
    if socketNumber == "*":
        for client in activeSockets:
            client.send(text.encode())
        print("Sending message to all activeSockets –> " + text)
    # Send message to specific client if a number is used
    else:
        try:
            socketNumber = int(socketNumber)
            client = activeSockets[int(socketNumber)]
            client.send(text.encode())
            print("Sending message to " + str(socketNumber) + " –> " + text)
        except ValueError:
            print("Invalid clientID")


def helpClient():
    helptext = "Commands: \n"
    helptext += "––> help - Show this help screen \n"
    helptext += "––> exit - Exit the server\n"
    helptext += "––> list - List all connected activeSockets\n"
    helptext += "––> message id message - Send a message to a specific client or use * for all activeSockets\n"
    helptext += "––> log - Get the request log\n"
    helptext += "––> game - Start a game with a client \n" + line
    return helptext


def listOfClients(clientSocket):
    clientlist = "Connected activeSockets:  \n"
    i = 0
    for client in activeSockets:
        if client == clientSocket:
            clientlist += "Your clientID is " + str(i)
        else:
            clientlist += "User " + str(i)
        clientlist += "\t"
        i += 1
    return clientlist


def getClientId(clientSocket):
    i = 0
    for client in activeSockets:
        if client == clientSocket:
            return i
        i += 1


def startGame(firstClientNumber, secondClientNumber):
    global activeSockets
    global gameStarted

    # Save the clientID as an integer
    firstClientNumber = int(firstClientNumber)
    secondClientNumber = int(secondClientNumber)

    # Send message to the secondClient
    message(secondClientNumber,
            str(firstClientNumber) + " wants to play a game with you. Type 'yes' to accept or 'no' to decline")

    # Get the socket number from the activeSockets
    try:
        client1Socket = activeSockets[firstClientNumber]
        client2Socket = activeSockets[secondClientNumber]
    except ValueError:
        print("Invalid clientID")
        return

    gameStarted = False
    while True:
        try:
            firstClientResponse = client1Socket.recv(1024).decode()
            secondClientResponse = client2Socket.recv(1024).decode()
            firstClientResponse = firstClientResponse.replace('HelloServer', '')
            secondClientResponse = secondClientResponse.replace('HelloServer', '')

            if firstClientResponse != "" and secondClientResponse != "":
                clientLogs.clear()
                """firstClientResponse = client1Socket.recv(1024).decode()
                secondClientResponse = client2Socket.recv(1024).decode()"""

                print(firstClientResponse + " " + secondClientResponse)

                if "yes" in secondClientResponse:
                    msg = "Game started"
                    message(firstClientNumber, msg)
                    message(secondClientNumber, msg)
                    firstClientResponse = ""
                    secondClientResponse = ""
                    clientLogs.clear()
                    gameStarted = True
                    time.sleep(1)
                elif "no" in secondClientResponse:
                    message(firstClientNumber, "Game declined")
                    message(secondClientNumber, "Game declined")
                    break

                if gameStarted and firstClientResponse != "" and secondClientResponse != "":
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

        except socket.error:
            print("Client " + str(addr) + " disconnected from the server")
            activeSockets.remove(clientSocket)
            break


# This function handles the client connection, it sends the response to the client and closes the connection
def handleClient(clientSocket, clientIP):
    print("Started new thread for client" + str(
        clientIP) + line)
    global clientLogs
    # Request log
    chatlog = []
    # Send welcome message to the client
    clientSocket.send("Welcome to the chat! Type 'help' for help. ".encode())
    while True:
        try:
            # Get the request and remove the HelloServer from the request
            request = formatRequest(clientSocket)
            # request = clientSocket.recv(1024).decode().replace('HelloServer', '')

            # If the request is not empty
            if len(request) != 0:
                # Add the request to the logs
                chatlog.append(request)
                clientLogs.append(ClientLog(clientSocket, request))
                print("Client " + str(clientIP) + " sent a request: " + request)
                if "help" == request:
                    clientSocket.send(helpClient().encode())
                elif "list" == request:
                    clientSocket.send(listOfClients(clientSocket).encode())
                elif "msg" == request or "message" == request:
                    # Find the client to send the message to
                    toClient = request.split(" ")[1]
                    text = ""
                    # Get all the words after the clientID
                    for i in range(2, len(request.split(" "))):
                        if i == 2:
                            text = request.split(" ")[i]
                        else:
                            text += " " + request.split(" ")[i]
                    message(toClient, text)
                elif "game" in request:
                    print("Game request")
                    gamelobby.append(clientSocket)
                elif "quit" == request:
                    gamelobby.remove(clientSocket)
                elif "log" in request:
                    clientSocket.send(str(chatlog).encode())
        except socket.error:
            print("Client " + str(addr) + " disconnected from the server")
            activeSockets.remove(clientSocket)
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
    if len(activeSockets) > 1:
        for client in activeSockets:
            if client != clientSocket:
                broadcastMessage = "New client  " + str(clientIP) + " connected to the server"
                try:
                    time.sleep(0.5)
                    client.send(broadcastMessage.encode())
                except socket.error:
                    print("Unable to send broacast message to " + str(client))


# Check if any activeSockets have disconnected
def checkForConnections():
    print("Started new thread to check for disconnected activeSockets" + line)
    global gamelobby
    while True:
        # Sleep for 2 seconds
        time.sleep(2)
        for client in activeSockets:
            try:
                client.sendall("HelloClient".encode())
            except socket.error:
                print("Client " + str(addr) + " disconnected from the server")
                activeSockets.remove(client)
        if len(activeSockets) == 0:
            gamelobby = []
            break
    print("No connections" + line)


def formatRequest(socket):
    # Format the request remove HelloServer
    request = socket.recv(1024).decode().replace('HelloServer', '')
    if len(request) == 0:
        return ""
    return request


# Check if any activeSockets have disconnected
def checkLobby():
    print("Started new thread to check for players seeking game" + line)
    activeGames = []

    while True:
        # Sleep for 2 seconds
        time.sleep(2)
        for client in gamelobby:
            try:
                # print("Client " + str(client) + " is in the lobby")
                # Get the messages from the players in the lobby
                for msg in clientLogs:
                    # If the socket is the same as the client in the lobby do stuff
                    if msg.clientSocket == client:
                        print(msg.request)
                        clientLogs.remove(msg)
                # Hvis det er to spillere i lobbyen, legg de til i activeGames,

            except socket.error:
                print("Client " + str(addr) + " disconnected from the server")
                activeSockets.remove(client)
                gamelobby.remove(client)
        if len(gamelobby) == 0:
            break
    print("Lobby empty" + line)


# List of active activeSockets
activeSockets = []
gamelobby = []

# Keep track of all the client requests
clientLogs = []


class ClientLog:
    def __init__(self, clientSocket, request):
        self.clientSocket = clientSocket
        self.request = request


class Game:
    def __init__(self, clientSocket1, clientSocket2, clientSocket1Points, clientSocket2Points):
        self.clientSocket1 = clientSocket1
        self.clientSocket2 = clientSocket2
        self.clientSocket1Points = clientSocket1Points
        self.clientSocket2Points = clientSocket2Points


# This loop will run forever, accepting connections and serving creating a new thread for each connection
while True:
    thread.start_new_thread(checkLobby, ())
    # Accept a connections
    clientSocket, addr = serverSocket.accept()
    # Add the client to the list of activeSockets
    activeSockets.append(clientSocket)
    broadcast(clientSocket, addr)
    thread.start_new_thread(handleClient, (clientSocket, addr))
    # Start a new thread to check for disconnected activeSockets if not started

    if len(activeSockets) == 1:
        thread.start_new_thread(checkForConnections, ())

# Close the socket
serverSocket.close()
