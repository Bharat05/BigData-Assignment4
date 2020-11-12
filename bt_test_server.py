""" Server for multithreated (asynchronous chat) application 
Adapted from https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170"""

import socket
# from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


# Defining constants
clients = {}
addresses = {}

HOST = socket.gethostbyname(socket.gethostname())
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
# should we call this socket?
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print(f"{client_address} has connected.")
        client.send(bytes("Greetings from Houston!"
                          "Please type your name and press enter!",
                          "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    """ Handles a single client connection."""
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = (f"Welcome {name}! If you ever want to quit, type 'quit'"
               "to quit.")
    msg = (f"{name} has joing the chat!")
    client.send(bytes(msg, "utf8"))
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("quit", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("quit", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes(f"{name} has left the chat.", "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification
    """ Broadcasts a message to all the client. """
    for client in clients:
        client.send(bytes(prefix, "utf8") + msg)


if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 Connections
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
