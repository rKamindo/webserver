import socket
from time import sleep
import threading
'''
create a basic HTTP server that listens on port 80
and can handle a single TCP connection at a time. 
For all requests we’ll return some text that describes 
the requested path.
'''

def start_server(host, port):
  # create an INET, STREAMing socket
  serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
  # bind the socket to the address of our server and the HTTP port
  serversocket.bind((host, port))
  # become a server socket
  serversocket.listen(100)

  print(f"Server listening on {host}:{port}")

  while True:
    # accept connections from outside
    (clientsocket, address) = serversocket.accept()
    # start a new thread to hande the client
    client_thread = threading.Thread(target=handle_client, args=(clientsocket,))
    client_thread.start()

def handle_client(clientsocket):
  try:
    # request processing
    request = clientsocket.recv(1024).decode()
    request_lines = request.split("\r\n")
    header_list = request_lines[0].split()
    requested_path = header_list[1]
    if requested_path == "/":
      requested_path = "index.html"
    
    thread_id = threading.current_thread().ident
    print(f"Path: {requested_path}, THread ID: {thread_id}")

    try:
      with open(f"www/{requested_path}", encoding="utf-8") as f:
        response_body = f.read()

      # send a response to client
      response_headers = "HTTP/1.1 200 OK\r\n\r\n"
      response_message = response_headers + response_body
    except FileNotFoundError:
      response_body = "404 Not Found"
      response_headers = "HTTP/1.1 404 Not Found\r\n\r\n"
      response_message = response_headers + response_body

    clientsocket.sendall(response_message.encode())
  except Exception as e:
    print(f"Error processing request: {e}")
  finally:
    clientsocket.close()
  
if __name__ == "__main__":
  HOST = "localhost"
  PORT = 80
  start_server(HOST, PORT)