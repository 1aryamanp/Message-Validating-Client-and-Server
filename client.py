import socket, sys

#take in arguments
serverName = sys.argv[1]
serverPort = int(sys.argv[2])
msgName = sys.argv[3]
sigName = sys.argv[4]

#temp debug to check args
# print(serverName)
# print(serverPort)
# print(msgName)
# print(sigName)

msgSizes = []
msgBytes = []
signatures = []

with open(msgName, 'r', encoding='ascii') as file:
 for i, line in enumerate(file):
  if i%2==0:
   msgSizes.append(int(line.strip()))
  else:
   tempBytes = bytes(line.strip(),'ascii')
   msgBytes.append(tempBytes) 
    
with open(sigName, 'r', encoding='ascii') as file:
 for i, line in enumerate(file):
  signatures.append(line.strip())
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverName, serverPort))

s.send("HELLO".encode("ascii"))

msg = s.recv(128)
if msg.decode("ascii") != "260 OK":
 print("error: expected 260 OK")
 exit()

# escape the message here
escapedMsg = []
for byte in msgBytes:
 if byte == 34:
  escapedMsg.append(92)
  escapedMsg.append(34)
 else:
  escapedMsg.append(byte)

# decode the escaped message to a string using the unicode_escape encoding with the backslashreplace error handler
escapedMsgString = bytes(escapedMsg).decode("unicode_escape", "backslashreplace")

# create a bytearray from the escaped message string
escapedMsgByteArray = bytearray(escapedMsgString)

# send the escaped message
s.send(escapedMsgByteArray)

msg = s.recv(128)
if msg.decode("ascii") != "270 SIG":
 print("error: expected 270 SIG")
 exit()

# receive the signature
signature = s.recv(10000)

# compare the signature to the expected signature
if signature == signatures[0]:
 s.send("PASS".encode("ascii"))
else:
 s.send("FAIL".encode("ascii"))

# receive the response from the server
msg = s.recv(128)
if msg.decode("ascii") != "260 OK":
 print("error: expected 260 OK")
 exit()

# close the socket
s.close()