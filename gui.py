# Author: Jonathan Lamoureux
from socket import *
import time
import sys
import tkinter as tk
from tkinter import ttk

# root window
root = tk.Tk()
root.geometry('600x360')
root.title('Network Analysis Tools')

# create a notebook
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# create frames
frame1 = ttk.Frame(notebook, width=600, height=380)
frame2 = ttk.Frame(notebook, width=600, height=380)

frame1.pack(fill='both', expand=True)
frame2.pack(fill='both', expand=True)

# add frames to notebook
notebook.add(frame1, text='Ping')
notebook.add(frame2, text='Traceroute')

text_input = tk.Text(frame1, height=15, width=100)
text_input.pack()

trace_input = tk.Text(frame2, height=15, width=100)
trace_input.pack()
trace_input.place(x=0, y=0)

def simulatePing(serverName, serverPort, timeout, numPings):
    # Create varaible for ping functionality
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    packets_received = 0
    packets_lost = 0
    message = "This string is actually 32 bytes"
    numBytes = len(message)
    response_times = []

    # Send packet to server
    text_input.delete("1.0", "end")
    text_input.insert('1.0', "Pinging %s with %d bytes of data:\n" % (serverName, numBytes))
    for i in range(numPings):
        start = time.perf_counter()
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        clientSocket.settimeout(timeout / 1000)
        try:
            servResponse, serverAddress = clientSocket.recvfrom(2048)
            end = time.perf_counter() - start
            text_input.insert('%d.0' % (i + 2), "Reply from %s: bytes=%d time=%dms TTL=%d\n" % (serverName, numBytes, int(round(end * 1000)), 56))
            packets_received += 1;
            response_times.append(int(round(end * 1000)))
        except:
            text_input.insert('%d.0' % (i + 2), "Request timed out\n")
            packets_lost += 1;
    text_input.insert('%d.0' % int(numPings + 3), "Ping statistics for %s:\n" % serverName)
    text_input.insert('%d.0' % int(numPings + 4), "\tPackets: Sent = %d, Received = %d, Lost = %d (%d%s loss),\n" % (numPings, packets_received, packets_lost, (packets_lost / numPings) * 100, "%"))
    text_input.insert('%d.0' % int(numPings + 5), "Approximate round trip time in milli-seconds:\n")
    text_input.insert('%d.0' % int(numPings + 6), "\tMinimum = %dms, Maximum %dms, Average %dms\n" % (max(response_times), min(response_times), sum(response_times) / len(response_times)))
    clientSocket.close()
def simulateTrace():
    print("test")
    return 1;
entry1 = tk.Entry(frame1, width=15)
entry1.insert(0, "127.0.0.1")
label1 = tk.Label(frame1, text="IP Address")
entry2 = tk.Entry(frame1, width=15)
label2 = tk.Label(frame1, text="Port")
entry2.insert(0, "12050")
entry3 = tk.Entry(frame1, width=15)
label3 = tk.Label(frame1, text="Timeout (ms)")
entry3.insert(0, "1000")
entry4 = tk.Entry(frame1,  width=15)
label4 = tk.Label(frame1, text="Ping Count")
entry4.insert(0, "5")
entry1.pack()
label1.pack()
entry1.place(x=20, y=275)
label1.place(x=20, y=250)
entry2.pack()
entry2.place(x=120, y=275)
label2.place(x=120, y=250)
entry3.pack()
entry3.place(x=220, y=275)
label3.place(x=220, y=250)
entry4.pack()
entry4.place(x=320, y=275)
label4.place(x=320, y=250)
button = tk.Button(frame1, text="Ping", command=lambda: simulatePing(entry1.get(), int(entry2.get()),  int(entry3.get()), int(entry4.get())), width=10, height=1)
button.place(x=480,y=260)
button2 = tk.Button(frame2, text="Trace Route", command=lambda: simulateTrace(), width=10, height=1)
button2.place(x=480,y=260)
root.mainloop()