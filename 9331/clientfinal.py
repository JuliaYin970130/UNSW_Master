import sys
import socket
import time

server_ip = sys.argv[1]
server_port = int(sys.argv[2])
server_address = (server_ip,server_port)

# initialize

client_socket = None
username = ''
is_login = False
temp_id = ''
contact_log_list = []
contact_log_file = None
contact_log_lock = None


# connection
try:
    client_socket = socket.socket()
    client_socket.connect(server_address)
except:
    print("connection: error")
    exit()


# login
def log_in():
    new_username = input("username:")
    new_password = input("password:")
    massage = "login:" + new_username + ":" + new_password
    client_socket.send(massage.encode())
    receive = client_socket.recv(1024).decode()

    if receive == "login:0":
        print("Welcome to the BlueTrace Simulator!")
        return True, new_username

    elif receive == "login:1":
        print("Invalid Password. Please try again.")
    elif receive == "login:2":
        print("Invalid Password. Your account has been blocked. Please try again later.")
    elif receive == "login:3":
        print("Username does not exist.")
    elif receive == "login:4":
        print("User already login.")

def donwload_tempID():
    pass

# start
while True:
    while not is_login:
        is_login, username = log_in()
        massage = input()
        if massage == "Donload_tempID":
            message = "tempID:" + username
            client_socket.send(massage.encode())
            receive = client_socket.recv(1024).decode()






