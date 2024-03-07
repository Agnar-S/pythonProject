import socket
import vectorbot as vb

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 7005  # Port to listen on (non-privileged ports are > 1023)


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server started and listening on {HOST}:{PORT}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                data1 = vb.run(data.decode(), conn)
                print(data1)
                if not data:
                    conn.send("No data...")
                    break


start_server()
