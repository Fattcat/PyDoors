import socket
import threading
import sys
import pyautogui
import time

def handle_client(client_socket, mouse_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break

        # Odešlete příkaz myši
        mouse_socket.send(data.encode())
        
        handle_commands(data)

        # Pošlete potvrzení klientovi
        client_socket.send("Command successfully executed.".encode())

    client_socket.close()

def handle_commands(data):
    try:
        action, *args = data.split(maxsplit=1)

        if action == "press":
            keys = args[0].split(',')
            for key in keys:
                pyautogui.keyDown(key)
            for key in keys:
                pyautogui.keyUp(key)
            print("Successfully sent command.")

        elif action == "write":
            pyautogui.write(args[0])
            print("Successfully wrote text.")

        elif action == "openWebSite":
            import webbrowser
            webbrowser.open(args[0])
            print("Successfully opened the website.")

        elif action == "moveMouse":
            x, y = map(int, args[0].split(','))
            move_mouse_handler(x, y)

        elif action == "Click":
            if args:
                button, *coords = args[0].split()
                if coords:
                    x, y = map(int, coords[0].split(','))
                    threading.Thread(target=click_handler, args=(button, x, y)).start()
                else:
                    threading.Thread(target=click_handler, args=(button,)).start()
            else:
                threading.Thread(target=click_handler).start()

        elif action == "RightClick":
            if args:
                *coords, = args[0].split()
                if coords:
                    x, y = map(int, coords[0].split(','))
                    threading.Thread(target=click_handler, args=('right', x, y)).start()
                else:
                    threading.Thread(target=click_handler, args=('right',)).start()

        else:
            print("Invalid command.")
    except Exception as e:
        print(f"Error processing command: {e}")

def move_mouse_handler(x, y):
    # Přesuňte kurzor myši na zadané souřadnice
    pyautogui.moveTo(x, y)
    print("Successfully moved mouse.")

def click_handler(button='left', x=None, y=None):
    if x is not None and y is not None:
        # Pokud jsou poskytnuty souřadnice, přesuňte kurzor a stiskněte myš
        pyautogui.moveTo(x, y)
        time.sleep(0.01)
    pyautogui.click(button=button)
    print(f"Successfully {button}-clicked.")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Zadejte adresu a port servera
    server_address = ('IPAdress', 12345)

    # Další socket pro komunikaci s druhým počítačem
    mouse_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mouse_address = ('IPAdress', 12346)
    mouse_socket.bind(mouse_address)
    mouse_socket.listen(1)

    try:
        server_socket.bind(server_address)
        server_socket.listen(5)
        print("Server is listening for connections.")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            client_handler = threading.Thread(target=handle_client, args=(client_socket, mouse_socket))
            client_handler.start()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server_socket.close()
        sys.exit()

if __name__ == "__main__":
    main()
