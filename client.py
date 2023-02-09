import _thread as thread
import socket
import time

print("Usage: client.py server host server port filename. \n Now starting server with default values")
host, port = "127.0.0.1", 9091

try:
    # Create new socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the host and port
    sock.connect((host, port))
    print("Connecting to " + host + ":" + str(port) + "\n")
    # Create the request with header
    request = str(input("Enter request: "))
    # Encode the response
    request = request.encode()
    # Send the response
    sock.send(request)

except ConnectionRefusedError:
    print("Connection refused. Please check the host and port, and try again.")
    exit(1)


def listen():
    # Sleep for 1 second
    time.sleep(1)
    while True:
        try:
            response = sock.recv(4096).decode()
            if response == "Hello":
                sock.send(request)
            else:
                print(response)

        except socket.error:
            print("Lost connection from the server")
            exit(1)


# while True:
# Try to connect to the server
thread.start_new_thread(listen, ())
