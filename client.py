import _thread as thread
import socket
import time

host, port = "127.0.0.1", 9091

closeThreads = False

try:
    # Create new socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the host and port
    sock.connect((host, port))
    print("Connecting to " + host + ":" + str(port) + "\n")
except ConnectionRefusedError:
    print("Connection refused. Please check the host and port, and try again.")
    exit(1)


def listen():
    # Sleep for 1 second
    while True:
        time.sleep(1)
        try:
            # Get the raw response from server
            rawResponse = sock.recv(1024).decode()
            response2 = rawResponse.replace('HelloClient', '')
            if len(response2) != 0:
                print("\n" + response2 + "\n" + "Enter new request:")
            if rawResponse in "HelloClient":
                sock.send("HelloServer".encode())

        except socket.error:
            print("Lost connection from the server")
            exit(1)


def chat():
    global firstChat
    # Display the help text for new users
    if firstChat:
        firstChat = False
        textrequest = str(input("Enter a request (type 'exit' to exit):\n"))
    else:
        textrequest = str(input())
    if textrequest != "exit":
        request = textrequest
        # Encode the response
        request = request.encode()
        # Send the response
        sock.send(request)
        print("Message sent " + textrequest)
    else:
        exit(1)
    global chatstarted
    chatstarted = False


firstChat = True
chatstarted = False
while True:
    thread.start_new_thread(listen, ())
    if not chatstarted:
        chatstarted = True
        chat()
