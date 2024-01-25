import os
import shutil
import datetime
import time
from imports import serverHandshake, packetsplit, ipheader
import base64

log_path = "log.txt"
request_path = "pipe/request.txt"
response_path = "pipe/response.txt"
connection = "pipe"
serverResource = "serverResources"
item = ""
filetype = ""
server = ""
httpMethod = ""
server_ip = '192.168.1.1'

handshake = False

if (os.path.isdir(connection)):
    handshake = True
else:
    handshake = serverHandshake()

if handshake:

    # Waiting for request

    while (not os.path.isfile(request_path)) :
        pass
    time.sleep(1)

    # Receive request

    print("\nRequest received!\n")

    with open(request_path, "r+") as request:
        data = request.read()
        print(data)
        client_ipheader = (data.split('\n', 1)[0]).split(' | ', -1)

    os.remove(request_path)

    if data:
        start = data.index("/")
        end = data.index(" HTTP/1.1")
        item = data[start+1:end]
        start = item.index(".") + 1
        filetype = item[start:]
        start = data.index("Host") + 6
        server = data[start:]
        start = data.index("\n")
        end = data.index("/")
        httpMethod = data[start:end-1]
    
    ip_condition = False

    if client_ipheader:
        source_ip = client_ipheader[0]
        dest_ip = client_ipheader[1]
        filetype = client_ipheader[2]
        packet_number = client_ipheader[3]
        number_of_packets = client_ipheader[4]

        if dest_ip == server_ip:
            if item in os.listdir(serverResource):
                ip_condition = True
    

    if ip_condition:
    
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
        content=""

        if httpMethod.strip()=="GET":
            temp = packetsplit(source)
            for i in range(len(temp)):
                packetdata = temp[i]
                packet_with_header = ipheader(server_ip, source_ip, item, str(i+1), len(temp))
                content += "\n\n" + packet_with_header + "\n\n" + response + "\n\n" + packetdata + "\n\n----------------------------"
            response = content
            log = response
        elif httpMethod.strip()=="HEAD":
            response = ipheader(server_ip, source_ip, item, 1, 1) + "\n\n" + response
            log = "\n\n" + response + "\n\n----------------------------"

        with open(log_path, "a") as pipe:
            pipe.write(log)
            print("\nResponse logged!")

        # Sending response
        with open(response_path, "w") as pipe:
            if httpMethod.strip()=="GET":
                shutil.copy(source,connection)
            pipe.write(response)
        print("Response sent!")