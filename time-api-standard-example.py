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
    print(get_time("Process 1"))
    print(get_time("Process 2"))
    print(get_time("Process 3"))


start = time.time()
main()
finish = time.time()
print(f"Total Time: {finish - start}s")
