import os
import time
import math
import base64

seq_m = "m"
seq_n = "n"
connection = "pipe"

def clientHandshake():
    if sendSYN(seq_m):
        receiveACK(seq_m)
    if receiveSYN(seq_n):
        sendACK(seq_n)
    while (not os.path.isdir(connection)):
        pass
    print("\nConnection is established!")
    return True

def serverHandshake():
    if receiveSYN(seq_m):
        sendACK(seq_m)
    if sendSYN(seq_n):
        if receiveACK(seq_n):
            os.mkdir(connection)
            print("\nConnection is established!")
            return True

def sendSYN(seq):
    with open("syn_{}.txt".format(seq), "w"):
        pass
    print("SYN sent!")
    return True

def receiveSYN(seq):
    syn = "syn_{}.txt".format(seq)
    while (not os.path.isfile(syn)) :
        pass
    print("SYN received!")
    with open(syn,"r+"):
        pass
    os.remove(syn)
    return True

def sendACK(seq):
    with open("ack_{}.txt".format(seq), "w"):
        pass
    print("ACK sent!")
    return True

def receiveACK(seq):
    ack = "ack_{}.txt".format(seq)
    while (not os.path.isfile(ack)) :
        pass
    print("ACK received!")
    with open(ack,"r+"):
        pass
    time.sleep(2)
    os.remove(ack)
    return True

def waitingMessage(path):
    while (not os.path.isfile(path)) :
        pass
    return True

#DNS lookup

def DNS_lookup(domain):
    source_ip = ip_table.get(domain)
    return source_ip

ip_table = {"www.gollum.mordor": "192.168.1.1",
        "rincewind.fourex.disc.atuin": "192.168.1.1"}

# Generates ip header

def ipheader(source_ip, dest_ip, item, packet_number, numberofpackets):
    return "{} | {} | {} | {} | {}".format(source_ip, dest_ip, item.split('.')[1], packet_number, numberofpackets)

# Splits images into packets, returns list of packets

def packetsplit(filepath):
    data = []
    with open(filepath,"rb") as f:
        while True:
            temp = base64.b64encode(f.read(1024)).decode('utf-8')
            if temp == '':
                break
            data.append(temp)
    return data

#decode data
#192.168.1.1 | 192.168.1.0 | jpg | 1 | 319

#HTTP/1.1 200 OK
#Date: Wed, 24 Jan 2024 23:20:30 GMT
#Server: www.gollum.mordor
#Last-Modified: Wed Jan 24 18:39:16 2024
#Accept-Ranges: bytes
#Content-Length: 326266
#Connection: open
#Content-Type: jpg

#/9j/2wBDAAIBAQEBAQIBAQECAgICAgQDAgICAgUEBAMEBgUGBgYFBgYGBwkIBgcJBwYGCAsICQoKCgoKBggLDAsKDAkKCgr/2wBDAQICAgICAgUDAwUKBwYHCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgr/wAARCAZABVcDASIAAhEBAxEB/8QAHgABAAAGAwEAAAAAAAAAAAAAAAEDBgcICQIEBQr/xAB+EAABAwMCAwUDBgYJCw0JAh8BAAIDBAURBgcIEiEJEzFBUSJhcQoUMoGRoRUjQlKxwRYaM2JocqfR5RcZJEOCkpOis9LhGCU0ODlTc3R1g5SywjU3RFRXY2R20/AmNkVGVVa0tfEnR2Vmd4SWo8MohYaVtuIpWHilpuPk1P/EABwBAQABBQEBAAAAAAAAAAAAAAABAgMEBQYHCP/EAEMRAAIBAwEHAQUECQMEAgIDAQABAgMEEQUGEhMhMUFRYRQicYGRBzKhsRUjJTM0QlLB0TVi4SRDcvAWU4LxFyaSNv/aAAwDAQACEQMRAD8A20IiLILYREQBERAEREAREQBERAEREAREQBERAEREAXV09S090vlfdq2MPFBIIKcO6hp5Gucfj7WF2l5kNHqW1tq4LTWUToqud8rvnEL+dpcAD1DseAHkgO3FrK611O6ej06Xwv5hE/5y0EjJGcYXCxW+S12mCimcC9jPbI8C49SuVto/wVa4qMvDu5jwXY8V5bv2QSaXn1cy/NY1jXvZTGkBBAOAM5HigPdRcKZ75KeOSXHM5gLseuFzQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQFpN0Kn5xrOqAPSMMZ9jQu/slQxVepK2slja75nSx8hI+i6Rzuv2MP2rwNW1PzvU1dUZzzVDvuOF1LfcrnaHzSWq5T0xqA0TdxKW84bnGcemT9qA97Ue4WrpL5VCiv0sMLZ3NijiazAaDjzbnyVNPlYw5lkAJ83HxXJofK4hvM92evmcqtq22C1bF1Tquha2omiIb3kWHjvJA0ePUdCp6gohXd2ypvm2i6TI6v53n63FWiV7dLU3zTTtHT4xy07f51AO+iIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCIiAIiIAiIgCKTS3GhrnyR0dWyR0TuWQMdnlPoVOQBSK+52+2RiWvq2RA+HO7x+HquFfVVnfwWq0QCauq38tPGT0Hq4+gHmvaZadF7ZU8dy1PMbhdJ88rjHzyPPm2Nn5LR/wDPKhvBKR4LdRWvAdLJJE1x9l80DmNP1kYXvw=='
def data_decode(data):
    encodeddata = data.split('\n')[11]
    decodeddata = encodeddata.encode('utf-8')
    print (decodeddata)
    return decodeddata