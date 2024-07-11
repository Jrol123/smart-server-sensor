import socket

UDP_IP = "fe80::2812:caa2:9b2d:c2ea"  # Замените на ваш серверный IPv6-адрес
UDP_PORT = 5000  # Замените на ваш порт

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
# sock.connect((UDP_IP, UDP_PORT))
# sock.listen()
sock.bind((UDP_IP, UDP_PORT))  # Определяем scope_id для IPv6-адреса, если он необходим

print("UDP сервер запущен")

while True:
    print("feskf[efk]")
    data, addr = sock.recv(22)  # Принимаем данные из сокета
    print("Получено сообщение:", data.decode())
