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
    # Bind socket to chosen port and listen for connections
    servSock.bind((host, port))
    servSock.listen()

    print('Proxy server running...')

    while True:
        cliSock, addr = servSock.accept()
        print('Accepted a connection from:', addr)
        handle_client(cliSock)


def handle_client(cliSock: socket):
    # Receive the web request from the client
    request = cliSock.recv(BUFFER_SIZE)

    if not request:
        cliSock.close()
        return
    
    # Decode Request bytes to string
    request = request.decode()

    #Get the request url
    url = request.split()[1]

    # Remove unnecessary characters from url
    while url.startswith('/') or url.startswith(':'):
        url = url[1:]
    
    # Remove the http:// prefix if it is present
    url = url.removeprefix("http://")

    # Assign file path in cache
    cacheFilePath = os.path.join(CACHE_DIR, url.replace('/','_').replace(':','_'))


    try:
        # Create a socket for the target web server
        webSock = socket(AF_INET, SOCK_STREAM)

        # From the url, get the host name and path
        # e.g the hostname is gaia.cs.umass.edu,
        # the path is /wireshark-labs/HTTP-wireshark-file1.html

        partitioned_url = url.partition("/")
        webHostn = partitioned_url[0]
        webPath = partitioned_url[1] + partitioned_url[2]
        print(webHostn)
        print(webPath)

        # Replace empty path with '/' character
        if webPath == '':
            webPath = '/'

        # Establish connection with web server. Use port 80 for HTTP
        webSock.connect((webHostn, 80))  # Connect to webHost on port 80

        # Check whether the file exists in the cache
        if os.path.exists(cacheFilePath):
            print(f"File found in cache: {url}")
            # Get the last modification time of the file and
            # construct if-modified-since header to request from the web server
            lastModified = os.path.getmtime(cacheFilePath)
            ifModSince = time.strftime("If-Modified-Since: %a, %d %b %Y %H:%M:%S GMT\r\n\r\n", time.gmtime(lastModified))
        else:
            ifModSince="\r\n"

        # Build a simple GET request
        webRequest = "GET " + webPath + " HTTP/1.1\r\nHost: " + webHostn +"\r\n" + ifModSince

        # Send the request to the web server. Includes the if-modified-since header
        webSock.sendall(webRequest.encode())

        # Receive response from the web server.
        # Should be done in a loop to ensure a response over BUFFER_SIZE is captured
        firstData = True    # This is so the cache is only checked on the first response. Prevents rare edge cases
        while True:
            response = webSock.recv(BUFFER_SIZE)
            # If no more data, break 
            if not response:
                break

            # Check for 304 Not Modified status code
            if firstData and response.startswith(b"HTTP/1.1 304 Not Modified"):
                print(f"Not Modified, sending file from cache: {url}")
                # Read data from the cache and send to client
                with open(cacheFilePath, 'rb') as cache_file:
                    cliSock.sendfile(cache_file)
            else:
                # Cache the response. Append as there may be more data coming for long files etc.
                with open(cacheFilePath, 'ab') as cache_file:
                    cache_file.write(response)

                # Forward response to the client
                cliSock.sendall(response)
            firstData = False

    # Handle errors
    except Exception as e:
        # Print Error Message and send 404 Not Found back to the client
        print(f"Error {e} when attempting to retrieve: {url}")
        response = b"HTTP/1.1 404 Not Found\r\n"
        cliSock.sendall(response)

    # Close the client socket
    cliSock.close()

if __name__ == "__main__":
    start_proxy_server(proxy_host, proxy_port)

