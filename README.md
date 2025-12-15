# ITNE352-GB8

# News Service System – Client/Server Project

## Project Description
This project implements a Python-based client–server news service system.
The server retrieves live news data from NewsAPI.org and serves multiple
clients simultaneously using TCP sockets and multithreading. Clients can
request news headlines and sources, view summarized lists, and retrieve
detailed information for selected items.

## Semester
S1 2025–2026

## Group Information
- Group Name: GB8
- Course: ITNE352 – Network Programming
- Section: 25261
- Student 1: Sarah Khalid 202102356
- Student 2: Ayah Hasan 202306851

## Table of Contents
1. Project Description
2. Requirements
3. How to Run the System
4. Scripts Description
5. Additional Concepts
6. Conclusion
7. Acknowledgments

## Requirements
To run this project, the following are required:
- Python 3.x
- `requests` Python library
- NewsAPI.org API key
- Internet connection

## How to Run the System
1. Install the required library:  
   ```bash
   pip install requests

2. Set the NewsAPI API key as an environment variable:  
macOS / Linux:  
export NEWS_API_KEY="YOUR_API_KEY"

Windows (PowerShell):  
$env:NEWS_API_KEY="YOUR_API_KEY"


3. Start the server:  
python server.py


4. Start the client in a new terminal:  
python client.py

5. Follow the on-screen menus to browse headlines and sources.

Scripts Description  
server.py

The server script listens for incoming TCP connections and handles multiple
clients concurrently using threads. It communicates with the NewsAPI to
retrieve news headlines and sources based on client requests, saves retrieved
data into JSON files for evaluation, and sends summarized and detailed results
back to the clients.

client.py

The client script connects to the server, sends the user’s name, and presents
interactive menus. It allows users to request news headlines or sources, view
lists of results, select individual items, and retrieve full details from the
server.

Additional Concepts

This project uses multithreading to allow the server to handle multiple
simultaneous client connections efficiently. Each client is served in a
separate thread, ensuring responsiveness and scalability.

Conclusion

This project demonstrates the implementation of a complete client–server
application using Python sockets, APIs, JSON handling, and multithreading. It
provides hands-on experience with network programming concepts and real-world
API integration.

Acknowledgments

We would like to thank Dr. Mohammed Almeer for his guidance and support
throughout the development of this project.
