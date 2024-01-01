import time
from multiprocessing import Manager, Lock
from process import WorkerProcess
from utils import get_metrics, write_metrics


class MainProcess:
    def __init__(self, ports: list[int]):
        self.ports = ports
        self.manager = Manager()
        self.lock = Lock()
        self.messages = self.manager.list()
        self.processes = []

    def start_worker_processes(self):
        for port in self.ports:
            p = WorkerProcess(lock=self.lock, messages=self.messages, port=port)
            p.start()
            self.processes.append(p)

    def terminate_worker_processes(self):
        for p in self.processes:
            p.terminate()
            p.join()

    def message_processing(self):
        messages_for_60_seconds = []
        count_cycle = 0
        while True:
            time.sleep(10)
            with self.lock:
                messages_list = list(self.messages)
                self.messages[:] = []
            if messages_list:
                print(messages_list)
                metrics = get_metrics(messages_list, count_type="10s")
                write_metrics(metrics)
                messages_for_60_seconds.extend(messages_list)
            if count_cycle == 5:
                if messages_for_60_seconds:
                    metrics_for_60_seconds = get_metrics(
                        messages_for_60_seconds, count_type="60s"
                    )
                    write_metrics(metrics_for_60_seconds)
                    messages_for_60_seconds = []
                count_cycle = 0
                continue
            count_cycle += 1

    def run(self):
        try:
            self.start_worker_processes()
            self.message_processing()
        finally:
            self.terminate_worker_processes()


if __name__ == "__main__":
    ports = [8010, 8011, 8012, 8013]
    MainProcess(ports).run()
