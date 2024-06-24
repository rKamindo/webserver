import os
import socket
import threading
import argparse

'''
This is a basic multi-threaded HTTP web server. The default host and port the
server socket is bound to is localhost:80. You can set the
host and port to bind the server socket to using the following arguments:
--host, --port
You can specify the directory of the www folder, which is used to serve HTML documents
using the following argument:
--www
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

    # normalize the path and strip leading \
    requested_path = os.path.normpath(requested_path).lstrip("\\")
    file_path = os.path.join(BASE_DIR, requested_path)

    thread_id = threading.current_thread().ident
    print(f"Path: {requested_path}\nThread ID: {thread_id}")

    try:
      with open(file_path, encoding="utf-8") as f:
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
  parser = argparse.ArgumentParser(description="Basic multi-threaded HTTP web server")
  parser.add_argument("--www", default="www")
  parser.add_argument("--host", default="localhost", help="Host to bind to")
  parser.add_argument("--port", type=int, default=80, help="Port to bind to")
  args = parser.parse_args()

  if not os.path.isdir(args.www):
    print(f"Error: {args.www} is not a valid directory")
    exit(1)

  BASE_DIR = os.path.abspath(args.www)
  start_server(args.host, args.port)