from network import Network
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, YELLOW, WHITE, BLACK
import pickle

pygame.font.init()

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers - Multiplayer")

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

class NetworkGame:
    """
    Wraps the network connection and the game state received from the server.
    """
    def __init__(self, win):
        self.win = win
        self.network = Network()
        self.player = self.network.getP()  # 0 for WHITE, 1 for BLACK
        # Get the initial game state from the server
        self.game = self.network.send("get")
        self.selected = None

    def update(self):
        # Request the latest game state from the server
        self.game = self.network.send("get")
        
        # If the second player hasn't connected, display a waiting message.
        if not self.game.ready:
            self.win.fill((0, 0, 0))
            font = pygame.font.SysFont("comicsans", 50)
            text = font.render("Waiting for second player...", True, (255, 255, 255))
            self.win.blit(
                text,
                (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2),
            )
        else:
            self.game.board.draw(self.win)
            self.draw_valid_moves()
            self.draw_turn_indicator()

    def draw_valid_moves(self):
        # If a piece is selected, highlight its valid moves.
        if self.selected is not None:
            row, col = self.selected
            piece = self.game.board.get_piece(row, col)
            # Only show moves if the selected piece belongs to the current player.
            my_color = WHITE if self.player == 0 else BLACK
            if piece != 0 and piece.color == my_color:
                valid_moves = self.game.board.get_valid_moves(piece)
                for move in valid_moves:
                    r, c = move
                    pygame.draw.rect(
                        self.win, YELLOW, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    )

    def draw_turn_indicator(self):
        # Draw a simple turn indicator at the top of the screen.
        my_color = WHITE if self.player == 0 else BLACK
        font = pygame.font.SysFont("comicsans", 30)
        if self.game.turn == my_color:
            text = font.render("Your Turn", True, (0, 255, 0))
        else:
            text = font.render("Opponent's Turn", True, (255, 0, 0))
        self.win.blit(text, (10, 10))

    def select(self, row, col):
        # Do not allow moves if the game is not ready.
        if not self.game.ready:
            return

        # Determine the player's color.
        my_color = WHITE if self.player == 0 else BLACK
        
        # Check if it's this player's turn.
        if self.game.turn != my_color:
            print("Not your turn!")
            return

        if self.selected is None:
            self.selected = (row, col)
        else:
            # Format the move as "start_row,start_col:end_row,end_col"
            move_str = f"{self.selected[0]},{self.selected[1]}:{row},{col}"
            self.network.send(move_str)
            self.selected = None

def main():
    run = True
    clock = pygame.time.Clock()
    net_game = NetworkGame(WIN)

    while run:
        clock.tick(FPS)
        net_game.update()
        pygame.display.update()

        # Check for a winner only if both players are connected.
        if net_game.game.ready and net_game.game.winner() is not None:
            winner = net_game.game.winner()
            print("Winner:", "WHITE" if winner == WHITE else "BLACK")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Only process clicks if the game is ready.
                if net_game.game.ready:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    net_game.select(row, col)

    pygame.quit()

def menu_screen():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        WIN.fill((225, 225, 53))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        WIN.blit(text, (100, 200))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    main()

if __name__ == "__main__":
    menu_screen()
