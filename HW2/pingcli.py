"""
Fall 2023 10/10/2023
CSC138 Computer Network Fundamentals - Homework 2
303833894 Yunjeong Lee

pingcli.py

This script sends 10 PING messages to a specified server and calculates the loss rate, minimum, maximum, and average RTT of the responses.
The script takes two command-line arguments: the hostname and the port number of the server.
"""

import sys
import time
from socket import *

# Check if the correct number of command-line arguments are provided
if len(sys.argv) != 3:
    print("Usage: python3 pingcli.py <hostname> <port>")
    sys.exit(2)

# Get the server name and port number from the command-line arguments
serverName = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a UDP socket for the client
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Initialize variables to keep track of the number of sent and received messages, and the minimum, maximum, and sum of RTT
sendCnt = 0
receivedCnt = 0
minRTT = float('inf')
maxRTT = 0
sumRTT = 0

# Send 10 PING messages to the server
for i in range(1, 11, 1):
    message = "PING"
    startTime = time.time()
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    sendCnt += 1
    clientSocket.settimeout(1)
    try:
        # Receive the response from the server and calculate the RTT
        reply, serverAddress = clientSocket.recvfrom(2048)
        rtt = (time.time() - startTime)*1000
        if rtt < minRTT:
            minRTT = rtt
        if rtt > maxRTT:
            maxRTT = rtt
        sumRTT += rtt
        print(f"Received {reply.decode()} from {serverAddress} (RTT: {rtt:.2f}ms)")
        receivedCnt += 1
    except timeout:
        # Handle the case where the response times out
        print(f"Request timed out for sequence {i}")

# Close the socket
clientSocket.close()

# Print the statistics of the PING messages sent and received
print("Ping statistics:")
print(f"Sent = {sendCnt}, Received = {receivedCnt}, Loss rate = {(sendCnt - receivedCnt) / sendCnt * 100}%")
if receivedCnt > 0:
    print(f"Minimum RTT = {minRTT:.2f}ms, Maximum RTT = {maxRTT:.2f}ms, Average RTT = {sumRTT / receivedCnt:.2f}ms")