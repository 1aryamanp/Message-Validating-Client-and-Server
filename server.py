import socket
import hashlib
import sys


def unescape(line):
    line = line.replace("\\.",".")
    #line = line.replace("\n.","").replace("\n","")
    line = line.replace("\.", ".")
    line = line.replace("\n.\n","")
    return line

    
def main():
    # Check if the correct number of command line arguments are provided
    if len(sys.argv) != 3:
        print("Incorrect usage")
        return
    
    # Get the listen port and key file path from command-line args
    listen_port = int(sys.argv[1])
    key_file = sys.argv[2]

    # Read in the keys * readline() function, append grpme
    
    keys = []
    # key_index = 0
    with open(key_file, "r") as key_file:
        line = key_file.readline()
        while line: # while there are more lines in the messages
            keys.append(line.strip())
            line = key_file.readline() # after stripping, read more
    
    i = 0

    # Create a socket and start listening on the specified port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a new socket
    server_socket.bind(("localhost", listen_port)) # binds the socket to the specified address and port. it binds it to the localhost. * not 0.0.0.0
    server_socket.listen(1) #starts listening on the specified port, 1 is the max num of queued connection. 1 connection at a time

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1024).decode("ascii")

        if request == "HELLO\n":
            #  sending the 260 OK response to acknowledge the hello
            print(request)
            client_socket.send("260 OK\n".encode("ascii"))
        else:
            # to handle invalid request from client
            print("Error: invalid request from client")
            client_socket.close()
            server_socket.close() # close the server socket to exit the program
            return
        
        while True:
            command = client_socket.recv(1024).decode("ascii") # client should potentially send a DATA command...

            if not command:
                break

            #print received command .. should be printing DATA
            print(command)
            

            if command == "DATA\n":
                while True:
                    
                    # reciving message from the client
                    line = client_socket.recv(1024).decode("ascii")#.strip
                    #print(line)
                    
                    # unescaping the message (have to fix)
                    line = unescape(line)
                    #print(line)
                    
                    
                    # encoding using hash & sending to SHA 256
                    message_hash = hashlib.sha256(line.encode("ascii") + keys[i].encode("ascii"))
                    # print(message_hash)

                    # equivalent hexadecimal value
                    hash_value = message_hash.hexdigest()
                    # print(hash_value)
                    
                    #print message
                    
                    print(line)
                    
                    # send the 270 SIG status code and the updated hash to the client
                    #client_socket.send(b"270 SIG\n".encode("ascii"))
                    client_socket.send(b"270 SIG\n")
                    client_socket.send((hash_value+"\n").encode("ascii"))

                    # pass_or_fail check from the client after sending message back
                    pass_or_fail = client_socket.recv(1024).decode("ascii")
                     # prints whatever response client sent

                    if pass_or_fail == "PASS\n":
                        # Handle the case where the client passed the validation
                        print(pass_or_fail)
                    elif pass_or_fail == "FAIL\n":
                        # Handle the case where the client failed the validation
                        print(pass_or_fail)
                    else:
                        print("Invalid response from client")
                        client_socket.close()
                        break

                    i += 1
                    
                    # sending 260 ok
                    client_socket.send("260 OK\n".encode("ascii"))
                    break

            elif command == "QUIT\n":
                # print and acknowledge quit command ^ i guess it is already coded above ?
                # close the socket and exit the program
                client_socket.close()
                quit()
                break
            
            else:
                print(f"Invalid command from client: {command}")
                break

if __name__ == "__main__":
    main()