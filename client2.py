# to send objects instead of a string (by "pickling" which serializes them)
import pickle

import socket
# SAME AS IN SERVER

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to server, similar to bind in the server file, will use address that pair server and port
client.connect(ADDR)

# since connected need to find way to send a message


def send(msg):
    message = msg.encode(FORMAT)  # need to encode string into byte-format
    # since first message is length of first messsage to send need the length
    msg_length = len(message)  # encode this as a string
    send_length = str(msg_length).encode(FORMAT)

    # pad it to make it 64 bytes long (the header)
    # byte representation will be the string += (64 - len of message) number of bytes for padding
    send_length += b' ' * (HEADER - len(send_length)
                           )  # so that the total is 64

    client.send(send_length)
    client.send(message)

    # recieve message from server
    # make sure can handle what message will be sent back
    print(client.recv(2048).decode(FORMAT))

 # send to server


m = input("Message to send (input q to quit): ")

while m != 'q':
    send(m)
    # press space to send message
    m = input("Press enter to send a message(q to quit): ")

send(DISCONNECT_MESSAGE)


# TO SEND MESSAGES FROM CLIENT TO CLIENT
# need to store a list of messages globally AFTER they are recieved by the server need to add to the
# list and send it back to each client. Make another protocol or thread

# TO USE ON MULTIPLE CLIENTS/COMPUTERS
# just download the client script and run on the other computer (while server is running on the original host)
# works as long as it is on the same wifi network!!!!!

# TO WORK OVER THE INTERNET
# look up public IP address (google my public ip address)
# in SERVER script change server to the public IP address (might have issues with fire wall specifically
# on the server side maybe client too)
