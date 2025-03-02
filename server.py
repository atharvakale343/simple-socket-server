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
# Create a file handler that logs INFO and above messages to "server.log"
file_handler = logging.FileHandler("server.log")
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter(
    "%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logging.getLogger().addHandler(file_handler)

# Global connection counter and a lock for thread safety
connection_id_counter = 0
connection_id_lock = threading.Lock()

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 9999

def handle_client(client_socket, client_address, conn_id):
    """Handle client connections and echo back received data"""
    try:
        logging.info(f"Connection {conn_id} established with {client_address}")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            response = f"[Conn {conn_id}] {message}"
            client_socket.sendall(response.encode('utf-8'))
    except ConnectionResetError:
        logging.warning(f"Connection reset by {client_address}")
    except Exception as e:
        logging.error(f"Error with {client_address}: {str(e)}")
    finally:
        client_socket.close()
        logging.info(f"Connection {conn_id} closed with {client_address}")

def start_server():
    """Start the TCP echo server"""
    global connection_id_counter
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        logging.info(f"Server started on port {PORT}")

        try:
            while True:
                client_sock, addr = server_socket.accept()
                with connection_id_lock:
                    connection_id_counter += 1
                    conn_id = connection_id_counter
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(client_sock, addr, conn_id),
                    daemon=True
                )
                client_thread.start()
        except KeyboardInterrupt:
            logging.info("Server shutting down gracefully...")
        except Exception as e:
            logging.error(f"Server error: {str(e)}")

if __name__ == "__main__":
    start_server()
