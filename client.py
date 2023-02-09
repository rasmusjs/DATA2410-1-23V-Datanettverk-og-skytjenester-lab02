# Instead of using a browser, write your own HTTP client to test your server. Your client will connect
# to the server using a TCP connection, send an HTTP request to the server, and display the server
# response as an output. You can assume that the HTTP request sent is a GET method. The client
# should take command line arguments specifying the server IP address or host name, the port at which
# the server is listening, and the path at which the requested object is stored at the server. The following
# is an input command format to run the client. client.py server host server port fileName

import socket

print("Usage: client.py server host server port filename. \n Now starting server with default values")
host, port = "127.0.0.1", 9090

while True:
    # Try to connect to the server
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
        # Get the response
        response = sock.recv(4096).decode()
        # Print the response to console
        print(response)
        # Close the connection
        sock.close()
        print("\nConnection closed")
        exit(1)
    except ConnectionRefusedError:
        print("Connection refused. Please check the host and port, and try again.")
        exit(1)
