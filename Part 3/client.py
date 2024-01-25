import os
import sys
import time
import shutil
import base64
from imports import clientHandshake, DNS_lookup, ipheader

log_path = "log.txt"
request_path = "pipe/request.txt"
response_path = "pipe/response.txt"
connection = "pipe"
clientResource = "clientResources"
clientip = '192.168.1.0'

# Set-up

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

    header = ipheader(clientip, DNS_lookup(server), resources[0], "1", "1")
    
    # Logging request

    request = "{} /{} HTTP/1.1\nHost: {}".format(httpMethod, resources[0], server)
    request = header + "\n\n" + request
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
    
    time.sleep(2)
    os.remove(response_path)

    # Decode image and move it to clientResources

    if httpMethod.strip()=="GET":
        generate = ""
        packets = data.split("\n\n----------------------------\n\n")
        for packet in packets:
            components = packet.split("\n")
            components = list(dict.fromkeys(components))
            components.remove("")
            ext = components[8].replace("Content-Type: ", "")
            if ext!="jpg":
                components.remove("----------------------------")
            ip_header = components[0].split(" | ")
            body = components[2]
            
            if (ip_header[0]==DNS_lookup(server) and ip_header[1]==clientip):
                if (components[1]=="HTTP/1.1 200 OK" and components[3].replace("Server: ", "") == server):
                    new_file = "{}/file.{}".format(clientResource, ext)
                    generate += components[-1]
        
        generate = generate.replace("----------------------------","").replace("==","")
        with open(new_file, "wb") as f:
            f.write(base64.b64decode(generate))

    source = connection + "/" +resources[0]
    if httpMethod == "GET":
        shutil.move(source,clientResource)
