import socket
from _thread import *
import pickle


<<<<<<< HEAD
def threaded_client(conn):
    conn.send(pickle.dumps(players))                # 
    reply = ''
=======

position = [
    [0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0],
    [0,1,0,1,0,1,0,1],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [-1,0,-1,0,-1,0,-1,0],
    [0,-1,0,-1,0,-1,0,-1],
    [-1,0,-1,0,-1,0,-1,0]
    ]

def print_pos(pos):
    for i in range(len(pos)):
        print(pos[i])

def threaded_client(conn , current_user):
    conn.send(pickle.dumps("Server connection Sucess"))
>>>>>>> 6acf34d7842405e92ba835864086466c9f330ae1
    while True:
        try:
            msg = pickle.loads(conn.recv(2048))
            print(msg)
            conn.send(pickle.dumps(position))
            
            data = pickle.loads(conn.recv(2048))
            conn.send(pickle.dumps("recived 2"))
            if not (data or msg):
                print("Disconnected")
                break
            else:
                print(f"received : {msg}")
                print_pos(data)
                
        except Exception as e:
            print(f'Error: {e}')
            break
    
    print("Lost connection")
    conn.close()

def main():
    current_user = 0
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
        current_user += 1
        print(f'connected to {addr}')
        if current_user <= 2 :
            start_new_thread(threaded_client, (conn,current_user))
        else:
            conn.send(pickle.dumps("Server full"))
            

main()
