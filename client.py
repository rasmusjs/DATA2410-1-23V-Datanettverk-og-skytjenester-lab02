import _thread as thread
import socket
import time

host, port = "127.0.0.1", 9091

closeThreads = False

# Create the socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the host and port
    sock.connect((host, port))
    print("Connecting to " + host + ":" + str(port) + "\n")
except ConnectionRefusedError:
    print("Connection refused. Please check the host and port, and try again.")
    exit(1)


def listen():
    while True:
        # Sleep for 1 second before checking for new messages
        time.sleep(1)
        try:
            # Get the raw response from server
            rawResponse = sock.recv(1024).decode()
            # Remove the "HelloClient" part of the response, and print the rest. HelloClient is used to keep the socket
            # alive for the server, and should not be printed to the client.
            response = rawResponse.replace('HelloClient', '')
            # If the response is not empty, print it
            if len(response) != 0:
                print("\n" + response + "\n" + "Enter new request:")
            # Send "HelloServer" to keep the socket alive
            if rawResponse in "HelloClient":
                sock.send("HelloServer".encode())
        # If the server is not responding, exit the program
        except socket.error:
            print("Lost connection from the server")
            exit(1)


# This function is used to send messages to the server
def sendUserInput():
    global firstChat
    # Display the help text for new users
    if firstChat:
        firstChat = False
        print("Type 'exit' to exit.")
    # Get the user input
    request = str(input())
    # If the user input is not "exit", send the request to the server
    if request == "exit":
        exit(1)
    else:
        # Encode and send the request
        sock.send(request.encode())
    # Set sendingInput to false, so the user can send another request
    global sendingInput
    sendingInput = False
    # Response from server if the user wants to play a game
    if request == "/play":
        print("Waiting for another player...")

# This is used give the user a new line before the first request
firstChat = True
sendingInput = False

while True:
    # If the user is not listening, start a new thread to listen for new messages, and keep the socket alive
    thread.start_new_thread(listen, ())
    # If the user is not sending input, start a new thread to send input
    if not sendingInput:
        sendingInput = True
        sendUserInput()
