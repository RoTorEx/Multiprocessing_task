import socket
import multiprocessing as mp
import json
import time


def worker():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(20):
        time.sleep(5)
        addr = ('127.0.0.1', 8887)
        payload = json.dumps({"A1": 10 + i, "A2": 2 * i, "A3": 100 + i})
        client.sendto(payload.encode("utf-8"), addr)
    client.close()


def process_json(messages, timestamp):
    result = {"timestamp": timestamp, "count_type": "10s", "A1_sum": 0,
              "A2_max": float('-inf'), "A3_min": float('inf')}

    for key, data in messages.items():
        for d in data:
            for key, value in d.items():
                if key == "A1":
                    result["A1_sum"] += value
                elif key == "A2":
                    result["A2_max"] = max(value, result["A2_max"])
                elif key == "A3":
                    result["A3_min"] = min(value, result["A3_min"])
    return result


def minutes_storage_process(messages, timestamp, minutes):
    res = {"timestamp": timestamp, "count_type": "60s", "A1_sum": 0, "A2_max":
           float('-inf'), "A3_min": float('inf')}
    for i in range(minutes - 1, len(messages)):
        res["A1_sum"] += messages[i]["A1_sum"]
        res["A2_max"] = max(res["A2_max"], messages[i]["A2_max"])
        res["A3_min"] = min(res["A3_min"], messages[i]["A3_min"])
    return res


def main():

    data_storage = {}
    minutes_storage = []
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('127.0.0.1', 8887))
    server.settimeout(10.0)
    process = mp.Process(target=worker, args=())
    process.daemon = True
    process.start()
    # process.join()
    delimiter_10_sec = 1
    delimiter_60_sec = 1
    try:
        start_time = int(time.time())
        print('Connection start')
        while True:
            message, address = server.recvfrom(1024)
            current = int(time.time())

            delimiter_10 = int(start_time//10 * 10) + 10
            delimiter_60 = int(start_time//10 * 60) + 60

            if current - (start_time + 10 * delimiter_10_sec) > 0:
                res = process_json(data_storage, delimiter_10)
                delimiter_10_sec += 1

                minutes_storage.append(res)
                data_storage.clear()
            if current - (start_time + 60 * delimiter_60_sec) > 0:
                delimiter_60_sec += 1
                res = minutes_storage_process(minutes_storage, delimiter_60,
                                              delimiter_60_sec)
                minutes_storage.append(res)
            if data_storage.get(delimiter_10):
                data_storage[delimiter_10].append((json.loads(
                    message.decode('utf-8'))))
            else:
                data_storage[delimiter_10] = [json.loads(
                    message.decode('utf-8'))]
    except TimeoutError:
        print('Connection closed')
        server.close()
    for message in minutes_storage:
        print(json.dumps(message, indent=4))


if __name__ == '__main__':
    main()
