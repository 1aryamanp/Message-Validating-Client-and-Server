import socket
import sys
import hashlib

# take in arguments
listenPort = int(sys.argv[1])
keyName = sys.argv[2]

keys = []

with open(keyName, 'r', encoding='ascii') as file:
    for line in file:
        keys.append(line.strip())

# establish socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), listenPort))
s.listen(5)

print(socket.gethostname())

while True:
    c, address = s.accept()
    msg = c.recv(1028)
    print(msg.decode("ascii"))

    if msg.decode("ascii") == "HELLO":
        c.send("260 OK".encode("ascii"))
        while True:
            msg = c.recv(1028)

            if msg.decode("ascii") == "DATA":
                data = c.recv(10000)  # Receive the message data
                unescaped_data = data.decode("utf-8").replace("\\.", ".").replace("\\\\", "\\")  # Unescape the line

                # Use SHA-256 to compute the hash
                sha256_hash = hashlib.sha256()
                sha256_hash.update(unescaped_data.encode("utf-8"))
                signature = sha256_hash.hexdigest()

                c.send("270 SIG".encode("ascii"))
                c.send(signature.encode("ascii"))  # Send back the signature

                msg = c.recv(1028)
                if msg.decode("ascii") == "PASS":
                    c.send("260 OK".encode("ascii"))
                elif msg.decode("ascii") == "FAIL":
                    c.send("260 OK".encode("ascii"))
                else:
                    print("error: illegal command, expecting PASS or FAIL")
                    c.close()
                    break
            elif msg.decode("ascii") == "QUIT":
                c.close()
                break
            else:
                print("error: illegal command, expecting DATA or QUIT")
                c.close()
                break
    else:
        print("error: illegal command, expecting HELLO")
        c.close()
