import socket
import threading
import json
import struct
import os
import requests

HOST = "127.0.0.1"
PORT = 65432

NEWS_API_KEY = "9d9b66c1e4e04b8a85656fae87e7f1b1"
BASE_URL = "https://newsapi.org/v2"
GROUP_ID = "group_X"
MAX_RESULTS = 15


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


def fetch_news(endpoint, params):
    params["apiKey"] = NEWS_API_KEY
    r = requests.get(f"{BASE_URL}/{endpoint}", params=params)
    return r.json()


def handle_client(conn, addr):
    hello = recv_json(conn)
    client_name = hello["client_name"]
    print(f"[CONNECTED] {client_name} from {addr}")

    while True:
        req = recv_json(conn)
        if not req:
            break

        if req["type"] == "quit":
            break

        if req["type"] == "headlines":
            data = fetch_news("top-headlines", req["params"])
            filename = f"{client_name}_headlines_{GROUP_ID}.json"
            json.dump(data, open(filename, "w"), indent=2)

            articles = data.get("articles", [])[:MAX_RESULTS]
            brief = [{"title": a["title"], "source": a["source"]["name"]} for a in articles]
            send_json(conn, {"type": "list", "items": brief, "full": articles})

        if req["type"] == "sources":
            data = fetch_news("top-headlines/sources", req["params"])
            filename = f"{client_name}_sources_{GROUP_ID}.json"
            json.dump(data, open(filename, "w"), indent=2)

            sources = data.get("sources", [])[:MAX_RESULTS]
            brief = [{"name": s["name"]} for s in sources]
            send_json(conn, {"type": "list", "items": brief, "full": sources})

    conn.close()
    print(f"[DISCONNECTED] {client_name}")


def main():
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen()
    print("Server running...")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    main()
