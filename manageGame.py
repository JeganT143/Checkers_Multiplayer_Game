from checkers.board import Board
from checkers.constants import WHITE, BLACK

class Manage:
    def __init__(self, id):
        self.id = id
        self.board = Board()       # The board with pieces and positions.
        self.turn = WHITE          # WHITE (player 0) always starts.
        self.ready = False         # Set to True when both players are connected.
        self.p1Went = False
        self.p2Went = False

    def play(self, player, move):
        """
        Expects a move string formatted as "start_row,start_col:end_row,end_col"
        and performs the move only if it's that player's turn.
        """
        try:
            start, end = move.split(":")
            start_row, start_col = map(int, start.split(","))
            end_row, end_col = map(int, end.split(","))
        except Exception as e:
            print("Invalid move format:", move)
            return

        piece = self.board.get_piece(start_row, start_col)
        if piece == 0:
            print("No piece at starting position!")
            return

        # Enforce turn order.
        if self.turn != piece.color:
            print("Not your turn!")
            return

        # Verify the player is moving their own piece.
        if (player == 0 and piece.color != WHITE) or (player == 1 and piece.color != BLACK):
            print("Not your piece!")
            return

        valid_moves = self.board.get_valid_moves(piece)
        if (end_row, end_col) in valid_moves:
            self.board.move(piece, end_row, end_col)
            skipped = valid_moves[(end_row, end_col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            print("Invalid move destination!")

    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False

    def winner(self):
        return self.board.winner()
