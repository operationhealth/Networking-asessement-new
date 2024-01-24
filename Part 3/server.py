import os
import shutil
import datetime
import time
from imports import serverHandshake, packetsplit

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
        ipheader = (data.split('\n', 1)[0]).split(' | ', -1)
    os.remove(request_path)
    
    if ipheader:
        print("parsing ip header...")
        source_ip = ipheader[0]
        dest_ip = ipheader[1]
        filetype = ipheader[2]
        packet_number = ipheader[3]
        number_of_packets = ipheader[4]
        if dest_ip == server_ip:

            if filetype in ("serverResources/ring.txt") or ("serverResources/wizzard.jpg"):
                print("Successfully parsed ip header")

                if data:
        
                    print ("parsing data")
                    start = data.index("/")
                    httpMethod = data[:start-1]
                    end = data.index(" HTTP/1.1")
                    item = data[start+1:end]
                    start = item.index(".") + 1
                    filetype = item[start:]
                    start = data.index("Host") + 6
                    server = data[start:]
            else:
                print("resourcetype not found")
        else:
            print("ip doesn't match server")
            


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
        print("get detected")
        if (filetype=="txt" or filetype=="html"):
            ("txt split")
            with open(source,"r") as f:
                content = f.read()
        else:
            print("splitting image")
            packets = packetsplit(source, 1024)
            number_of_packets_to_send = packets[0]
            content = []
            for i in range(len(packets)):
                packetdata = packets[i]
                packet_with_header = ipheader(server_ip, source_ip, "jpg", str(i), number_of_packets[0]) + packetdata
                content.append(packet_with_header)


        response = response + "\n\n" + content


    log = "\n\n" + response + "\n\n----------------------------"

    with open(log_path, "a") as pipe:
        pipe.write(log)
        print("\nResponse logged!")

    # Sending response
    if httpMethod == "GET":
        with open(response_path, "w") as pipe:
            shutil.copy(source,connection)
            pipe.write(response)
    print("Response sent!")

