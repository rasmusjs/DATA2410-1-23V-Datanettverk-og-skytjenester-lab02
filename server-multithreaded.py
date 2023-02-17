# A server should keep track of the total number of clients, allow clients to send messages and broadcast everyone.
# Below are some key functions you must implement: • You should implement a function named broadcast to notify
# everyone when a client joins (except the client who joined). • You should also implement a function called game
# where it will allow two clients to play rock, paper, scissors game.

import _thread as thread
import socket
import time

# Define the host and port
host, port = "127.0.0.1", 9091

# Create a socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# List of active sockets
connectedClients = []
# Keep track of all players in the lobby
gamelobby = []

# Keep track of all the client requests
clientRequests = []
checkingGames = False

# Create a blanking line for the console
line = "\n_______________________________________________________"


# This client will hold the information about the client requests

class ClientLog:
    def __init__(self, client, request):
        self.client = client
        self.request = request


# This object will hold all the information about the game
class Game:
    def __init__(self, socket1, socket2, player1Choice, player2Choice, player1Points,
                 player2Points, responseSent, rounds):
        self.socket1 = socket1
        self.socket2 = socket2
        self.player1Choice = player1Choice
        self.player2Choice = player2Choice
        self.client1Points = player1Points
        self.client2Points = player2Points
        self.responseSent = responseSent
        self.rounds = rounds


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
    global connectedClients
    socketNumber = str(socketNumber)
    # Send message to all connectedClients if * is used
    if socketNumber == "*":
        for client in connectedClients:
            client.send(text.encode())
        print("Sending message to all connectedClients –> " + text)
    # Send message to specific client if a number is used
    else:
        try:
            socketNumber = int(socketNumber)
            client = connectedClients[int(socketNumber)]
            client.send(text.encode())
            print("Sending message to " + str(socketNumber) + " –> " + text)
        except ValueError:
            print("Invalid clientID")


def helpClient():
    helptext = "Commands: \n"
    helptext += "––> help - Show this help screen \n"
    helptext += "––> exit - Exit the server\n"
    helptext += "––> list - List all connected connectedClients\n"
    helptext += "––> message/msg id message - Send a message to a specific client or use * for all clients\n"
    helptext += "––> log - Get a log of all your requests\n"
    helptext += "––> game - Start a online game with rock paper scissors, the first to 3 points wins.\n"
    helptext += "Use r p s to choose your move, write cancel to quit the game\n" + line
    return helptext


# This function lists all the connected clients
def listOfClients(client):
    clientlist = "Connected connected users:  \n"
    i = 0
    for connected in connectedClients:
        if connected == client:
            clientlist += "Your clientID is " + str(i)
        else:
            clientlist += "User " + str(i)
        clientlist += "\t"
        i += 1
    return clientlist


# This function gets the clientID from the client
def getClientId(client):
    i = 0
    for connected in connectedClients:
        if connected == client:
            return i
        i += 1


# This function handles the client connection, it sends the response to the client and closes the connection
def handleClient(client, clientIP):
    print("Started new thread for client" + str(
        clientIP) + line)
    # Get access to the clientRequests list
    global clientRequests
    # Request log
    chatlog = []
    # Send welcome message to the client
    client.send("Welcome to the chat! Type 'help' for help. ".encode())
    while True:
        try:
            # Get the request and remove the HelloServer from the request
            request = formatRequest(client)
            # request = client.recv(1024).decode().replace('HelloServer', '')

            # If the request is not empty
            if len(request) != 0:
                # Add the request to the logs
                chatlog.append(request)
                clientRequests.append(ClientLog(client, request))
                print("Client " + str(clientIP) + " sent a request: " + request)
                if "help" == request:
                    client.send(helpClient().encode())
                elif "list" == request:
                    client.send(listOfClients(client).encode())
                elif "msg" == request or "message" == request:
                    # Try to split the request, if it fails send an error message
                    try:
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
                    except IndexError:
                        client.send("Invalid message command".encode())
                elif "game" in request:
                    print("Game request")
                    gamelobby.append(client)
                    client.send("Waiting for another player to join".encode())
                elif "quit" == request:
                    gamelobby.remove(client)
                elif "log" in request:
                    client.send(str(chatlog).encode())
        except socket.error:
            print("Client " + str(addr) + " disconnected from the server")
            connectedClients.remove(client)
            break


# This  function notifies  everyone when a client joins (except the client who joined).
def broadcast(client, clientIP):
    # Check if there are more than 1 connected clients
    if len(connectedClients) > 1:
        # Loop through all connectedClients
        for connected in connectedClients:
            # If the client is not the client who joined send a message to the client
            if connected != client:
                broadcastMessage = "New client  " + str(clientIP) + " connected to the server"
                # Try to send the message, if it fails remove the client from the connectedClients list
                try:
                    time.sleep(0.5)
                    connected.send(broadcastMessage.encode())
                except socket.error:
                    print("Unable to send broadcast message to " + str(connected))


# This function checks if any clients have disconnected and keeps the connections with the clients alive
def checkForConnections():
    print("Started new thread to check for disconnected connectedClients" + line)
    global gamelobby
    while True:
        # Sleep for 2 seconds
        time.sleep(2)
        # Loop through all clients
        for client in connectedClients:
            # Try to send a message to the client, if it fails remove the client from the list
            try:
                client.sendall("HelloClient".encode())
            except socket.error:
                print("Client " + str(addr) + " disconnected from the server")
                connectedClients.remove(client)
        # If there are no connected clients break the loop and set the gamelobby to empty
        if len(connectedClients) == 0:
            gamelobby = []
            break
    print("No connections" + line)


# This function formats the request, it removes the HelloServer from the request if it is there
def formatRequest(request):
    # Format the request remove HelloServer
    request = request.recv(1024).decode().replace('HelloServer', '')
    if len(request) == 0:
        return ""
    return request


# This is the rock paper scissors games, it will allow two clients to play against each other
def game():
    print("Started new thread to check for game seeking game" + line)
    global gamelobby
    global checkingGames
    activeGames = []
    while True:
        checkingGames = True
        # Sleep for 2 seconds
        time.sleep(2)
        # Loop through all clients in the lobby
        for client in gamelobby:
            try:
                # If we have 2 game in a lobby start the game
                if len(gamelobby) % 2 == 0:
                    for client2 in gamelobby:
                        # print("Client " + str(client) + " is in the lobby")
                        if client2 != client:
                            if len(activeGames) == 0:
                                activeGames.append(Game(client, client2, "", "", 0, 0, 0, 0))
                                print("Game started between " + str(client) + " and " + str(client2))
                        # Dette funker ikke, vi får en evig løkke her
                        # else:
                        #    for activeGame in activeGames:
                        #        if activeGame.socket1 != client and activeGame.socket2 != client2:
                        #            activeGames.append(Game(client, client2, "", "", 0, 0, 0, 0))
                        #            print("Game started between " + str(client) + " and " + str(client2))
                # This is the game logic for the game, it will run every 2 seconds
            except socket.error:
                print("Client " + str(addr) + " disconnected from the server")
                connectedClients.remove(client)
                gamelobby.remove(client)

        # Try to loop through all the active games
        try:
            for activeGame in activeGames:
                # Send the message to the clients
                msg = "Starting a game of rock paper scissors, use r, p, or s to choose your move."
                msg += " Write cancel to quit the game"

                if activeGame.rounds < 3 and activeGame.rounds != 0:
                    msg = "Round number  " + str(activeGame.rounds)

                if activeGame.rounds == 3:
                    msg = "Last round"

                if activeGame.responseSent != 1:
                    activeGame.socket1.send(msg.encode())
                    activeGame.socket2.send(msg.encode())
                    activeGame.responseSent = 1

                # Get the messages from the game in the game
                for clientR in clientRequests:
                    # If the socket  is the same as the client in the lobby do stuff
                    if clientR.request != "game" and clientR.request != "":
                        # Break the loop if the client wants to quit
                        if clientR.request == "cancel":
                            gamelobby.remove(clientR.client)
                            clientRequests.remove(clientR)
                            continue

                        # Check if the client has sent a valid message
                        if clientR.request == "r" or clientR.request == "p" or clientR.request == "s":
                            # Only add the message to the game if the player has not made a choice
                            if activeGame.player1Choice == "" and clientR.client == activeGame.socket1:
                                activeGame.player1Choice = str(clientR.request)
                                # print("Player 1 message:" + clientR.request)
                                clientRequests.remove(clientR)
                                continue
                            if activeGame.player2Choice == "" and clientR.client == activeGame.socket2:
                                activeGame.player2Choice = str(clientR.request)
                                # print("Player 2 message:" + clientR.request)
                                clientRequests.remove(clientR)
                                continue
                # If the players are not in the lobby remove the game between them
                if activeGame.socket1 not in gamelobby or activeGame.socket2 not in gamelobby:
                    activeGame.socket1.send("Game ended, player left".encode())
                    activeGame.socket2.send("Game ended,  player left".encode())
                    activeGames.remove(activeGame)
                    break

                # If both players have made a choice, check who won the rounds and add the score, this is also the
                # game logic
                if activeGame.player1Choice != "" and activeGame.player2Choice != "":
                    print("Player 1 said:" + activeGame.player1Choice)
                    print("Player 2 said:" + activeGame.player2Choice)
                    msgPlayer1, msgPlayer2 = "Tie this round", "Tie this round"
                    # Check if the players have made the same choice, if they have then it is a tie
                    if activeGame.player1Choice == activeGame.player2Choice and activeGame.player1Choice != "game":
                        activeGame.responseSent = 1
                        activeGame.rounds += 1
                    # Check if player 1 won the round
                    elif (activeGame.player1Choice == "r" and activeGame.player2Choice == "s") or (
                            activeGame.player1Choice == "s" and activeGame.player2Choice == "p") or (
                            activeGame.player1Choice == "p" and activeGame.player2Choice == "r"):
                        msgPlayer1, msgPlayer2 = "You won this round", "You lost this round"
                        activeGame.client1Points += 1
                        activeGame.responseSent = 1
                        activeGame.rounds += 1
                    # Check if player 2 won the round
                    elif (activeGame.player1Choice == "r" and activeGame.player2Choice == "p") or (
                            activeGame.player1Choice == "s" and activeGame.player2Choice == "r") or (
                            activeGame.player1Choice == "p" and activeGame.player2Choice == "s"):
                        msgPlayer1, msgPlayer2 = "You lost this round", "You won this round "
                        activeGame.client2Points += 1
                        activeGame.responseSent = 1
                        activeGame.rounds += 1
                    # If the players have not made a valid choice
                    else:
                        msgPlayer1, msgPlayer2 = "Invalid choice", "Invalid choice"

                    # Send the message to the clients
                    activeGame.socket1.sendall(msgPlayer1.encode())
                    activeGame.socket2.sendall(msgPlayer2.encode())

                    # Reset the choices
                    activeGame.player1Choice = ""
                    activeGame.player2Choice = ""
                    # If the game is over remove the game from the active games list and the lobby
                    if activeGame.rounds == 4:
                        if activeGame.client1Points > activeGame.client2Points:
                            msgPlayer1, msgPlayer2 = "You won the game!", "You lost the game, better luck next time."
                        elif activeGame.client1Points < activeGame.client2Points:
                            msgPlayer1, msgPlayer2 = "You lost the game, better luck next time.", "You won the game!"
                        else:
                            msgPlayer1, msgPlayer2 = "Game ended in tie.", "Game ended in tie."
                        # Send the same end message to both players
                        msg = " Removed the you from the lobby, you can now start a new game with the command game"
                        msgPlayer1 += msg
                        msgPlayer2 += msg
                        # Send the message to the clients
                        activeGame.socket1.sendall(msgPlayer1.encode())
                        activeGame.socket2.sendall(msgPlayer2.encode())
                        print("Game ended between " + str(activeGame.socket1) + " and " + str(
                            activeGame.socket2))
                        # Remove players from the lobby
                        gamelobby.remove(activeGame.socket1)
                        gamelobby.remove(activeGame.socket2)
                        activeGames.remove(activeGame)
        except socket.error or ValueError:
            print("Client " + str(addr) + " disconnected from the server")
        # If the lobby is empty break the loop
        if len(gamelobby) == 0:
            break
    # end of while loop

    # Stop checking for games if there are no clients in the lobby
    checkingGames = False
    print("Closed thread to check for game seeking game, no clients in lobby" + line)


# This loop will run forever, accepting connections and serving creating a new thread for each connection
while True:
    # Accept a connections
    clientSocket, addr = serverSocket.accept()
    # Add the client to the list of connectedClients
    connectedClients.append(clientSocket)
    # Add the client to the lobby
    broadcast(clientSocket, addr)
    # Start a new thread to handle the client, for listening to the client
    thread.start_new_thread(handleClient, (clientSocket, addr))

    # Start a new thread to check for disconnected connectedClients if not started
    if len(connectedClients) == 1:
        thread.start_new_thread(checkForConnections, ())

    # Start a new thread to check for game seeking clients
    if len(gamelobby) > 1 or checkingGames is False:
        thread.start_new_thread(game, ())

# Close the socket
serverSocket.close()
