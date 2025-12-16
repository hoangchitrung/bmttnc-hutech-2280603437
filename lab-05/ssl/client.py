import socket
import ssl
import threading

# Server Info
server_address = ("localhost", 12345)


def receive_data(ssl_socket):
    try:
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            print("Nhận: ", data.decode("utf-8"))
    except:
        pass
    finally:
        ssl_socket.close()
        print("Kết nối đã đóng")


# Create socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.verify_mode = ssl.CERT_NONE  # change this according to your need
context.check_hostname = False

# Install SSL connection
ssl_socket = context.wrap_socket(client_socket, server_hostname="localhost")

ssl_socket.connect(server_address)

# Start a thread to receive data from server
received_thread = threading.Thread(target=receive_data, args=(ssl_socket,))
received_thread.start()

# send data to server
try:
    while True:
        message = input("Nhập tin nhắn: ")
        ssl_socket.send(message.encode("utf-8"))
except KeyboardInterrupt:
    pass
finally:
    ssl_socket.close()
