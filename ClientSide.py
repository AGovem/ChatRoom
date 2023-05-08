import socket
import threading
import os


def connect_server():
    os.system("cls")

    global nickname
    global passwd
    nickname = input("Nickname: ")

    ip = input("Write The Server's IP: ") # "localhost"
    port = 8888 #input("Write The Server's PORT NO:")

    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))

stop = False

def receive():
    while True:
        global stop
        if stop:
            break
        try:
            msg = client.recv(1024).decode("utf-8")
            if msg == "NICK":
                client.send(nickname.encode("utf-8"))
            else:
                print(msg)

        except socket.error:
            print("\033[41mERROR Occured\033[m")
            client.close()
            break


def write():
    while True:
        if stop:
            break
        msg = f"{nickname}: \033[32m{input('')}\033[m"
        cik ="-exit"
        if msg == f"{nickname}: \033[32m{cik}\033[m":
            client.send(msg.encode("utf-8"))
            client.close()
            break
        else:
            client.send(msg.encode("utf-8"))

connect_server()
receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()