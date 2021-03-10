import asyncio
import json
import time


async def get_time(name):
    reader, writer = await asyncio.open_connection("worldtimeapi.org", 80)
    request = (b"GET /api/ip HTTP/1.1\r\n"
               b"host: worldtimeapi.org\r\n"
               b"Content-Length: 0\r\n"
               b"\r\n")
    writer.write(request)
    await writer.drain()

    _, stats_code, status_text = (await reader.readline()).split(b" ", 2)
    if stats_code != b"200":
        print(f"Error Response: {stats_code} {status_text}")
        return

    content_length = 0
    response_headers = []
    while header_line := await reader.readline():
        stripped_header_line = header_line.decode("latin-1").rstrip()
        if not stripped_header_line:
            break
        header_key, header_value = stripped_header_line.split(":", 1)
        if header_key.lower() == "content-length":
            content_length = int(header_value)
        response_headers.append((header_key, header_value.strip()))

    body = await reader.read(content_length)

    writer.close()
    response = json.loads(body)
    await writer.wait_closed()
    return f"{name}: {response['datetime']}"


async def main():
    for coro in asyncio.as_completed((
        get_time("Process 1"),
        get_time("Process 2"),
        get_time("Process 3"),
    )):
        print(await coro)

start = time.time()
asyncio.run(main())
finish = time.time()
print(f"Total Time: {finish - start}s")
