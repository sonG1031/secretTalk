import socket
import threading
import os
import platform

CLS = ""
if platform.system() == "Windows":
    CLS = "cls"
elif platform.system() == "Darwin" or platform.system() == "Linux":
    CLS = "clear"

nickname = input("키미노 나마에와? ")

ip = input("IP: ") # 자기 IP에 맞게 수정하셈 ㅇㅇ
port = int(input("PORT: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "NICK":
                client.send(nickname.encode('utf-8'))
            else:
                nick = message.split(':')[0]
                if nick == nickname:
                    continue
                print(message)
        except:
            print("이세카이 접속 해제")
            client.close()
            break


def write():
    while True:
        try:
            text = input()
            if text == CLS:
                os.system(CLS)
                continue

            message = f'{nickname}: {text}'
            client.send(message.encode('utf-8'))
        except:
            print("이세카이 접속 해제")
            client.close()
            break


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()