import socket

def send_message(client_socket, message):
    client_socket.send(message.encode('ascii') + "\r\n".encode('ascii'))

def main():
    server_name = 'localhost'
    server_port = 7894
    message_filename = 'message1.txt'
    signature_filename = 'sig1.txt'

    messages = []
    signatures = []

    with open(message_filename, 'r') as message_file:
        messages = message_file.read().splitlines()

    with open(signature_filename, 'r') as signature_file:
        signatures = signature_file.read().splitlines()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_name, server_port))

    send_message(client_socket, "HELLO")

    response = client_socket.recv(1024).decode('ascii').strip()
    if response != "260 OK":
        print("Error: Server did not respond correctly")
        return

    for message, expected_signature in zip(messages, signatures):
        send_message(client_socket, "DATA")
        send_message(client_socket, message)

        response = client_socket.recv(1024).decode('ascii').strip()
        if response != "270 SIG":
            print("Error: Invalid response from the server")
            return

        received_signature = client_socket.recv(1024).decode('ascii').strip()
        if received_signature == expected_signature:
            send_message(client_socket, "PASS")
        else:
            send_message(client_socket, "FAIL")

        response = client_socket.recv(1024).decode('ascii').strip()
        if response != "260 OK":
            print("Error: Invalid response from the server")
            return

    send_message(client_socket, "QUIT")
    client_socket.close()

if __name__ == "__main__":
    main()
