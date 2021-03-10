import concurrent.futures
import http.client
import json
import time


def get_time(name):
    client = http.client.HTTPConnection("worldtimeapi.org")
    client.request("GET", "/api/ip")
    http_response = client.getresponse()
    if http_response.status != 200:
        print(f"Error Response: {http_response.status} {http_response.reason}")
        return

    body = http_response.read()
    response = json.loads(body)
    return f"{name}: {response['datetime']}"


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        get_time_futures = {
            executor.submit(get_time, "Process 1"),
            executor.submit(get_time, "Process 2"),
            executor.submit(get_time, "Process 3"),
        }
        for get_time_future in concurrent.futures.as_completed(get_time_futures):
            try:
                data = get_time_future.result()
            except Exception as exc:
                print(f"Exception: {exc}")
            else:
                print(data)


start = time.time()
main()
finish = time.time()
print(f"Total Time: {finish - start}s")
