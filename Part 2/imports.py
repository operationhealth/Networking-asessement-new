import os

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
    os.remove(ack)
    return True

def waitingMessage(path):
    while (not os.path.isfile(path)) :
        pass
    return True