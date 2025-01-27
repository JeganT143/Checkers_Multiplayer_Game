from network import Network

def print_pos(pos):
    for i in range(len(pos)):
        print(pos[i])

def main():
    run = True
    n = Network()
    msg  = n.get_msg()
    print(msg)
    reply = n.send("Waiting for initial position")
    if reply != "waiting for second player" :
        initial_pos = reply
        print("initial Position recived")
        print_pos(initial_pos)
    else:
        print(f"Server says : {reply}")
    
main()
