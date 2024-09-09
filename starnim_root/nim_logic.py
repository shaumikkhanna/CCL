from collections import Counter
from draw_page_nim import create_pdf


class Board:

    def __init__(self, piles, split_allowed, limit) -> None:
        self.piles = piles
        self.split_allowed = split_allowed
        if limit is None:
            self.limit = max(piles)
        else:
            self.limit = limit

    def play(self, pile, take, leave=None):
        if take < 1 or take > self.limit:
            raise ValueError(f"Invalid number {take}")
        
        if leave is not None:
            assert self.split_allowed, "Split not allowed"

            self.piles.insert(pile + 1, self.piles[pile] - leave - take)
            self.piles[pile] = leave
        else:
            self.piles[pile] -= take

    def is_empty(self):
        return all(pile == 0 for pile in self.piles)
    
    def __str__(self):
        out = ''
        for pile in self.piles:
            out += ' '.join(['o' for _ in range(pile)]) + '\n'

        return out

    def nimber(self):
        out = 0
        for pile in self.piles:
            out ^= pile

        return out
    
    def __eq__(self, other):
        return Counter(self.piles) == Counter(other.piles)
    
    def is_safe(self):
        return self.nimber() == 0
    
    def valid_moves(self):
        moves = []

        for ind, pile in enumerate(self.piles):
            for take in range(1, min(pile, self.limit) + 1):
                moves.append((ind, take))
        
        if self.split_allowed:
            for ind, pile in enumerate(self.piles):
                for take in range(1, min(pile, self.limit) + 1): # COULD BE A BUG
                    for leave in range(1, pile - take):
                        moves.append((ind, take, leave))
        
        return moves

    def find_safe_moves(self):
        if self.is_safe():
            raise ValueError("Game is already safe")

        safe_moves = []
        for move in self.valid_moves():
            new_board = Board(self.piles.copy(), split_allowed=self.split_allowed, limit=self.limit)
            new_board.play(*move)
            if new_board.is_safe():
                safe_moves.append(move)

        if safe_moves:
            return safe_moves
        else:
            raise ValueError("Something went wrong")
        
    def find_unsafe_moves(self):
        if not self.is_safe():
            raise ValueError("Game is already unsafe")

        unsafe_moves = []
        for move in self.valid_moves():
            new_board = Board(self.piles.copy(), split_allowed=self.split_allowed, limit=self.limit)
            new_board.play(*move)
            if not new_board.is_safe():
                unsafe_moves.append(move)

        if unsafe_moves:
            return unsafe_moves
        else:
            raise ValueError("Something went wrong")
        
    def board_after_one_move(self):
        if self.is_safe():
            move = self.find_unsafe_moves()[0]
        else:
            move = self.find_safe_moves()[0]

        new_board = Board(self.piles.copy(), split_allowed=self.split_allowed, limit=self.limit)
        new_board.play(*move)

        return new_board
    
    def all_children_boards(self):
        children = []
        for move in self.valid_moves():
            new_board = Board(self.piles.copy(), split_allowed=self.split_allowed, limit=self.limit)
            new_board.play(*move)
            children.append(new_board)

        return children
    
    def pages_required(self):
        unique_boards = []
        queue = [self]

        while queue:
            current = queue.pop(0)
            if current not in unique_boards:
                unique_boards.append(current)
                for child in current.all_children_boards():
                    if child not in unique_boards:
                        queue.append(child)

        return unique_boards
    
    def page_number(self):
        return ''.join(str(x) for x in sorted(self.piles))
    
    def create_pdf(self):
        if self.is_empty():
            my_text = [
                ("YOU WIN! \n", "bold_italic"),
                ("Congratulations!", "italic"),
            ]
            create_pdf(f"nim_pdfs/000.pdf", [0, 0, 0], my_text)

        else:
            page_number = self.board_after_one_move().page_number()
            if page_number == '000':
                my_text = [
                    ("You lose :( \n", "bold_italic"),
                    ("Better luck next time!", "italic"),
                ]
            else:
                my_text = [
                    ("Turn to page ", "regular"),
                    (page_number, "bold"),
                ]
            
            create_pdf(f"nim_pdfs/{self.page_number()}.pdf", sorted(self.piles), my_text)
    
