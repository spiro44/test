import random
import openpyxl
#import bisect
#import operator
import time
from threading import Thread
import datetime
import json
import socket


class Person_string:
    '''
    data = {
        "name": "Alan",
        "last_name": "Smith",
        "age": 0,
        "weith": 0
        }
    age = 0
    '''
    def __init__(self, data):
        self.data = data
        self.age = data["age"]


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
    data = {
        "name": random.choice(list_names),
        "last_name": random.choice(list_last_names),
        "age": random.choice(range(21, 80)),
        "weith": random.choice(range(60, 120))
    }
    return Person_string(data)

def add_person_in_data(data_in_ram, list_names, list_last_names):
    temp_person = generate_person(list_names, list_last_names)
    for key_temp in data_in_ram.keys():
        data_in_ram[key_temp].append(temp_person)

def delete_person_in_data(data_in_ram, temp_person):
    for key_temp in data_in_ram.keys():
        data_in_ram[key_temp].remove(temp_person)

def sorted_data_in_ram(data_in_ram):
    for key_temp in data_in_ram.keys():
        data_in_ram[key_temp] = sorted(data_in_ram[key_temp], key=lambda x: x.data.get(key_temp))

def initial_generate_data(list_names, list_last_names):
    data_in_ram = {
        "name"     : [],
        "last_name": [],
        "age"      : [],
        "weith"    : []
    }
    for i in range(0, 1000000):
        add_person_in_data(data_in_ram, list_names, list_last_names)
    sorted_data_in_ram(data_in_ram)
    #bisect.insort_left(data_in_ram[key_temp], temp_person, key=lambda x: x.data.get(key_temp))
    return data_in_ram

def continue_modify_data(data_in_ram, list_names, list_last_names):
    #i = 1
    while True:
        print(1, datetime.datetime.now())
        flag = random.choice(['add', 'modify', 'delete'])
        print(2, datetime.datetime.now())
        random_position = random.choice(range(0, len(data_in_ram["name"])))
        print(3, datetime.datetime.now())
        random_person_string = data_in_ram["name"][random_position]
        print(4, datetime.datetime.now())
        if flag == 'add':
            add_person_in_data(data_in_ram, list_names, list_last_names)
            #sorted_data_in_ram(data_in_ram)
            print(5, datetime.datetime.now())
        elif (flag == 'delete') and (len(list(data_in_ram.keys())) > 1):
            delete_person_in_data(data_in_ram, random_person_string)
            print(6, datetime.datetime.now())
        elif flag == 'modify':
            delete_person_in_data(data_in_ram, random_person_string)
            print(7, datetime.datetime.now())
            add_person_in_data(data_in_ram, list_names, list_last_names)
            print(8, datetime.datetime.now())
            #sorted_data_in_ram(data_in_ram)
        #time.sleep(0.005)
        #print(i)
        #i += 1
        #print_current_data(data_in_ram)

def print_current_data(data_in_ram):
    for key in data_in_ram.keys():
        print(key)
        for temp_str in data_in_ram[key]:
            print(temp_str.data)

def request_list_test(data_in_ram, column, position, n):
    while True:
        sorted_data = data_in_ram[column][position:position + n]
        for temp_string in sorted_data:
            print(temp_string.data)
        input()

if __name__ == "__main__":
    list_names, list_last_names = read_xls_to_dict("names.xlsx")
    #print(generate_person(list_names, list_last_names).data)

    data_in_ram = initial_generate_data(list_names, list_last_names)

    #print_current_data(data_in_ram)

    column = "name"
    position = 20
    n = 50
    t = Thread(target=continue_modify_data, args=(data_in_ram, list_names, list_last_names))
    t2 = Thread(target=request_list_test, args=(data_in_ram, column, position, n))
    t.start()
    t2.start()
