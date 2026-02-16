import socket
import os

# Set the server address and port
serverAddress = ('0.0.0.0', 5698)
# Create a TCP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the server socket to the address and port
serverSocket.bind(serverAddress)
# Listen for incoming connections
serverSocket.listen(10)

# Set the base directory where all the files are located
file_path_base = "C:/Users/USER/OneDrive/Desktop/Project1_T011/task2/task2/"

while True:
    print("The server is ready to receive")
    # Accept a new connection
    connection, clientAddress = serverSocket.accept()

    try:
        # Receive the request from the client
        data = connection.recv(1024).decode()
        print("IP: " + clientAddress[0] + ", Port: " + str(clientAddress[1]))
        print(data)  # Extract request details
        # Parse the request line
        request_line = data.splitlines()[0]
        # Get the requested URI
        requestUri = request_line.split()[1] if len(request_line.split()) > 1 else "/"

        # Handle specific request for processing material
        if requestUri.startswith('/process_request'):
            # Extract query parameters
            query_string = requestUri.split('?')[1] if '?' in requestUri else ""
            params = dict([param.split('=') for param in query_string.split('&')])
            file_name = params.get('fileName', '')

            # Check if the file exists locally
            file_path = os.path.join(file_path_base, file_name)
            if os.path.exists(file_path):
                # Serve the file if it exists locally
                content_type = "image/png" if file_name.endswith(".png") else "image/jpeg"
                with open(file_path, "rb") as f:
                    connection.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode() + f.read())
            else:
                # Check the file extension for redirection
                file_extension = file_name.split('.')[-1].lower()
                if file_extension in ['jpg', 'jpeg', 'png']:
                    # Redirect to Google Image search
                    redirect_url = f"https://www.google.com/search?q={file_name.replace(' ', '+')}&tbm=isch"
                    connection.sendall(f"HTTP/1.1 307 Temporary Redirect\r\nLocation: {redirect_url}\r\n\r\n".encode())
                elif file_extension in ['mp4', 'avi', 'mkv', 'mov']:
                    # Redirect to YouTube search
                    redirect_url = f"https://www.youtube.com/results?search_query={file_name.replace(' ', '+')}"
                    connection.sendall(f"HTTP/1.1 307 Temporary Redirect\r\nLocation: {redirect_url}\r\n\r\n".encode())
                else:
                    # If file type is not recognized
                    error_message = (
                        "<html><head><meta charset='UTF-8'><title>Unsupported file type</title></head>"
                        "<body><h1>Unsupported file type. Please enter a valid file name.</h1></body></html>"
                    )
                    connection.sendall(
                        b"HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n\r\n" + error_message.encode())
            continue

        # Determine the file path and content type based on the request URI
        file_path = ""
        content_type = "text/html"  # Default to HTML content type

        if requestUri in ['/ar', '/main_ar.html']:
            file_path = file_path_base + "main_ar.html"
        elif requestUri in ['/', '/en', '/index.html', '/main_en.html']:
            file_path = file_path_base + "main_en.html"
        elif requestUri == '/supporting_material_en.html':
            file_path = file_path_base + "supporting_material_en.html"
        elif requestUri == '/supporting_material_ar.html':
            file_path = file_path_base + "supporting_material_ar.html"
        elif requestUri.endswith(".css"):
            file_path = file_path_base + "style.css"
            content_type = "text/css"
        elif requestUri.endswith(".png") or requestUri.endswith(".jpg"):
            # Serve image files
            file_path = file_path_base + requestUri.strip("/")
            content_type = "image/png" if requestUri.endswith(".png") else "image/jpeg"

        # Check if the file exists and send it if found
        if file_path and os.path.exists(file_path):
            # Open and read the file in binary mode
            with open(file_path, "rb") as f:
                connection.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode() + f.read())
        else:
            # If the file is not found, send a 404 error page
            error_message = (
                f"<html><head><meta charset='UTF-8'><title>Error 404</title></head>"
                f"<body style='color: red;'><h1>The file is not found</h1>"
                f"<p>Client IP: {clientAddress[0]}</p>"
                f"<p>Client Port: {clientAddress[1]}</p>"
                f"</body></html>"
            )
            connection.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n" + error_message.encode())

    except Exception as e:
        # Print any errors for debugging
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        connection.close()
        print("Connection closed")
