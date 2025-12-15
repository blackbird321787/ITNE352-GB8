import socket
import json
import struct

HOST = "127.0.0.1"
PORT = 65432


def send_json(conn, data):
    encoded = json.dumps(data).encode()
    conn.sendall(struct.pack("!I", len(encoded)))
    conn.sendall(encoded)


def recv_json(conn):
    header = conn.recv(4)
    if not header:
        return None
    length = struct.unpack("!I", header)[0]
    body = conn.recv(length)
    return json.loads(body.decode())


def main():
    username = input("Enter username: ")

    s = socket.socket()
    s.connect((HOST, PORT))
    send_json(s, {"client_name": username})

    while True:
        print("\n1. Headlines\n2. Sources\n3. Quit")
        choice = input("Choose: ")

        if choice == "1":
            send_json(s, {"type": "headlines", "params": {"country": "us"}})
            res = recv_json(s)
            for i, item in enumerate(res["items"], 1):
                print(i, item["title"])

        elif choice == "2":
            send_json(s, {"type": "sources", "params": {}})
            res = recv_json(s)
            for i, item in enumerate(res["items"], 1):
                print(i, item["name"])

        elif choice == "3":
            send_json(s, {"type": "quit"})
            break

    s.close()


if __name__ == "__main__":
    main()
