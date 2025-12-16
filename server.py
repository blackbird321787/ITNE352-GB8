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
GROUP_ID = "group_8"
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
    response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
    return response.json()


def handle_client(conn, addr):
    hello = recv_json(conn)
    client_name = hello["client_name"]
    print(f"[CONNECTED] {client_name} from {addr}")

    last_results = [] 

    while True:
        req = recv_json(conn)
        if not req:
            break

        req_type = req["type"]

        if req_type == "quit":
            break

        print(f"[REQUEST] {client_name} | {req_type} | {req.get('params')}")

        if req["type"] == "headlines":
            data = fetch_news("top-headlines", req.get("params", {}))
            filename = f"{client_name}_headlines_{GROUP_ID}.json"
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
            articles = data.get("articles", [])[:MAX_RESULTS]
            last_results = articles
            
            brief_list = []
            for i, a in enumerate(articles):
                brief_list.append({
                    "id": i,
                    "title": a.get("title"),
                    "source": a["source"]["name"],
                    "author": a.get("author")
                })

            send_json(conn, {"type": "list", "items": brief_list})
            
        elif req_type == "sources":
            data = fetch_news("top-headlines/sources", req.get("params", {}))

            filename = f"{client_name}_sources_{GROUP_ID}.json"
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)

            sources = data.get("sources", [])[:MAX_RESULTS]
            last_results = sources

            brief_list = []
            for i, s in enumerate(sources):
                brief_list.append({
                    "id": i,
                    "name": s.get("name")
                })

            send_json(conn, {"type": "list", "items": brief_list})
        elif req_type == "details":
            index = req.get("index")

            if 0 <= index < len(last_results):
                send_json(conn, {
                    "type": "details",
                    "item": last_results[index]
                })
            else:
                send_json(conn, {
                    "type": "error",
                    "message": "Invalid selection"
                })
                
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

