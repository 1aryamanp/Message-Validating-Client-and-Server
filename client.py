from os import makedirs
import socket
import sys

# read message file
def read_message_file(filename):
    messages = []

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            message = ""
            for line in lines:
                line = line.strip()
                # Check if the line is empty or a number
                if not line or line.isdigit():
                    if message:
                        # Remove the trailing space and append the message
                        message = message.rstrip()
                        messages.append(message)
                    message = ""
                else:
                    message += line + " "
            if message:
                # Remove the trailing space and append the last message
                message = message.rstrip()
                messages.append(message)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    return messages

# read signature file
def read_signature_file(filename): 
    signatures = []

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                signature = line.strip()
                signatures.append(signature)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    
    return signatures
    
    
def main():
        
    if len(sys.argv) != 5:
        print("Incorrect usage of input arguments")
        return
        
    server_name = sys.argv[1]
    server_port = int(sys.argv[2])
    message_file = sys.argv[3]
    sig_file = sys.argv[4]

    #read message and signature files
    messages = read_message_file(message_file)
    signatures = read_signature_file(sig_file)
    

    if len(messages) != len(signatures):
        print("Error: Number of messages and signatures must match")
        return
    
    # open a socket connection

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_name, server_port))

    # send the "HELLO" message

    client_socket.send("HELLO\n".encode("ascii"))

    # recivning 260 OK
    response = client_socket.recv(1024).decode("ascii").strip()
    print(response)

    if response != "260 OK":
        print("Error: Failed to establish a connection with the server")
        client_socket.close()
        return
    
    message_counter = 0
    for message, signature in zip(messages, signatures):
        # send data command
        client_socket.send("DATA\n".encode("ascii"))

        # send the message
        # client_socket.send(f"{len(message)}\n".encode("ascii"))
        client_socket.sendall((message+"\n.\n").encode("ascii"))
        
        response = client_socket.recv(1024).decode("ascii").strip()
        print(response)

        if response != "270 SIG":
            print ("Error: Invalid response from the server")
            # client_socket.close()
            return
        
        received_sig = client_socket.recv(1024).decode("ascii").strip()
        print(received_sig)

        if received_sig == signature:
            print('aryaman')
            client_socket.send("PASS\n".encode("ascii"))
        else:
            print('vraj')
            client_socket.send("FAIL\n".encode("ascii"))
        

        new_response = client_socket.recv(1024).decode("ascii").strip()
        print(new_response)
        
        if new_response != "260 OK":
            print("no 260 OK response to pass/fail")
            #client_socket.close()
            return
        
        message_counter += 1
        
        if message_counter == 10:
            break

    #after sending the quit command
    client_socket.send("QUIT\n".encode("ascii"))
    #close the TCP socket
    client_socket.close()

if __name__ == "__main__":
    main()

       
    
        