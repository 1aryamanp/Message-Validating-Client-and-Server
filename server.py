import socket
import hashlib

def handle_client(client_socket, keys):
    try:
        request = client_socket.recv(1024).decode('ascii').strip()
        if request != "HELLO":
            print("Error: Invalid request from client")
            return

        client_socket.send("260 OK\r\n".encode('ascii'))

        while True:
            request = client_socket.recv(1024).decode('ascii')
            if request.startswith("DATA"):
                sha256_hash = hashlib.sha256()
                while True:
                    data = client_socket.recv(1024).decode('ascii')
                    if data == ".":
                        break
                    sha256_hash.update(data.encode('ascii'))
                signature = sha256_hash.hexdigest()
                client_socket.send("270 SIG\r\n".encode('ascii'))
                client_socket.send(signature.encode('ascii') + "\r\n".encode('ascii'))
            elif request == "QUIT":
                client_socket.close()
                return
            else:
                print("Error: Invalid request from client")
                return
    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()

def main():
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 7894
    key_file = "key.txt"

    with open(key_file, "r") as key_file:
        keys = [line.strip() for line in key_file.readlines()]

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    while True:
        client_sock, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        handle_client(client_sock, keys)

if __name__ == "__main__":
    main()
