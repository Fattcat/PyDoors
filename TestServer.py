import socket
import os
import shutil

def start_server():
    host = '127.0.0.1'  # Zmeniť podľa potreby
    port = 12345         # Zmeniť podľa potreby

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server čaká na pripojenie na {host}:{port}")

    client_socket, client_address = server_socket.accept()
    print(f"Pripojené od {client_address}")

    command = client_socket.recv(1024).decode('utf-8')
    
    if command.startswith("Search"):
        _, filename = command.split(" ", 1)
        result = search_file(filename)
        client_socket.send(result.encode('utf-8'))
    elif command.startswith("Download"):
        _, path = command.split(" ", 1)
        result = download_files(path)
        client_socket.send(result.encode('utf-8'))
    elif command.startswith("Upload"):
        _, filename = command.split(" ", 1)
        result = upload_file(filename)
        client_socket.send(result.encode('utf-8'))
    elif command.startswith("List"):
        result = list_files()
        client_socket.send(result.encode('utf-8'))
    else:
        client_socket.send("Invalid command".encode('utf-8'))

    client_socket.close()
    server_socket.close()

def search_file(filename):
    for root, dirs, files in os.walk('/'):  # Zmeniť podľa potreby
        if filename in files:
            file_path = os.path.join(root, filename)
            return f"File named: {filename} saved in path: {file_path}"
    return f"File {filename} not found!"

def download_files(path):
    path = path.strip()
    if os.path.isfile(path):
        shutil.copy(path, os.path.join(os.path.dirname(__file__), os.path.basename(path)))
        return f"File downloaded: {os.path.basename(path)}"
    elif os.path.isdir(path):
        files = os.listdir(path)
        for file in files:
            shutil.copy(os.path.join(path, file), os.path.join(os.path.dirname(__file__), file))
        return f"All files in directory downloaded: {os.path.basename(path)}"
    else:
        return f"File or directory not found: {path}"

def upload_file(filename):
    try:
        shutil.copy(os.path.join(os.path.dirname(__file__), filename), "C:/User/Files/")
        return f"File uploaded to C:/User/Files/: {filename}"
    except FileNotFoundError:
        return f"File not found: {filename}"

def list_files():
    current_path = os.getcwd()
    files = os.listdir(current_path)
    files_list = "\n".join(files)
    return f"Actual Path: {current_path}\nSaved files: {files_list}"

if __name__ == "__main__":
    start_server()
