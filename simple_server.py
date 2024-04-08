from http.server import HTTPServer, SimpleHTTPRequestHandler

# Define the IP address and port number to listen on
host = '127.0.0.1'
port = 8000

# Create a simple HTTP server with the defined host and port
server_address = (host, port)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

# Print a message indicating that the server is running
print(f"Server running at http://{host}:{port}")

# Start the server
httpd.serve_forever()
