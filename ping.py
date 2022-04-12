import time
from socket import *
import time
# Set up server variables
serverName = '127.0.0.1'
serverPort = 12050
clientSocket = socket(AF_INET, SOCK_DGRAM)
timeout = 1000  # in ms
number_of_pings = 4
packets_received = 0
packets_lost = 0
message = "This string is actually 32 bytes"
numBytes = len(message)
response_times = []
# Send packet to server
print("Pinging %s with %d bytes of data:" % (serverName, numBytes))
for i in range(number_of_pings):
    start = time.perf_counter()
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    clientSocket.settimeout(timeout / 1000)
    try:
        servResponse, serverAddress = clientSocket.recvfrom(2048)
        end = time.perf_counter()-start
        print("Reply from %s: bytes=%d time=%dms TTL=%d" % (serverName, numBytes, int(round(end * 1000)), 56))
        packets_received += 1;
        response_times.append(int(round(end * 1000)))
    except:
        print("Request timed out")
        packets_lost += 1;
print("Ping statistics for %s:" % serverName)
print("\tPackets: Sent = %d, Received = %d, Lost = %d (%d%s loss)," % (number_of_pings, packets_received, packets_lost, (packets_lost / number_of_pings) * 100, "%"))
print("Approximate round trip time in milli-seconds:")
print("\tMinimum = %dms, Maximum %dms, Average %dms" % (max(response_times), min(response_times), sum(response_times) / len(response_times)))
clientSocket.close()