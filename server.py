import socket
from _thread import start_new_thread
import pickle
from manageGame import Manage  # Use our multiplayer game logic

# Server setup
server = socket.gethostbyname(socket.gethostname())
port = 5050
svr_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    svr_skt.bind((server, port))
except socket.error as e:
    print(str(e))

svr_skt.listen()
print("Waiting for a connection. Server started....")

# Game management variables
games = {}
idCount = 0

def threaded_client(conn, p, gameId):
    global idCount
    # Send the player's number (0 or 1) to the client
    conn.send(str.encode(str(p)))
    print(f"Player role {p} sent to a client in game {gameId}")
    
    while True:
        try:
            data = conn.recv(1024 * 4)
            if gameId in games:
                game = games[gameId]
                
                if not data:
                    break
                
                # Convert data to string (e.g., "get", "reset", or a move like "2,3:3,4")
                data_str = data.decode()
                
                if data_str == "reset":
                    game.resetWent()
                    print("Game reset status updated")
                elif data_str != "get":
                    # Process a move command received from the client
                    print("Move received:", data_str)
                    game.play(p, data_str)
                
                # Send back the updated game state as a pickled object
                conn.sendall(pickle.dumps(game))
                print("Game state sent to player", p)
            else:
                break  
        except Exception as e:
            print("Error:", e)
            break
    
    print("Lost connection")
    try:
        del games[gameId]
        print(f"Closing game {gameId}")
    except KeyError:
        pass
    
    idCount -= 1
    conn.close()

while True:
    conn, addr = svr_skt.accept()
    print(f"Connected to: {addr}")
    
    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    
    if idCount % 2 == 1:
        games[gameId] = Manage(gameId)
        print(f"Creating a new game with ID: {gameId}")
    else:
        games[gameId].ready = True
        p = 1
        print(f"Game {gameId} is ready to start")
    
    start_new_thread(threaded_client, (conn, p, gameId))
