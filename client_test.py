
import json
import socket
import pprint

client = socket.socket()
host = "127.0.0.1"
port = 1234



client.connect((host, port))
N = 10 # ввести размер "окна"
while True:
    dict_for_send = {
        "position": 0,
        "column": "age",
        "n": N
    }
    print("Введите через пробел: номер позиции, столбец (name, last_name, age, weith) для сортировки:")
    try:
        position, column = input().split()
        dict_for_send = {
            "position": int(position),
            "column" : column,
            "n" : N
        }
    except:
        print("ошибка ввода данных")
    message = json.dumps(dict_for_send)
    client.send(message.encode())
    print("send message")
    request = client.recv(4096)
    data = json.loads(request.decode())
    #print(request)
    pprint.pprint(data)

#client.close()