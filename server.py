#!/bin/python3
'''
Код для сервера на удаленой машине в интернете 
'''
import socket #Импортируем библиотеку для работы с сокетом
import threading #Импортируем бибилиотеку для поддержики многопотомчности кода

# Connection Data
host = '90.156.227.3' #Воодим сюда ip адрес сервера, где будет сокет в состоянии lisen
port = 55555 #Порт, который будет прослушивать входящие SYN пакеты

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Для "старта" сервера, вызваем функцию socket() 
#из библиотеки socket. Функция принимает два параметра, первыйы параметр - IPv4, второй параметр - тип socket-а.
#DGRAM - UDP, SOUC_STREAM - TCP
server.bind((host, port)) #Привязываем наш socket к ip b порту
server.listen() #Переводим socket в слушающее состояние. 

# Lists For Clients and Their Nicknames
clients = [] #Массив для клиентов
nicknames = [] #Массив для никнеймов

# Sending Messages To All Connected Clients
def broadcast(message): #Функция для рассылки сообщений. Любое сообщение на вход - отправляется всем клиентам.
    for client in clients: #для каждого элемента в коллекции clients
        client.send(message) #пересылаеется message с помощью функции send()

# Handling Messages From Clients
# Обрабатываем сообщения от клиентов. 
def handle(client):
    client.send('NICK'.encode('utf-8'))
    nickname = client.recv(1024).decode('utf-8')
    if nickname in nicknames:
        client.send('Nickname already taken! Please choose another nickname.'.encode('utf-8'))
        client.close()
        return
    nicknames.append(nickname)
    clients.append(client)
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024) #Принимаем сообщения с помошью функции recv()
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client) 
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        #Здесь, в бесконечном цикле, ждем SYN - SYN\ACK - ACK обмена.
        # Accept Connection
        client, address = server.accept() # здесь возвращатеся socket в состоянии ESTABLISHED
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname) # Добавляем в массив никнейм
        clients.append(client) # Добавляем в наш массив socket

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname)) # Выводим сообещие, кто присоединился 
        broadcast("{} joined!".format(nickname).encode('ascii')) # Рассылаем броадкаст сообщение
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,)) # С помощью функции Thread() библиотеки threading
        # запускаем отдельный поток для функции handle с аргументом client
        thread.start()

print("Server if listening...")
receive()
