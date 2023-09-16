import socket
import os

# Nastavíme IP adresu a port servera
server_ip = 'IP_adresa_servera'  # Nahraďte skutočnou IP adresou servera
server_port = 8080  # Nahraďte skutočným portom servera

# Pripojíme sa na server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((server_ip, server_port))
    print("Pripojenie na server úspešné. Čakám na spustenie servera...")
except ConnectionRefusedError:
    print("Pripojenie na server neúspešné. Uistite sa, že server je spustený.")
    os._exit(1)

while True:
    # Získať príkaz od používateľa
    command = input("Zadajte príkaz: ")

    # Poslať príkaz na server
    s.send(command.encode())

    if command == "exit":
        break

    if command == "clear":
        os.system('clear')  # Linux príkaz na vymazanie obrazovky terminálu

    # Prijíma odpoveď od servera
    response = s.recv(1024).decode()
    print(response)

print("Disconnected.")

# Zatvoríme pripojenie
s.close()
