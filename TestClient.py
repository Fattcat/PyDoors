import socket
import sys
import threading

def receive_data(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print(data)

def send_data(client_socket):
    while True:
        message = input("Enter a command: ")
        client_socket.send(message.encode())
        if message.lower() == "exit":
            break
        response = client_socket.recv(1024).decode()
        print(response)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Zadejte adresu a port servera
    server_address = ('IPAdress', 12345)

    try:
        client_socket.connect(server_address)
        print("Connected to the server.")

        receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
        send_thread = threading.Thread(target=send_data, args=(client_socket,))

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()
        sys.exit()

if __name__ == "__main__":
    main()
