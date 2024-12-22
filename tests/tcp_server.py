import socket
'''
tcp_server.py
创建一个简单的 TCP 服务器，监听 127.0.0.1 的 9999 端口，客户端发来什么就回复什么。
'''
def start_server(host='127.0.0.1', port=9999):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Connected by {client_address}")
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    print(f"Received: {data}")
                    client_socket.sendall(data)
                    print(f"Sent: {data}")

if __name__ == "__main__":
    start_server()
