import socket
import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def list_files(directory):
    files = os.listdir(directory)
    return "\n".join(files)

def change_directory(path):
    try:
        os.chdir(path)
        return f"Aktuálny adresár bol zmenený na: {os.getcwd()}"
    except Exception as e:
        return f"Chyba pri zmene adresára: {str(e)}"

def send_file(client_socket, file_name):
    try:
        with open(file_name, "rb") as file:
            file_data = file.read()
        client_socket.send(file_data)
    except FileNotFoundError:
        client_socket.send(b"FileNotFound")

server_ip = '192.168.0.174'
server_port = 8080 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((server_ip, server_port))
    print("Pripojenie na server úspešné. Čakám na spustenie servera...")
except ConnectionRefusedError:
    print("Pripojenie na server neúspešné. Uistite sa, že server je spustený.")
    os._exit(1)

while True:
    command = input("Zadajte príkaz: ")
    s.send(command.encode())

    if command == "exit":
        break

    if command == "clear":
        clear_screen()

    response = s.recv(1024).decode()
    print(response)

print("Disconnected.")
s.close()
