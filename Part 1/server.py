import os
import datetime

log_path = "log.txt"
request_path = "request.txt"
response_path = "response.txt"

# Waiting for request

while (not os.path.isfile(request_path)) :
    pass

# Receive request

print("\nRequest received!\n")

with open(request_path, "r+") as request:
    data = request.read()
    print(data)

os.remove(request_path)

if data:
    start = data.index("Host") + 6
    server = data[start:]

# Logging response

date = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")

response = """HTTP/1.1 200 OK
Date: {}
Server: {}
Last-Modified:
Accept-Ranges: bytes
Content-Length:
Connection: open
Content-Type:""".format(date, server)

log = "\n\n" + response + "\n\n----------------------------"

with open(log_path, "a") as pipe:
    pipe.write(log)
    print("\nResponse logged!")

# Sending response

with open(response_path, "w") as pipe:
    pipe.write(response)
    print("Response sent!")