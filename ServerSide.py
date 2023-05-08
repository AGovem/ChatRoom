import socket
import threading
import os

host = "192.168.1.42"
port = 8888

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

nicknames = []
clients = []

red = "\033[31m"
green = "\033[32m"
cyan = "\033[36m"
off = "\033[m"


def broadcast(client, message):
    for cli in clients:
        if cli != client:
            cli.send(message.encode("utf-8"))


def handle(client):
    nickname = nicknames[clients.index(client)]
    while True:
        try:
            msg = client.recv(1024).decode("utf-8")
            broadcast(client, msg)

        except socket.error:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(client, f"\033[34m{nickname}\033[m Left The Chat!")
                nicknames.remove(nickname)
                break


def main():
    while True:
        global client
        client, address = server.accept()
        print(f"{address} Connected To Server!")

        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")

        nicknames.append(nickname)
        clients.append(client)

        print(f"{nickname} Connect To Server")
        broadcast(client, f"\033[34m{nickname} Joined The Chat Room\033[m")
        client.send("\033[45mSuccessfully Connected To Server!\033[m".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server Is Working...")
main()
