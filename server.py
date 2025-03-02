import socket
import threading
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 9999

def handle_client(client_socket, client_address):
    """Handle client connections and echo back received data"""
    try:
        logging.info(f"Connection established with {client_address}")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            client_socket.sendall(data)
    except ConnectionResetError:
        logging.warning(f"Connection reset by {client_address}")
    except Exception as e:
        logging.error(f"Error with {client_address}: {str(e)}")
    finally:
        client_socket.close()
        logging.info(f"Connection closed with {client_address}")

def start_server():
    """Start the TCP echo server"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        logging.info(f"Server started on port {PORT}")

        try:
            while True:
                client_sock, addr = server_socket.accept()
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(client_sock, addr),
                    daemon=True
                )
                client_thread.start()
        except KeyboardInterrupt:
            logging.info("Server shutting down gracefully...")
        except Exception as e:
            logging.error(f"Server error: {str(e)}")

if __name__ == "__main__":
    start_server()
