import threading
import socket

host = "127.0.0.1"
port = 55555

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.bind((host, port))
srv.listen()

clts = []
nicks = []


def broadcast(msg):
    for clt in clts:
        clt.send(msg)


def handle(clt):
    while True:
        try:
            msg = clt.recv(1024)
            broadcast(msg)
        except:
            index = clts.index(clt)
            clts.remove(clt)
            clt.close()
            nick = nicks[index]
            broadcast(f"{nick} has disconnected.".encode("ascii"))
            nicks.remove(nick)
            break


def rcv():
    while True:
        clt, adrs = srv.accept()
        print(f"Connected with{str(adrs)}")

        clt.send("NICK".encode("ascii"))
        nick = clt.recv(1024).decode("ascii")
        nicks.append(nick)
        clts.append(clt)

        print(f"The clients nicname is {nick}.")
        broadcast(f"{nick} has connected.".encode("ascii"))
        clt.send("Sucessfully connected to the server.".encode("ascii"))

        thread = threading.Thread(target=handle, args=(clt,))
        thread.start()


print("Server is listening...")
rcv()
