import socket

# Nastavíme IP adresu a port servera
server_ip = '192.168.0.174'  # Nahraďte skutočnou IP adresou servera
server_port = 8080  # Nahraďte skutočným portom servera

# Pripojíme sa na server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_ip, server_port))

while True:
    # Získať príkaz od používateľa
    command = input("Zadajte príkaz: ")

    # Poslať príkaz na server
    s.send(command.encode())

    if command == "exit":
        break

    # Prijíma odpoveď od servera
    response = s.recv(1024).decode()
    print(response)

# Zatvoríme pripojenie
s.close()
