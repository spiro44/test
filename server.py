import random
import openpyxl
from threading import Thread
import socket
import json


def read_xls_to_dict(filename):
    workbook1 = openpyxl.load_workbook(filename)
    sheet1 = workbook1.worksheets[0]
    list_names =[]
    for row in sheet1.rows:
        list_names.append(row[0].value)
    sheet2 = workbook1.worksheets[1]
    list_last_names =[]
    for row in sheet2.rows:
        list_last_names.append(row[0].value)
    return list_names, list_last_names

def generate_person(list_names, list_last_names):
    return {
            "name"      : random.choice(list_names),
            "last_name" : random.choice(list_last_names),
            "age"       : random.choice(range(21,80)),
            "weith"     : random.choice(range(60,120))
        }
def initial_generate_data(list_names, list_last_names):
    data_in_ram = {}
    for index_string in range(0, 10000):
        data_in_ram[index_string] = generate_person(list_names, list_last_names)
    return data_in_ram

def continue_modify_data(data_in_ram, list_names, list_last_names):
    while True:

        flag = random.choice(['add', 'modify', 'delete'])
        last_key_data = max(data_in_ram.keys())
        random_key_data = random.choice(list(data_in_ram.keys()))
        if (flag == 'add') and (len(list(data_in_ram.keys())) < 10000):
            current_key = last_key_data + 1
            data_in_ram[current_key] = generate_person(list_names, list_last_names)
        elif (flag == 'delete') and (len(list(data_in_ram.keys())) > 1):
            data_in_ram.pop(random_key_data)
        elif flag == 'modify':
            data_in_ram[random_key_data] = generate_person(list_names, list_last_names)
        #time.sleep(0.005)


def sorted_index_by_column(data_in_ram, column="age"):
    t_list = data_in_ram.keys()
    test_dict = {key: data_in_ram[key][column] for key in t_list if key in data_in_ram.keys()}
    sorted_tuple = sorted(test_dict.items(), key=lambda x: x[1])
    test_list = [i[0] for i in sorted_tuple]
    return test_list

def print_current_data(data_in_ram, sorted_list, position, n):
    temp_list = sorted_list[position:position + n]
    for index_string in temp_list:
        if index_string in data_in_ram.keys():
            template_print = '''index: {index:5} name: {name:8} last_name: {last_name:8} age : {age:9} weith :{weith}'''.format(
            index = index_string,
            **data_in_ram[index_string]
            )
        print(template_print)

def request_list_test(data_in_ram, column):
    while True:
        sorted_list = sorted_index_by_column(data_in_ram, column=column)
        #print_current_data(data_in_ram, sorted_list, position, n)
        #input()
        return sorted_list

def create_client_data(data_in_ram, sorted_list, position, n):
    client_dict = {}
    temp_list = sorted_list[position:position + n]
    for index_string in temp_list:
        if index_string in data_in_ram.keys():
            client_dict[index_string] = data_in_ram[index_string]
    return client_dict

def server_lst(server, data_in_ram):
    server.listen(5)
    print("Server ready")
    '''
    column = "name"
    position = 20
    n = 50
    '''
    while True:
        client, address = server.accept()
        print("client connect", address)
        while True:
            message = client.recv(4096)
            print("message", message)
            dict_client = json.loads(message.decode())
            column, position, n = dict_client["column"], dict_client["position"], dict_client["n"]
            sorted_list = sorted_index_by_column(data_in_ram, column=column)
            print(sorted_list)
            client_dict = create_client_data(data_in_ram, sorted_list, position, n)
            data_string = json.dumps(client_dict)
            print('Адрес подключения:', address)
            client.send(data_string.encode())
            print("отправлено")
    #client.close()

if __name__ == "__main__":

    list_names, list_last_names = read_xls_to_dict("names.xlsx")
    data_in_ram = initial_generate_data(list_names, list_last_names)
    print("Initial data is ready")
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )
    host = "127.0.0.1"
    port = 1234
    server.bind((host, port))

    t = Thread(target=continue_modify_data, args=(data_in_ram, list_names, list_last_names))
    #t2 = Thread(target=request_list_test, args=(data_in_ram, column, position, n))
    t2 = Thread(target=server_lst, args=(server, data_in_ram))
    t.start()
    t2.start()



