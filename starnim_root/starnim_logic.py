import random
from draw_page_starnim import draw_n_pointed_star, create_pdf_with_svg


class Starnim:

    def __init__(self, node_states=None, ordered_states=None, grundy=None) -> None:
        if node_states is None and ordered_states is None:
            raise ValueError("You must provide either node_states or ordered_states")
        if node_states is not None and ordered_states is not None:
            raise ValueError("You can't provide both node_states and ordered_states")
        if ordered_states is not None:
            self.ordered_states = ordered_states
            self.node_states = self.get_original_order()
        if node_states is not None:
            self.node_states = node_states
            self.ordered_states = self.get_ordered_states()

        if grundy is not None:
            self.grundy = grundy
        else:
            self.calculate_grundy()

    def calculate_grundy(self):
        G = [0, 1, 2]
        n = len(self.node_states)

        for ind in range(3, n):
            grundy_of_all_possible_moves = [
                G[k] ^ G[ind - k - 1] for k in range(ind // 2 + 1)
            ] + [
                G[k] ^ G[ind - k - 2] for k in range(ind // 2 + 1)
            ]
            G.append(Starnim.mex(grundy_of_all_possible_moves))

        self.grundy = G

    def get_ordered_states(self):
        n = len(self.node_states)

        new_order = [0]

        for _ in range(n - 1):
            new_order.append(
                (new_order[-1] + n // 2) % n
            )
        out = []
        for i in range(n):
            out.append(self.node_states[new_order[i]])

        return out
    
    def get_original_order(self):
        rearranged_properties = self.ordered_states
        
        n = len(rearranged_properties)  # Number of properties (nodes)
        original_properties = [None] * n  # Initialize with None to hold original order
        next_node = 0  # Start from the original starting node
        
        # Calculate the node jumps based on how they were rearranged
        jump = n // 2  # Halfway across the circle, as used in rearrangement

        for i in range(n):
            original_properties[next_node] = rearranged_properties[i]
            next_node = (next_node + jump) % n  # Move to the next node as per the star connectivity

        return original_properties
    
    @property
    def pile_dict(self):
        # Convert the node states to a dictionary of piles. The nodes are represented in odrered order.
        pile_dict = {}
        running_inds = []

        for ind, node in enumerate(self.ordered_states):
            if not node:
                running_inds.append(ind)
            else:
                if not running_inds:
                    continue
                pile_dict[len(pile_dict)] = running_inds
                running_inds = []

        if running_inds:
            if not self.ordered_states[0]:
                try:
                    pile_dict[0] = running_inds + pile_dict[0]
                except KeyError:
                    pile_dict[0] = running_inds
            else:
                pile_dict[len(pile_dict)] = running_inds

        return pile_dict
    
    def play(self, nodes):
        # Nodes are written in the ordered order.

        if len(nodes) > 2:
            raise ValueError(f"Too many nodes. Expected 1 or 2, got {len(nodes)}")
        if len(nodes) == 2:
            for v in self.pile_dict.values():
                if nodes[0] in v and nodes[1] in v:
                    break
            else:
                raise ValueError("The nodes are not connected")

        assert self.ordered_states[nodes[0]] == 0, "The node is already taken"
        self.ordered_states[nodes[0]] = 1
        if len(nodes) == 2:
            assert self.ordered_states[nodes[1]] == 0, "The secont node is already taken"
            self.ordered_states[nodes[1]] = 1

        self.node_states = self.get_original_order()

    def is_empty(self):
        return all(self.node_states)
    
    def is_full(self):
        return not any(self.node_states)

    def __str__(self):
        out = ''
        for v in self.pile_dict.values():
            out += ' '.join(['o' for _ in range(len(v))]) + '\n'

        return out

    def nimber(self):
        out = 0
        for v in self.pile_dict.values():
            out ^= self.grundy[len(v)]

        return out
    
    @staticmethod
    def mex(numbers):
        numbers = set(numbers)
        for i in range(len(numbers) + 1):
            if i not in numbers:
                return i
    
    def __eq__(self, other):
        list1, list2 = self.node_states, other.node_states

        if len(list1) != len(list2):
            return False
        
        # Concatenate list1 with itself
        double_list1 = list1 + list1
        
        # Convert lists to strings for easy substring check
        str_list1 = ''.join(map(str, double_list1))
        str_list2 = ''.join(map(str, list2))
        
        # Check if list2 is a substring of the concatenated list1
        return str_list2 in str_list1
    
    def is_safe(self):
        if self.is_full():
            return True

        return self.nimber() == 0
    
    def valid_moves(self):
        moves = []
        for v in self.pile_dict.values():
            if len(v) == 1:
                moves.append((v[0],))
            else:
                moves.append((v[0],))
                for ind in range(1, len(v)):
                    moves.append((v[ind],))
                    moves.append((v[ind - 1], v[ind]))

        return moves

    def find_safe_moves(self):
        if self.is_safe():
            raise ValueError("Game is already safe")

        safe_moves = []
        for move in self.valid_moves():
            new_star = Starnim(node_states=self.node_states.copy(), grundy=self.grundy.copy())
            new_star.play(move)
            if new_star.is_safe():
                safe_moves.append(move)

        if safe_moves:
            return safe_moves
        else:
            raise ValueError("Something went wrong")
        
    def find_unsafe_moves(self):
        if not self.is_safe():
            raise ValueError("Game is already unsafe")

        return self.valid_moves()
        
    def board_after_one_move(self):
        if self.is_safe():
            move = self.find_unsafe_moves()[0]
        else:
            move = self.find_safe_moves()[0]

        new_star = Starnim(node_states=self.node_states.copy(), grundy=self.grundy.copy())
        new_star.play(move)

        return new_star

    def next_move_node(self, error_probability=0):
        # Find move in the ordered order
        if random.random() < error_probability:
            ordered_move = random.choice(self.valid_moves())
        elif self.is_safe():
            ordered_move = random.choice(self.find_unsafe_moves())
        else:
            ordered_move = random.choice(self.find_safe_moves())

        return [
            self.ordered_node_to_normal_node(ordered_node) for ordered_node in ordered_move
        ]

    def ordered_node_to_normal_node(self, ordered_node):
        return (ordered_node * (len(self.node_states) // 2)) % len(self.node_states)

    def all_children_boards(self):
        children = []
        for move in self.valid_moves():
            new_star = Starnim(node_states=self.node_states.copy(), grundy=self.grundy.copy())
            new_star.play(move)
            children.append(new_star)

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
        return ''.join(str(int(not x)) for x in self.node_states)
    
    def create_pdf(self):
        #TODO fix the page number and node lables
        draw_n_pointed_star(self.node_states, list(range(len(self.node_states))))
        if self.is_empty():
            my_text = [
                ("YOU WIN! \n", "bold_italic"),
                ("Congratulations!", "italic"),
            ]
            create_pdf_with_svg(f"starnim_pdfs/000000000.pdf", '000000000', my_text)

        else:
            page_number = self.board_after_one_move().page_number()
            if page_number == '000000000':
                my_text = [
                    ("You lose :( \n", "bold_italic"),
                    ("Better luck next time!", "italic"),
                ]
            else:
                my_text = [
                    ("Turn to page ", "regular"),
                    (page_number, "bold"),
                ]
            
            create_pdf_with_svg(f"starnim_pdfs/{self.page_number()}.pdf", self.page_number(), my_text)
    
