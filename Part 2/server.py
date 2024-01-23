import os
import shutil
from imports import serverHandshake

log_path = "log.txt"
request_path = "pipe/request.txt"
response_path = "pipe/response.txt"
connection = "pipe"
serverResource = "serverResources"
file = ""

handshake = False

if (os.path.isdir(connection)):
    handshake = True
else:
    handshake = serverHandshake()

if handshake:

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
        start = data.index("/")
        end = data.index(" HTTP/1.1")
        file = data[start+1:end]

    # Logging response

    response = "HTTP/1.1 200 OK"
    log = "\n\n" + response + "\n\n----------------------------"

    with open(log_path, "a") as pipe:
        pipe.write(log)
        print("\nResponse logged!")

    # Sending response
    
    source = serverResource + "/" + file

    with open(response_path, "w") as pipe:
        shutil.copy(source,connection)
        pipe.write(response)
        print("Response sent!")