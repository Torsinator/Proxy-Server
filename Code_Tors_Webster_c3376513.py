from socket import *
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

    # TODO: End

    print('Proxy server running...')

    while True:
        cliSock, addr = servSock.accept()
        print('Accepted a connection from:', addr)
        handle_client(cliSock)


def handle_client(cliSock):
    # TODO: Start - Receive the request
    request = 
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
        webSock = 
        # TODO: End

        # TODO: Start - From the url, get the host name and path
        # e.g the hostname is gaia.cs.umass.edu, 
        # the path is /wireshark-labs/HTTP-wireshark-file1.html 
        webHostn = 
        webPath = 
        # TODO: End

        # Replace empty path with '/' character
        if webPath == '':
            webPath = '/'
        
        # TODO: Start - Establish connection with web server
    
        # TODO: End 

        # Check whether the file exists in the cache
        if os.path.exists(cacheFilePath):
            print(f"File found in cache: {url}")
            # TODO: Start - Get the last modification time of the file and 
            # construct if-modified-since header to request
            # (Hint: you may need to import another module to help with this)
            lastModified = 
            ifModSince = 
            #TODO: End
        else:
            ifModSince="\r\n"

        # Build a simple GET request
        webRequest = "GET " + webPath + " HTTP/1.1\r\nHost: " + webHostn +"\r\n" + ifModSince 

        # TODO: Start - Send the request to the web server
        
        # TODO: End

        # TODO: Start - Receive response from the web server
        response = 
        # TODO: End

        # TODO: Check for 304 Not Modified status code
        if :
        #TODO: End
            
            print(f"Not Modified, sending file from cache: {url}")
            # TODO: Start - Read data from the cache and send to client
        
            # TODO: End
            
        else:
            # Cache the response
            with open(cacheFilePath, 'wb') as cache_file:
                cache_file.write(response)
            
            # TODO: Start - Forward response to the client
            
            # TODO: End

    # Handle errors
    except Exception as e:
        # TODO: Start - Print an error message and send HTTP error code to the client

        # TODO: End

    # TODO: Start - Close the client socket 
    
    # TODO: End

    return

if __name__ == "__main__":
    start_proxy_server(proxy_host, proxy_port)

