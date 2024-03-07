import socket
import time
# Server's IP address
# If the server is not on this machine,
# put the private (network) or public IP address (if over the internet)
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 7005  # Server's port


def client_program():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    while True:
        # Input message you want to send to the server
        message = input("Enter your message ('quit' to exit): ")

        if message.lower().strip() == 'quit':
            client_socket.send('quit'.encode())  # Send quit message to server
            break

        # Send message
        client_socket.send(message.encode())

        while True:
            # Receive response from the server
            response = client_socket.recv(1024).decode()
            if not response:
                break
            # Iterate through each character in the response and print it on the same line
            for char in response:
                print(char, end='', flush=True)
                time.sleep(0.05)  # Adjust the sleep time as needed for desired speed


    # Close the socket when done
    client_socket.close()


client_program()
