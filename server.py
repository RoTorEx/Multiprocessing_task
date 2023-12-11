import time
import socket
import pickle

HOST = 'localhost'
PORT = 0


def send_message():
    """ Отправка сообщений по socket """

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))

    info = {"A1": 3, "A2": 30, "A3": 130}

    while True:

        resp = pickle.dumps(info)
        s.sendto(resp, (HOST, 1080))
        print('Mailing...', resp)
        time.sleep(3)


send_message()