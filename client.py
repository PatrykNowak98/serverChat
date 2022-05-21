import socket
import threading

nick = input("Choose your nickname: ")

clt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clt.connect(("127.0.0.1", 55555))

def rcv():
    while True:
        try:
            msg = clt.recv(1024).decode("ascii")
            if msg == "NICK":
                clt.send(nick.encode("ascii"))
            else:
                print(msg)
        except:
            print("Error")
            clt.close()
            break

def wr():
    while True:
        msg = f"{nick}: {input('')}"
        clt.send(msg.encode("ascii"))

recieve_thread = threading.Thread(target=rcv)
recieve_thread.start()

write_thread = threading.Thread(target=wr)
write_thread.start()
