import socket
import os

def get_system_info():
    system_info = f"Connected to PC: {os.uname().nodename}\nPublic IP: {get('https://api64.ipify.org').text}"
    return system_info

def connect_to_server():
    host = '127.0.0.1'  # Zmeniť podľa potreby
    port = 12345         # Zmeniť podľa potreby

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    system_info = get_system_info()
    client_socket.send(system_info.encode('utf-8'))

    command = input("Enter command: ")
    client_socket.send(command.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    print(response)

    client_socket.close()

if __name__ == "__main__":
    connect_to_server()
