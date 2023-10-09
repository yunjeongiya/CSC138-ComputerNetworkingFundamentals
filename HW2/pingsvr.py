"""
Fall 2023 10/10/2023
CSC138 Computer Network Fundamentals - Homework 2
303833894 Yunjeong Lee

pingsvr.py

This script receives PING messages from a client and sends back PONG as a response.
The script takes one command-line argument: the port number of the server.
"""

import sys
from socket import *

# Check if the correct number of command-line arguments are provided
if len(sys.argv) != 2:
    print("Usage: python3 pingsvr.py <port>")
    sys.exit(2)

# Get the server port number from the command-line argument
serverPort = int(sys.argv[1])

# Create a UDP socket and bind it to the server port
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

# Print a message to indicate that the server is listening on the specified port
print("UDP Ping Server is listening on port", serverPort)

try:
    # Loop indefinitely to receive and respond to PING messages
    while True:
        # Receive a PING message and the client address
        message, clientAddress = serverSocket.recvfrom(2048)
        
        # Check if the message is empty
        if not message:
            print(f"Packet from {clientAddress} was lost.")
        else:
            # Print the received message and client address
            print(f"Received {message.decode()} from {clientAddress}")
            
            # Send a PONG message back to the client
            reply = "PONG"
            serverSocket.sendto(reply.encode(), clientAddress)
            
            # Print the sent message and client address
            print(f"Sent {reply} to {clientAddress}")

# Handle keyboard interrupt (Ctrl+C) to gracefully close the socket
except KeyboardInterrupt:
    serverSocket.close()
    sys.exit(0)
