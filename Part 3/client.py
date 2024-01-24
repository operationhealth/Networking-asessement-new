import os
import sys
import time
import shutil
from imports import clientHandshake, DNS_lookup, ipheader

log_path = "log.txt"
request_path = "pipe/request.txt"
response_path = "pipe/response.txt"
connection = "pipe"
clientResource = "clientResources"
clientip = '192.168.1.0'

# Set-up

# client = sys.argv[1]
url = sys.argv[1]
paths = url.replace("http://","").split("/")
server = paths[0]
resources = paths[1:]
httpMethod = sys.argv[2].upper()

handshake = False

if (os.path.isdir(connection)):
    handshake = True
else:
    handshake = clientHandshake()

if handshake :
    print(server)
    print(DNS_lookup(server))

    header = ipheader(clientip, DNS_lookup(server), resources[0], "1", "1")

    # Logging request

    request = "{} /{} HTTP/1.1\nHost: {}".format(httpMethod, resources[0], server)
    request = header + "\n" + request
    log = "\n\n" + request + "\n\n----------------------------"

    if (not os.path.isfile(log_path)) :
        f = open(log_path, "x")
        f.close()

    if (os.stat(log_path).st_size == 0):
        log =  "----------------------------" + log

    with open(log_path, "a") as pipe:
        pipe.write(log)
        print("\nRequest logged!")

    # Sending request

    with open(request_path, "w") as pipe:
        pipe.write(request)
        print("Request sent!")

    # Waiting for response

    while (not os.path.isfile(response_path)) :
        pass
    time.sleep(2)

    # Receive response

    print("\nResponse received!\n")

    with open(response_path, "r+") as response:
        data = response.read()
    print(data)
    os.remove(response_path)

    source = connection + "/" +resources[0]
    shutil.move(source,clientResource)
