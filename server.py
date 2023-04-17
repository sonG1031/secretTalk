import threading
import socket


def get_open_port(): # 사용가능한 포트 얻는 함수
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


ip = '127.0.0.1' # 자기 IP에 맞게 수정하셈 ㅇㅇ
port = get_open_port()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen()
print(f"{ip}:{port}/대기중...")

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f">>> {nickname}쿤 사요나라 -_-".encode('utf-8'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f">>> {address}/이세카이 전생중!")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'>>> {nickname}쿤 이세카이 소환 성공!')
        broadcast(f'>>> {nickname}쿤 이세카이 소환 성공!\n'.encode('utf-8'))
        client.send('>>> 이세계로 전생 완료!\n'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == "__main__":
    try:
        receive()
    except:
        print("이세카이 제거")