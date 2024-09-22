from socket import *
import time
import os

# Global variables
proxy_host='localhost'
proxy_port=8888
CACHE_DIR = 'PROXY_CACHE' # Directory for cache files
BUFFER_SIZE = 4096    # Receive buffer

# Create the cache directory if it doesn't already exist
os.makedirs(CACHE_DIR, exist_ok=True)

def start_proxy_server(host, port):
    # Create a server socket
    servSock = socket(AF_INET, SOCK_STREAM)
    # TODO: Start - Bind the socket to a port and begin listening
    servSock.bind((host, port))
    servSock.listen()
    # TODO: End

    print('Proxy server running...')

    while True:
        cliSock, addr = servSock.accept()
        print('Accepted a connection from:', addr)
        handle_client(cliSock)


def handle_client(cliSock: socket):
    # TODO: Start - Receive the request
    request = cliSock.recv(BUFFER_SIZE).decode()
    # TODO: End

    if not request:
        cliSock.close()
        return

    #Get the request url
    url = request.split()[1]

    # Remove unnecessary characters from url
    while url.startswith('/') or url.startswith(':'):
        url = url[1:]

    # Assign file path in cache
    cacheFilePath = os.path.join(CACHE_DIR, url.replace('/','_').replace(':','_'))


    try:
        # TODO: Start - Create socket to fetch content from web
        webSock = socket(AF_INET, SOCK_STREAM)
        # TODO: End

        # TODO: Start - From the url, get the host name and path
        # e.g the hostname is gaia.cs.umass.edu,
        # the path is /wireshark-labs/HTTP-wireshark-file1.html
        print(url)
        partitioned_url = url.partition("/")
        webHostn = partitioned_url[0]
        webPath = partitioned_url[1] + partitioned_url[2]
        print(webHostn)
        print(webPath)
        # TODO: End

        # Replace empty path with '/' character
        if webPath == '':
            webPath = '/'

        # TODO: Start - Establish connection with web server
        webSock.connect((webHostn, 80))  # Connect to webHost on port 80
        # TODO: End

        # Check whether the file exists in the cache
        if os.path.exists(cacheFilePath):
            print(f"File found in cache: {url}")
            # TODO: Start - Get the last modification time of the file and
            # construct if-modified-since header to request
            # (Hint: you may need to import another module to help with this)
            lastModified = os.path.getmtime(cacheFilePath)
            ifModSince = time.strftime("If-Modified-Since: %a, %d %b %Y %H:%M:%S GMT\r\n\r\n", time.gmtime(lastModified))
            #TODO: End
        else:
            ifModSince="\r\n"

        # Build a simple GET request
        webRequest = "GET " + webPath + " HTTP/1.1\r\nHost: " + webHostn +"\r\n" + ifModSince

        # TODO: Start - Send the request to the web server
        webSock.sendall(webRequest.encode())
        # TODO: End

        # TODO: Start - Receive response from the web server
        response = webSock.recv(BUFFER_SIZE)
        # TODO: End

        # TODO: Check for 304 Not Modified status code
        if response.decode().startswith("HTTP/1.1 304 Not Modified"):
        #TODO: End

            print(f"Not Modified, sending file from cache: {url}")
            # TODO: Start - Read data from the cache and send to client
            with open(cacheFilePath, 'rb') as cache_file:
                cliSock.sendfile(cache_file)
            # TODO: End

        else:
            # Cache the response
            with open(cacheFilePath, 'wb') as cache_file:
                cache_file.write(response)

            # TODO: Start - Forward response to the client
            cliSock.sendall(response)
            # TODO: End

    # Handle errors
    except Exception as e:
        # TODO: Start - Print an error message and send HTTP error code to the client
        print(f"Error when attempting to retrieve: {url}")
        response = b"HTTP/1.1 404 Not Found\r\n"
        cliSock.sendall(response)
        # TODO: End

    # TODO: Start - Close the client socket
    cliSock.close()
    # TODO: End

    return

if __name__ == "__main__":
    start_proxy_server(proxy_host, proxy_port)

