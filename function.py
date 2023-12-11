import pickle
import json
import socket
from multiprocessing import Process, Queue
import time
from datetime import datetime, timedelta


HOST = 'localhost'
PORT = 1080


class Worker(Process):
    """ Класс получения данных по socket"""
    
    def __init__(self, dt_queue):
        super().__init__()
        self.dt_queue = dt_queue

    def run(self) -> None:
        """ Запуск процесса worker"""
        wk_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        wk_socket.bind((HOST, PORT))

        received_data = []
        while True:
            data, _ = wk_socket.recvfrom(1024)
            if not data:
                wk_socket.close()
                break
            json_data = pickle.loads(data)
            received_data.append(json_data)
            self.dt_queue.put(received_data)
            print('Receiving ...', json_data)



class Master(Process):
    """ Класс для обработки данных из очереди от worker """
    
    def __init__(self, dt_queue):
        super().__init__()
        self.dt_queue = dt_queue

    def run(self) -> None:
        """
        Запуск процесса master
        """
        while True:
            self.metrics_counts()
        # if data:
        #     self.terminate()

    def metrics_counts(self):
        """ """
        data = self.get_data()
        print('-----', data)
        result = self.my_interval(data)
        print(result)
        self.to_json(result)

    def get_data(self):
        """
        Агрегация данных от worker
        :return: полученные данные
        """

        time.sleep(3)
        data = self.dt_queue.get()
        print(type(data))
        return data

    # def terminate(self) -> None:
    #     """ Завершение процессов """
    #     time.sleep(30)
    #     return super().terminate()

    @staticmethod
    def to_json(data):
        """
        Метод для записи в json файл
        """
        with open('metrics.json', 'a') as file:
            file.write(json.dumps(data))

    @staticmethod
    def my_interval(received_data):
        result = []
        short_interval = datetime.now()
       # long_interval = datetime.now()
        for d in received_data:
            current_time = datetime.now()
            # if current_time - long_interval <= timedelta(seconds=61):
            #     long_interval = datetime.now()
            #     for r in result:
            #         st_result = {"timestamp": int(time.time()),
            #                      "count_type": '60s',
            #                      "A1_sum": 0,
            #                      "A2_max": 0,
            #                      "A3_min": float('inf')
            #                      }
            #         short_interval = datetime.now()
            #         st_result['count_type'] = '10s'
            #         st_result['A1_sum'] += d.get('A1_sum', 0)
            #         st_result['A2_max'] = max(st_result['A2_max'], r.get('A2_max', 0))
            #         st_result['A3_min'] = min(st_result['A3_min'], r.get('A3_min', float('inf')))
            #         result.append(st_result)

            if current_time - short_interval <= timedelta(seconds=10):
                start_dict = {"timestamp": int(time.time()),
                              "count_type": '10s',
                              "A1_sum": 0,
                              "A2_max": 0,
                              "A3_min": float('inf')
                              }
                short_interval = datetime.now()
                start_dict['count_type'] = '10s'
                start_dict['A1_sum'] += d.get('A1', 0)
                start_dict['A2_max'] = max(start_dict['A2_max'], d.get('A2', 0))
                start_dict['A3_min'] = min(start_dict['A3_min'], d.get('A3', float('inf')))
                time.sleep(3)
            result.append(start_dict)
        return result


def main():
    dt_queue = Queue()
    worker = Worker(dt_queue)
    master = Master(dt_queue)
    worker.start()
    master.start()

