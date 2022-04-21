# Points of reference: https://blogs.oracle.com/linux/post/learning-by-doing-writing-your-own-traceroute-in-8-easy-steps
# Author: Thomas Anderson

from sys import *
from socket import *

def trace(dest):
    #define protocols and general definitions
    proto_icmp = getprotobyname('icmp')
    proto_udp = getprotobyname('udp')
    port = 12050
    maxHops = 30
    time = 1

    # start the ttl trace
    for time_to_live in range(1, maxHops + 1):
        clientSocket = socket(AF_INET, SOCK_RAW, proto_icmp)
        clientSocket.settimeout(time)
        probeSocket = socket(AF_INET, SOCK_DGRAM, proto_udp)

        clientSocket.bind(('', port))
        probeSocket.setsockopt(SOL_IP, IP_TTL, time_to_live)
        probeSocket.sendto(''.encode(), (dAddr, port))

        try:
            data, cAddr = clientSocket.recvfrom(512) #checking for data being sent
            cAddr = cAddr[0]
        except error:
            cAddr = None #set cAddr to none if there is no response
        finally:
            clientSocket.close()
            probeSocket.close()

        yield cAddr

        if cAddr == dAddr: #dest reached if destination address and current address are the same
            print("\nDestination Reached")
            break

if __name__ == "__main__": # main loop
    dest = argv[1]
    dAddr = gethostbyname(dest)
    print("Performing traceroute to %s (%s)\n" % (dest, dAddr))
    print("# \t IP \t Resolved Name\n")
    for i, v in enumerate(trace(dAddr)):
        print("%d\t%s" % (i+1, v))
