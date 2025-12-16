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

def choose_from_list(items):
    if not items:
        print("No items found.")
        return None

    for item in items:
        if "title" in item:
            print(f"{item['id'] + 1}. {item['title']}")
        else:
            print(f"{item['id'] + 1}. {item['name']}")

    while True:
        choice = input("Select item number (or B to go back): ")
        if choice.lower() == "b":
            return None
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(items):
                return index
        print("Invalid input. Please enter a valid number or B to go back.")


def main():
    username = input("Enter username: ")

    s = socket.socket()
    s.connect((HOST, PORT))
    send_json(s, {"client_name": username})

    while True:
        print("\nMAIN MENU")
        print("1. Search headlines")
        print("2. List of sources")
        print("3. Quit")

        choice = input("Choose: ")

        if choice == "1":
            print("\nHEADLINES MENU")
            print("1. Search by keyword")
            print("2. Search by category")
            print("3. Search by country")
            print("4. List all")
            print("5. Back")

            sub = input("Choose: ")
            params = {}

            if sub == "1":
                params["q"] = input("Enter keyword: ")
            elif sub == "2":
                params["category"] = input("Enter category: ")
            elif sub == "3":
                params["country"] = input("Enter country code: ")
            elif sub == "4":
                pass
            else:
                continue

            send_json(s, {"type": "headlines", "params": params})
            response = recv_json(s)

            index = choose_from_list(response.get("items", []))
            if index is not None:
                send_json(s, {"type": "details", "index": index})
                details = recv_json(s)
                print("\nDETAILS:")
                for k, v in details.get("item", {}).items():
                    print(f"{k}: {v}")

        
        elif choice == "2":
            print("\nSOURCES MENU")
            print("1. Search by category")
            print("2. Search by country")
            print("3. Search by language")
            print("4. List all")
            print("5. Back")

            sub = input("Choose: ")
            params = {}

            if sub == "1":
                params["category"] = input("Enter category: ")
            elif sub == "2":
                params["country"] = input("Enter country code: ")
            elif sub == "3":
                params["language"] = input("Enter language: ")
            elif sub == "4":
                pass
            else:
                continue

            send_json(s, {"type": "sources", "params": params})
            response = recv_json(s)

            index = choose_from_list(response.get("items", []))
            if index is not None:
                send_json(s, {"type": "details", "index": index})
                details = recv_json(s)
                print("\nDETAILS:")
                for k, v in details.get("item", {}).items():
                    print(f"{k}: {v}")
            
        elif choice == "3":
            send_json(s, {"type": "quit"})
            break

    s.close()


if __name__ == "__main__":
    main()

