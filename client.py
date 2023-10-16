import socket
import sys

def main():
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])
    msgName = sys.argv[3]
    sigName = sys.argv[4]

    msgSizes = []
    msgBytes = []
    signatures = []

    with open(msgName, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if i % 2 == 0:
                msgSizes.append(int(line.strip()))
            else:
                tempBytes = bytes(line.strip(), 'utf-8')
                msgBytes.append(tempBytes)

    with open(sigName, 'r', encoding='ascii') as file:
        for line in file:
            signatures.append(line.strip())

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((serverName, serverPort))

    s.send("HELLO".encode("ascii"))

    msg = s.recv(128)
    if msg.decode("ascii") != "260 OK":
        print("error: expected 260 OK")
        s.close()
        return

    for i in range(len(msgSizes)):
        s.send("DATA".encode("ascii"))
        s.send(msgBytes[i])  # Send the message
        response = s.recv(128)

        if response.decode("ascii") != "270 SIG":
            print("error: expected 270 SIG")
            s.close()
            return

        # Receive the server's computed signature
        server_signature = s.recv(128)

        # Compare the signature to the expected signature
        if server_signature.decode("ascii") == signatures[i]:
            s.send("PASS".encode("ascii"))
        else:
            s.send("FAIL".encode("ascii"))

        response = s.recv(128)

        if response.decode("ascii") != "260 OK":
            print("error: expected 260 OK")
            s.close()
            return

    # Send the QUIT message and close the socket
    s.send("QUIT".encode("ascii"))
    s.close()

if __name__ == "__main__":
    main()
