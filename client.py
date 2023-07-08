
import socket #Импортируем библиотеку для работы с сокетом
import threading #Импортируем бибилиотеку для поддержики многопотомчности кода

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #создаем наш сокет.
client.connect(('90.156.227.3', 55555)) #коннектимся к нашему серверу.

# Listening to Server and Sending Nickname
def receive(): # Функция, которая принимает сообщения от сервера
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

def write(): # Функция для вывода сообщения с консоли
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('utf-8'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()










