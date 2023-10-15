import socket
import sys

# Listen port and key file name
LISTEN_PORT = int(sys.argv[1])
KEY_FILE_NAME = sys.argv[2]

# Load the keys from the key file
keys = []
with open(KEY_FILE_NAME, 'r', encoding='ascii') as file:
    for line in file:
        keys.append(line.strip())

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), LISTEN_PORT))
server_socket.listen(5)

# Accept a connection
client_socket, client_address = server_socket.accept()

# Receive the first message from the client
message = client_socket.recv(1028)
message_decoded = message.decode("ascii")

# Check if the first message is "HELLO"
if message_decoded != "HELLO":
    print("error: illegal command, expecting HELLO")
    client_socket.close()
    exit(1)

# Send a "260 OK" message to the client
client_socket.send("260 OK".encode("ascii"))

# Start a loop to receive and process messages from the client
while True:
    # Receive the next message from the client
    message = client_socket.recv(1028)
    message_decoded = message.decode("ascii")

    # Check if the message is "DATA"
    if message_decoded != "DATA":
        print("error: illegal command, expecting DATA or QUIT")
        client_socket.close()
        exit(1)

    # Receive the data from the client
    data = client_socket.recv(10000)

    # Unescape the data
    unescaped_data = data.decode("ascii")

    # Generate a SHA-256 hash of the data
    hash = sha256(unescaped_data.encode("ascii")).hexdigest()

    # Send a "270 SIG" message to the client
    client_socket.send("270 SIG".encode("ascii"))

    # Send the hash to the client
    client_socket.send(hash.encode("ascii"))

    # Receive the next message from the client
    message = client_socket.recv(1028)
    message_decoded = message.decode("ascii")

    # Check if the message is "PASS" or "FAIL"
    if message_decoded != "PASS" and message_decoded != "FAIL":
        print("error: illegal command, expecting PASS or FAIL")
        client_socket.close()
        exit(1)

    # Send a "260 OK" message to the client
    client_socket.send("260 OK".encode("ascii"))

    # If the message is "QUIT", break out of the loop
    if message_decoded == "QUIT":
        break

# Close the client socket
client_socket.close()

# Close the server socket
server_socket.close()