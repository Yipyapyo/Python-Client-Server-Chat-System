import socket
import errno
import sys
from datetime import datetime

HEADER_LENGTH = 10
my_username = input("Username: ")

IP = input("What is the IP you want to join? ")
PORT = 1234


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # conenction type, streaming data
client_socket.connect((IP, PORT))  # connect to IP and specific port
client_socket.setblocking(False)  # no messages will be blocked
print("Type your messages here: ")
print("'/disconnect' to disconnect")

username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")  # pad out to 10 bytes
client_socket.send(username_header + username)  # send username length and inputted name

while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:")
    message = input(f"{current_time} {my_username} > ")  # input the message

    if message == "/disconnect" or message == "/DISCONNECT":
        print("You have disconnected")
        input("Press enter to terminate program")
        sys.exit(0)
    else:
        pass

    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message):< {HEADER_LENGTH}}".encode("utf-8")  # pad out to 10 bytes
        client_socket.send(message_header + message)  # send length of message and the message itself
        
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)  # receive 10 bytes to get the user name length
            if not len(username_header):  # if no data is received
                print("Connection closed by the server")
                sys.exit()  # close application
            username_length = int(username_header.decode("utf-8").strip())  # username length is decoded
            username = client_socket.recv(username_length).decode("utf-8")  # receive the username 
            
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")  # receive the message

            now = datetime.now()
            current_time = now.strftime("%H:%M:")
            print(f"{current_time} {username} > {message}")
            
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error", str(e))
            sys.exit()
        continue

    except Exception as e:
        print("General error", str(e))
          
