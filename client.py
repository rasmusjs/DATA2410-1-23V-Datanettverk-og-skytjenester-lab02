import socket
import time

host, port = "127.0.0.1", 9091

"""    # Create the request with header
    request = str(input("Enter request: "))
    # Encode the response
    request = request.encode()
    # Send the response
    sock.send(request)"""

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
        time.sleep(3)
        try:
            response = sock.recv(3).decode()
            if response in "420":
                sock.send("69".encode())
            else:
                print(response)
        except socket.error:
            print("Lost connection from the server")
            exit(1)


while True:
    # Try to connect to the server
    # thread.start_new_thread(listen, ())
    listen()
