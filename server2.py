# IDE recommended for testing
import socket
import threading  # create multiple threads in 1 program
import time

# time.sleep(1) #wait for it to finish before printing BUT if each in one thread can run simulatinously
# print("hello")

# HEADER and FORMAT USED IN STEP 3
HEADER = 64  # bytes
FORMAT = 'utf-8'
# USED IN STEP 4
DISCONNECT_MSG = "DISCONNECT"

# STEP 1 ----------------------------------------------------------- PICK THE PORT AND IP ADDRESS
# pick a PORT (above 4000ish become inactive on computer) pick a port which is not in use
PORT = 5050
# get local IP by using ipconfig in command line and get iPv4
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

# STEP 2 ------------------------------------------------PICK A SOCKET AND BIND IT TO THE ADDRESS
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # (family,type)
s.bind(ADDR)  # socket is bound to address

# STEP 3 ---------------------------------------------------MAKE FUNCTIONS FOR CONNECTION HANDLING


def handle_client(conn, addr):  # new thread for handling connections after start()
    # running concurrently for each client
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        # wait to recieve information from the client
        # receive this many bytes from the client
        msg_length = conn.recv(HEADER).decode(FORMAT)
        # if message is more than 64 bytes will not be able to recieve it
        # DECODE message from its byte format into a string using UTF-8
        # convert into an integer
        # NEED TO MAKE SURE WE ARE GETTING A VALID MESSAGE BEFORE CONVERTING
        if msg_length:  # if it is not empty:
            msg_length = int(msg_length)
            # get actual message using number of bytes to recieve and decode
            msg = conn.recv(msg_length).decode(FORMAT)
            # STEP 4 WITHIN 3,------------------------------- DISCONNECTING THE CLIENT FROM SERVER
            if(msg == DISCONNECT_MSG):
                connected = False
            # print message from the address (including disconnect message)
            print(f"[{addr}] [{msg}]")
            # STEP 5---------------------------------- SEND MESSAGE BACK TO CLIENT
            conn.send("Message Recieved!".encode(FORMAT))

    conn.close()  # closes connection


def start():
    s.listen()  # handles NEW connections
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        # blocks until new connection occurs; conn is a socket object and addr is info about the obj
        conn, addr = s.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        # creates new thread, when new connection occurs pass connection to handle_client and the passing arguments
        thread.start()

        # print the number of active threads (active clients), representing num of clients connected
        # -1 since always one thread running
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] SERVER IS STARTING...")
start()
