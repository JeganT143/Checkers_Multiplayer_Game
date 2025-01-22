import socket
from _thread import *
import pickle

players = ['Player1', 'Player2']

def threaded_client(conn):
    conn.send(pickle.dumps(players))
    reply = ''
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if not data:
                print("Disconnected")
                break
            else:
                print(f"received : {data}")
        except Exception as e:
            print(f'Error: {e}')
            break
    
    print("Lost connection")
    conn.close()

def main():
    server = socket.gethostbyname(socket.gethostname())
    port = 5050

    svr_sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        svr_sct.bind((server, port))
    except socket.error as e:
        print(str(e))

    svr_sct.listen()
    print("Waiting for connections, server started")

    while True:
        conn, addr = svr_sct.accept()
        print(f'connected to {addr}')
        start_new_thread(threaded_client, (conn,))

main()
