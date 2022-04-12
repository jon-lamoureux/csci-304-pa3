from socket import *
import random
import time
serverPort = 12050
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ("The server is ready to receive")
while 1:
    oddsOfIgnoring = random.randint(1, 10)
    message, clientAddress = serverSocket.recvfrom(2048)
    # give the server a 1 in 10 chance of not responding
    if oddsOfIgnoring <= 9:
        modifiedMessage = message.decode()
        number = random.randint(15, 25) / 1000
        time.sleep(number)
        print("Slept for %dms, replying now..." % (number * 1000))
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)
    else:
        print("Ignore the client")
