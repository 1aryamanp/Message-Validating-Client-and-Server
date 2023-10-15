import socket
import sys

# Server name, port, and message and signature file names
SERVER_NAME = sys.argv[1]
SERVER_PORT = int(sys.argv[2])
MSG_FILE_NAME = sys.argv[3]
SIG_FILE_NAME = sys.argv[4]

# Load the messages and signatures from the files
msg_sizes = []
msg_bytes = []
signatures = []

with open(MSG_FILE_NAME, 'r', encoding='ascii') as file:
    for i, line in enumerate(file):
        if i % 2 == 0:
            msg_sizes.append(int(line.strip()))
        else:
            msg_bytes.append(bytes(line.strip(), 'ascii'))

with open(SIG_FILE_NAME, 'r', encoding='ascii') as file:
    for i, line in enumerate(file):
        signatures.append(line.strip())

# Create a socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_NAME, SERVER_PORT))

# Send the "HELLO" message to the server
client_socket.send("HELLO".encode("ascii"))

# Receive the response from the server
server_response = client_socket.recv(128)

# Check if the response is "260 OK"
if server_response.decode("ascii") != "260 OK":
    print("error: expected 260 OK")
    exit(1)

# Send the escaped messages to the server
for i in range(len(msg_bytes)):
    escaped_msg = msg_bytes[i]
    client_socket.send(escaped_msg.encode("ascii"))

    # Receive the response from the server
    server_response = client_socket.recv(128)

    # Check if the response is "270 SIG"
    if server_response.decode("ascii") != "270 SIG":
        print("error: expected 270 SIG")
        exit(1)

    # Receive the signature from the server
    signature = client_socket.recv(10000)

    # Compare the signature to the expected signature
    if signature == signatures[i]:
        client_socket.send("PASS".encode("ascii"))
    else:
        client_socket.send("FAIL".encode("ascii"))

# Receive the response from the server
server_response = client_socket.recv(128)

# Check if the response is "260 OK"
if server_response.decode("ascii") != "260 OK":
    print("error: expected 260 OK")
    exit(1)

# Send the "QUIT" message to the server
client_socket.send("QUIT".encode("ascii"))

# Close the client socket
client_socket.close()