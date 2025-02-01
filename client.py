from network import Network

def print_pos(pos):
    for i in range(len(pos)):
        print(pos[i])

def main():
    run = True
    n = Network()
    msg  = n.get_msg()
    print(msg)
    initial_pos= n.send("Waiting for initial position")
    print("initial pos recived")
    print_pos(initial_pos)
    
    
main()
