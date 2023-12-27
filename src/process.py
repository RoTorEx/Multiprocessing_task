import json
import socket
from multiprocessing import Process, Lock
from multiprocessing.managers import ListProxy


class WorkerProcess(Process):
    def __init__(self, lock: Lock, messages: ListProxy, port: int):
        super(WorkerProcess, self).__init__()
        self.lock = lock
        self.messages = messages
        self.port = port

    def run(self):
        self.read_message()

    def read_message(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(("localhost", self.port))
            while True:
                message, _ = sock.recvfrom(1024)
                message_data = json.loads(message.decode("utf-8"))
                self.update_data(message_data)

    def update_data(self, message_data: dict):
        with self.lock:
            self.messages.append(message_data)
