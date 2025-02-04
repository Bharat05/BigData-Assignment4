#  !/home/dev/anaconda3/bin/python
"""Script for Tkinter GUI chat client 
Adapted from https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170"""


"""Script for Tkinter GUI chat client."""
import socket
# from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "quit":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("quit")
    send()

def myquit():
    print('Quit Handler')
    client_socket.send(bytes('quit', "utf8"))
    client_socket.shutdown(1)
    client_socket.close()
    top.protocol("WM_DELETE_WINDOW", on_closing)
    exit()

top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
# To navigate through past messages.
scrollbar = tkinter.Scrollbar(messages_frame)
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15,
                           width=128, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
exit_button = tkinter.Button(top, text="Quit", command=myquit)
exit_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
# HOST = socket.gethostbyname(socket.gethostname())
# PORT = 33000
HOST = input('Enter host: ')
HOST = socket.gethostbyname(HOST)
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

print(ADDR)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
