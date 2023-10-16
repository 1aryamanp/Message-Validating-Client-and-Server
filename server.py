from fileinput import filename
import socket, sys

# take in arguments
listenPort = int(sys.argv[1])
keyName = sys.argv[2]

#temp debug to check args
# print(listenPort)
# print(keyName)

keys = []

with open(keyName, 'r', encoding='ascii') as file:
    for i, line in enumerate(file):
        keys.append(line.strip())

#establish socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), listenPort))
#temp print to get host name
print(socket.gethostname())
s.listen(5)

#listen for connection
c, address = s.accept()
msg = c.recv(1028)
print(msg.decode("ascii"))
if msg.decode("ascii") == "HELLO":
    c.send("260 OK".encode("ascii"))
    while True:
        msg = c.recv(1028)
        if msg.decode("ascii") == "DATA":
            msg.recv(10000)
            #unescape the line here

            #use sha256 hash here
            c.send("270 SIG".encode("ascii"))
            #send back sig
            msg.recv(1028)
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