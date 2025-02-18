import pygame
from network import Network
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, YELLOW, WHITE, BLACK
import socket

pygame.font.init()
pygame.mixer.init() 

SELECT_SOUND = pygame.mixer.Sound("select.wav") 
MOVE_SOUND = pygame.mixer.Sound("move.wav") 
START_SOUND = pygame.mixer.Sound("game_start.wav")


FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers - Multiplayer")

def draw_text(surface, text, size, color, center):
    """Helper function to draw centered text."""
    font = pygame.font.SysFont("comicsans", size)
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=center)
    surface.blit(text_surface, rect)

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

class NetworkGame:
    def __init__(self):
        self.network = Network()  
        self.player = self.network.getP()  # 0 for WHITE, 1 for BLACK.
        # Get the initial game state (a dictionary)
        self.game = self.network.send("get")
        self.selected = None

    def update(self):
        self.game = self.network.send("get")
        # Now self.game is a dictionary with keys: 'ready', 'turn', 'winner', 'board'
        if not self.game['ready']:
            WIN.fill((30, 30, 30))
            draw_text(WIN, "Waiting for second player...", 40, (255, 255, 255), (WIDTH//2, HEIGHT//2))
        else:
            # Draw the board from the game state.
            self.game['board'].draw(WIN)
            self.draw_valid_moves()
            self.draw_ui()

    def draw_valid_moves(self):
        if self.selected is not None:
            row, col = self.selected
            piece = self.game['board'].get_piece(row, col)
            my_color = WHITE if self.player == 0 else BLACK
            if piece != 0 and piece.color == my_color:
                valid_moves = self.game['board'].get_valid_moves(piece)
                for move in valid_moves:
                    r, c = move
                    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    s.set_alpha(100)
                    s.fill(YELLOW)
                    WIN.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))

    def draw_ui(self):
        my_color = WHITE if self.player == 0 else BLACK
        turn_text = "Your Turn" if self.game['turn'] == my_color else "Opponent's Turn"
        turn_color = (0, 255, 0) if self.game['turn'] == my_color else (255, 0, 0)
        draw_text(WIN, turn_text, 30, turn_color, (WIDTH//2, 20))
        color_text = "You are WHITE" if self.player == 0 else "You are BLACK"
        draw_text(WIN, color_text, 24, (200,200,200), (90, HEIGHT-20))
        draw_text(WIN, "Select piece then destination", 20, (200,200,200), (WIDTH//2, HEIGHT-20))

    def select(self, row, col):
        if not self.game['ready']:
            return
        my_color = WHITE if self.player == 0 else BLACK
        if self.game['turn'] != my_color:
            print("Not your turn!")
            return
        if self.selected is None:
            self.selected = (row, col)
            SELECT_SOUND.play() 
        else:
            move_str = f"{self.selected[0]},{self.selected[1]}:{row},{col}"
            response = self.network.send(move_str)  # Sending move request to server
            
            if response == "valid":
                MOVE_SOUND.play() 
            
            self.selected = None

def main():
    run = True
    clock = pygame.time.Clock()
    net_game = NetworkGame()

    while run:
        clock.tick(FPS)
        net_game.update()
        pygame.display.update()

        if net_game.game['ready'] and net_game.game['winner'] is not None:
            winner = net_game.game['winner']
            win_color = "WHITE" if winner == WHITE else "BLACK"
            WIN.fill((30,30,30))
            draw_text(WIN, "Game Over!", 50, (255,255,255), (WIDTH//2, HEIGHT//2 - 50))
            draw_text(WIN, f"Winner: {win_color}", 40, (255,215,0), (WIDTH//2, HEIGHT//2))
            draw_text(WIN, "Press any key to exit...", 30, (200,200,200), (WIDTH//2, HEIGHT//2 + 50))
            pygame.display.update()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        run = False
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        waiting = False
                        run = False
                clock.tick(FPS)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if net_game.game['ready']:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    net_game.select(row, col)
    pygame.quit()

def menu_screen():
    pygame.mixer.Sound.play(START_SOUND)
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        WIN.fill((50,50,50))
        draw_text(WIN, "Multiplayer Checkers", 60, (255,0,0), (WIDTH//2, HEIGHT//2 - 50))
        draw_text(WIN, "Press any key or click to play!", 40, (255,255,255), (WIDTH//2, HEIGHT//2 + 20))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    main()

if __name__ == "__main__":
    menu_screen()
