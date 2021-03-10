import http.client
import json
import time
import multiprocessing as mp


def get_time(name, q: mp.Queue):
    client = http.client.HTTPConnection("worldtimeapi.org")
    client.request("GET", "/api/ip")
    http_response = client.getresponse()
    if http_response.status != 200:
        print(f"Error Response: {http_response.status} {http_response.reason}")
        return

    body = http_response.read()
    response = json.loads(body)
    q.put(f"{name}: {response['datetime']}")


def main():
    mp.set_start_method('spawn')
    q = mp.Queue()
    p1 = mp.Process(target=get_time, args=("Process 1", q))
    p1.start()
    p2 = mp.Process(target=get_time, args=("Process 2", q))
    p2.start()
    p3 = mp.Process(target=get_time, args=("Process 3", q))
    p3.start()
    p1.join()
    p2.join()
    p3.join()

    while not q.empty():
        print(q.get())


if __name__ == "__main__":
    start = time.time()
    main()
    finish = time.time()
    print(f"Total Time: {finish - start}s")
