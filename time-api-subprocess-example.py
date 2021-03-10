from subprocess import DEVNULL, PIPE, Popen
import json
import time


def main():
    subprocs = (
        ("Process 1", Popen(["/usr/bin/curl", "http://worldtimeapi.org/api/ip"], stdout=PIPE, stderr=DEVNULL)),
        ("Process 2", Popen(["/usr/bin/curl", "http://worldtimeapi.org/api/ip"], stdout=PIPE, stderr=DEVNULL)),
        ("Process 3", Popen(["/usr/bin/curl", "http://worldtimeapi.org/api/ip"], stdout=PIPE, stderr=DEVNULL)),
    )

    for entry in subprocs:
        name, subproc = entry
        stdout, stderr = subproc.communicate()
        response = json.loads(stdout)
        print(f"{name}: {response['datetime']}")


start = time.time()
main()
finish = time.time()
print(f"Total Time: {finish - start}s")
