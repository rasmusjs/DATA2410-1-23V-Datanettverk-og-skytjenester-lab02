import _thread as thread
import socket
import time

host, port = "127.0.0.1", 9091

# Create the socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the host and port
    sock.connect((host, port))
    print("Connecting to " + host + ":" + str(port) + "\n")
except ConnectionRefusedError:
    print("Connection refused. Please check the host and port, and try again.")
    exit(1)

# Variable used to quit the program if the server is not responding
connected = True


# This function is used to listen for new messages from the server, it also keeps the socket alive
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
            break
    global connected
    connected = False


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


# This is used give the user a new line before the first request
firstChat = True
sendingInput = False

while True:
    try:
        if connected:
            # If the user is not listening, start a new thread to listen for new messages, and keep the socket alive
            thread.start_new_thread(listen, ())
            # If the user is not sending input, start a new thread to send input
            if not sendingInput:
                sendingInput = True
                sendUserInput()
    except socket.error:
        print("Lost connection from the server")
        break
exit(1)
