import os
import shutil
import datetime
import time
from imports import serverHandshake

log_path = "log.txt"
request_path = "pipe/request.txt"
response_path = "pipe/response.txt"
connection = "pipe"
serverResource = "serverResources"
item = ""
filetype = ""
server = ""
httpMethod = ""

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
        httpMethod = data[:start-1]
        end = data.index(" HTTP/1.1")
        item = data[start+1:end]
        start = item.index(".") + 1
        filetype = item[start:]
        start = data.index("Host") + 6
        server = data[start:]

    # Logging response
        
    date = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    filesize = os.path.getsize(serverResource + "/" + item)

    x = os.path.getmtime(serverResource + "/" + item)
    lastModified = time.ctime(x)

    response = """HTTP/1.1 200 OK
Date: {}
Server: {}
Last-Modified: {}
Accept-Ranges: bytes
Content-Length: {}
Connection: open
Content-Type: {}""".format(date, server, lastModified, filesize, filetype)
    
    source = serverResource + "/" + item
    
    if (httpMethod=="GET"):
        if (filetype=="txt" or filetype=="html"):
            mode = "r"
        else:
            mode = "rb"
        with open(source,mode) as f:
            content = f.read()
        response = response + "\n\n" + content

    log = "\n\n" + response + "\n\n----------------------------"

    with open(log_path, "a") as pipe:
        pipe.write(log)
        print("\nResponse logged!")

    # Sending response

    with open(response_path, "w") as pipe:
        shutil.copy(source,connection)
        pipe.write(response)
        print("Response sent!")