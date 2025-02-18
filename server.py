import socket
from _thread import start_new_thread
import pickle
from manageGame import Manage  # Use our multiplayer game logic

# Server setup
server = socket.gethostbyname(socket.gethostname())
# server = "10.50.60.110"
print(server)
port = 5050
svr_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    svr_skt.bind((server, port))
except socket.error as e:
    print(str(e))

svr_skt.listen()
print("Waiting for a connection. Server started at", server)

# Game management variables
games = {}
idCount = 0

def get_state(game):
    """
    Return a dictionary representing the current game state.
    """
    state = {
        'board': game.board,   # Both machines must have the same checkers module
        'ready': game.ready,
        'turn': game.turn,
        'winner': game.winner()
    }
    return state

def threaded_client(conn, p, gameId):
    global idCount
    # Send the player's number (0 for white, 1 for black) to the client.
    conn.send(str.encode(str(p)))
    print(f"Player role {p} sent to a client in game {gameId}")
    
    while True:
        try:
            data = conn.recv(1024 * 4)
            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                
                # Data is expected as a UTF-8 string command.
                data_str = data.decode()
                
                if data_str == "reset":
                    game.resetWent()
                    print("Game reset status updated")
                elif data_str != "get":
                    print("Move received:", data_str)
                    game.play(p, data_str)
                
                # Send back the updated game state as a pickled dictionary.
                state = get_state(game)
                conn.sendall(pickle.dumps(state))
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
    print("Connected to:", addr)
    
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
