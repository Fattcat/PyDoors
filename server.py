import socket
import os

# Nastavíme IP adresu a port servera
server_ip = '0.0.0.0'  # '0.0.0.0' znamená, že prijímame pripojenia na všetkých rozhraniach
server_port = 8080  # Nahraďte skutočným portom servera

# Spustíme server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server_ip, server_port))
s.listen(5)
print(f"Server čaká na pripojenie na adrese {server_ip}:{server_port}")

# Funkcia na získanie zoznamu súborov v aktuálnom adresári
def list_files(directory):
    files = os.listdir(directory)
    return "\n".join(files)

# Funkcia na zmenu adresára
def change_directory(path):
    try:
        os.chdir(path)
        return f"Aktuálny adresár bol zmenený na: {os.getcwd()}"
    except Exception as e:
        return f"Chyba pri zmene adresára: {str(e)}"

# Priekžem pripojenie od klienta
client_socket, addr = s.accept()
print(f"Pripojenie od {addr} úspešné. Čakám na príkazy od klienta...")

while True:
    # Prijímame príkaz od klienta
    command = client_socket.recv(1024).decode()

    if not command:
        break

    if command == "exit":
        break
    elif command == "show_files":
        files = list_files(os.getcwd())
        client_socket.send(files.encode())
    elif command.startswith("change_dir "):
        new_dir = command.split(" ")[1]
        response = change_directory(new_dir)
        client_socket.send(response.encode())
    elif command.startswith("download "):
        file_name = command.split(" ")[1]

        try:
            with open(file_name, "rb") as file:
                file_data = file.read()
            client_socket.send(file_data)
        except FileNotFoundError:
            client_socket.send(b"FileNotFound")

    if command == "clear":
        os.system('clear')  # Linux príkaz na vymazanie obrazovky terminálu

print("Disconnected.")

# Zatvoríme pripojenie
client_socket.close()
s.close()
