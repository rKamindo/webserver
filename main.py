import socket
'''
create a basic HTTP server that listens on port 80
and can handle a single TCP connection at a time. 
For all requests we’ll return some text that describes 
the requested path.
'''

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
# bind the socket to the address of our server and the HTTP port
serversocket.bind(("localhost", 80))
# become a server socket
serversocket.listen(5)

while True:
  # accept connections from outside
  (clientsocket, address) = serversocket.accept()
  print("New connection from", clientsocket, address)

  # request processing
  request = clientsocket.recv(1024).decode()
  request_lines = request.split("\r\n")
  header_list = request_lines[0].split()
  requested_path = header_list[1]
  
  if requested_path == "/":
    requested_path = "index.html"

  with open(f"www/{requested_path}", encoding="utf-8") as f:
    response_body = f.read()

    # send a response to client
    response_headers = "HTTP/1.1 200 OK\r\n\r\n"
    response_message = response_headers + response_body
    clientsocket.sendall(response_message.encode())
    clientsocket.close()
    print("Sent a response!")
  
