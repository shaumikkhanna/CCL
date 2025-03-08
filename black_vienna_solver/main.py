import random
import itertools
from math import log2
from collections import Counter
import pickle


class Game:


    def __init__(self, card_piles=None, query_cards=None, **config):
        self.query_history = [] # This is from the perspective of player 'me' and will not include any queries to 'me'.
        self.config = config
        self.player_cards = dict()

        '''
        config = {
            total_symbols: int (27),
            symbols_per_query_card: int (3),
            appearances_per_symbol: int (4),
            num_cards_vienna: int (3),
            num_cards_player: int (8),
        }
        '''

        if card_piles is not None: # If card piles given, assign to self.player_cards and fill out the config.
            config['num_cards_vienna'] = len(card_piles[-1])
            config['num_cards_player'] = len(card_piles[0])
            config['total_symbols'] = 3 * len(card_piles[0]) + config['num_cards_vienna']
            self.player_cards = dict(zip('abcv', card_piles))            


        if query_cards is not None: # If query cards given, assign to self.query_cards and fill out the config.
            config['symbols_per_query_card'] = len(query_cards[0])
            config['appearances_per_symbol'] = len(query_cards) * config['symbols_per_query_card'] // config['total_symbols']

            query_counter_values = Counter(itertools.chain(*query_cards)).values()
            assert all(v == config['appearances_per_symbol'] for v in query_counter_values), 'Asymmetric query cards'

            self.query_cards = query_cards
        
        else: # If query cards not given, generate query cards using config.
            self.generate_query_cards()


        # Is maintaining 3 available query cards.
        self.available_query_cards = self.query_cards.copy()
        random.shuffle(self.available_query_cards)


    def assign_cards_randomly(self):
        """
        Uses self.config to assign cards randomly to players 'me', 'left', 'right', and 'v'.
        """

        assert self.config is not None, 'Config not set'
        
        card_piles = list(range(1, self.config['total_symbols'] + 1))
        random.shuffle(card_piles)

        num_cards_player = self.config['num_cards_player']
        self.player_cards = {
            'me': card_piles[:num_cards_player],
            'left': card_piles[num_cards_player:2*num_cards_player],
            'right': card_piles[2*num_cards_player:3*num_cards_player],
            'v': card_piles[3*num_cards_player:]
        }


    def generate_query_cards(self): #TODO: Implement this
        pass 


    def query(self, query_card, to_player, update_db=False, update_query_deck=False):
        assert query_card in self.query_cards, 'Invalid query card'
        assert to_player in ['left', 'right'], 'Invalid player'

        answer = sum(q_symbol in self.player_cards[to_player] for q_symbol in query_card)

        if update_db:
            self.update_db(query_card, to_player, answer)

        if update_query_deck:
            self.available_query_cards.remove(query_card)
            self.available_query_cards.append(query_card)

        return answer
    
    
    def setup_db(self):
        """
        Assumes you are player 'me' and sets up the database of all possible card combinations for players 'left', 'right', and 'v'
        """

        self.all_possibilites = []

        # Possibilities of the form all combinaitons of (b, c, v)
        cards = set(range(1, self.config['total_symbols'] + 1))
        for my_card in self.player_cards['me']:
            cards.remove(my_card)

        for b_combination in itertools.combinations(cards, self.config['num_cards_player']):
            remaining_after_b = cards - set(b_combination)
            for c_combinaiton in itertools.combinations(remaining_after_b, self.config['num_cards_player']):
                v_combination = tuple(remaining_after_b - set(c_combinaiton))
                self.all_possibilites.append((b_combination, c_combinaiton, v_combination))


    def update_db(self, query_card, to_player, answer):
        """
        Given a query card, a player to query, and the answer, 
        updates the database of all possible card combinations for players 'left', 'right', and 'v'
        based on that information.
        """

        assert to_player in ['right', 'left'], 'Invalid player'
        assert type(answer) == int, 'Invalid answer'

        if not hasattr(self, 'all_possibilites'):
            self.setup_db()

        player_index = 0 if to_player == 'left' else 1 if to_player == 'right' else None
        func = lambda possibility: sum(q_symbol in possibility[player_index] for q_symbol in query_card) == answer
        self.all_possibilites = list(filter(func, self.all_possibilites))

        # Add the query to the query history
        self.query_history.append((query_card, to_player, answer))


    def update_db_bulk(self, query_tuples):
        """
        Given a list of query tuples (query_card, to_player, answer), 
        updates the database of all possible card combinations for players 'left', 'right', and 'v'
        based on that information.
        """

        if not hasattr(self, 'all_possibilites'):
            self.setup_db()

        out = []
        for possibility in self.all_possibilites:
            for query_tuple in query_tuples:
                query_card, to_player, answer = query_tuple
                player_index = 0 if to_player == 'left' else 1 if to_player == 'right' else None
                if sum(q_symbol in possibility[player_index] for q_symbol in query_card) != answer:
                    break
            else:
                out.append(possibility)

        self.all_possibilites = out


    @staticmethod
    def convert_letter_string_to_number(cards):
        symbols = 'abcdefghijklmnopqrstuvwxyz?'
        if type(cards) == list:
            return [[symbols.index(letter) + 1 for letter in card] for card in cards]
        else:
            return [symbols.index(letter) + 1 for letter in cards]
    

    def query_probabilities(self, query_card, to_player):
        """
        Given a query card and a player to query, returns a dict of the expected probabilities of each possible answer.
        """

        prob_dict = dict()
        for possibility in self.all_possibilites:
            player_index = 0 if to_player == 'left' else 1 if to_player == 'right' else None
            answer = sum(q_symbol in possibility[player_index] for q_symbol in query_card)
            prob_dict[answer] = prob_dict.get(answer, 0) + 1

        total = sum(prob_dict.values())
        return {k: v / total for k, v in prob_dict.items()}


    def vienna_distribution(self, pre_query=None, return_entropy=False):
        """
        Finds the probability distribution of the Vienna cards given the current state of the game.
        If pre_query is given, then the distribution is calculated as if that query, answer had been made.
        If return_entropy is True, then simply the entropy of the distribution is returned.
        """
        
        if pre_query is not None:
            query_card, to_player, answer = pre_query
            player_index = 0 if to_player == 'left' else 1 if to_player == 'right' else None
            
            func = lambda possibility: sum(q_symbol in possibility[player_index] for q_symbol in query_card) == answer
            working_all_possibilites = list(filter(func, self.all_possibilites))
        else:
            working_all_possibilites = self.all_possibilites

        viennas = dict()
        for possibility in working_all_possibilites:
            for vienna_card in possibility[2]: # MAINTAINING VIENNAS WITH SINGLE ELEMENT KEYS (instead of using all possible tuples for vienna)
                viennas[vienna_card] = viennas.get(vienna_card, 0) + 1

        total = sum(viennas.values())

        if return_entropy:
            return -sum(v/total * log2(v/total) for v in viennas.values())
        else:
            return {k: v / total for k, v in viennas.items()}


    def query_vienna_entropy(self, query_card, to_player):
        """
        Finds the entropy of the Vienna cards after a given query is made.
        """
    
        expected_entropy = 0
        for answer, prob_for_that_answer in self.query_probabilities(query_card, to_player).items():
            entropy_of_viennas_after_query_answer = self.vienna_distribution(
                pre_query=(query_card, to_player, answer), 
                return_entropy=True
            )
            expected_entropy += prob_for_that_answer * entropy_of_viennas_after_query_answer
            # print(f'Query: {query_card}\nTo: {to_player}\nAnswer: {answer}\nProbability for that answer:{prob_for_that_answer}\nEntropy: {entropy_of_viennas_after_query_answer}\n\n')

        return expected_entropy


    def best_query(self, show_all=False, query_deck=False):
        """
        Finds the best query to make based on the current state of the game.
        """

        best_query = None
        best_entropy = float('inf')
        
        if show_all:
            all_results = []

        available_query_cards = self.available_query_cards[:3] if query_deck else self.query_cards

        # Iterating through all possible queries (query card, player being asked) and all possible
        # answers with the probabilities of being that answer.
        for query_card in available_query_cards:
            for to_player in ['left', 'right']:

                # which query minimises  sum_Q   p_Q,j  *  H(P_(Q->j))   ?
                # where Q is some query and j is it's answer.
                # p_Q,j is the probability of getting answer j for query Q
                # P_(Q->j) is the prob_distribution of the Vienna cards after query Q, answer j has updated the db
                # H gives the entropy of the distribution
                
                expected_entropy = self.query_vienna_entropy(query_card, to_player)
            
                if expected_entropy < best_entropy:
                    best_query = (query_card, to_player)
                    best_entropy = expected_entropy

                if show_all:
                    all_results.append((query_card, to_player, expected_entropy))

        
        if show_all:
            all_results.sort(key=lambda x: x[2])
            for query_card, to_player, expected_entropy in all_results:
                print(f'Query: {query_card} To: {to_player} Entropy: {expected_entropy}\n')
        
        return best_query
        
        
    def check_if_ready_to_call(self, epsilon=0.001):
        vienna_distribution = self.vienna_distribution()
        call = []

        for k, v in vienna_distribution.items():
            if v > epsilon:
                call.append(k)

        if len(call) == self.config['num_cards_vienna']:
            return call
        else:
            return False


def test_run_game(T, query_cards, total_symbols, num_cards_vienna, num_cards_player, query_deck=True):
    avg_moves = []
    for _ in range(T):
        g = Game(query_cards=query_cards, total_symbols=total_symbols, num_cards_vienna=num_cards_vienna, num_cards_player=num_cards_player)
        g.assign_cards_randomly()
        g.setup_db()

        moves = 0
        while not g.check_if_ready_to_call():
            best_query = g.best_query(query_deck=query_deck)
            g.query(*best_query, update_db=True, update_query_deck=query_deck)
            moves += 1

        avg_moves.append(moves)

    print(f"For the game with symbols = {total_symbols},\nSymbols per query card = {g.config['symbols_per_query_card']}\nAppearances per symbol = {g.config['appearances_per_symbol']}\nNumber of vienna cards = {num_cards_vienna}\nNumber of player cards = {num_cards_player}\n in ({T} runs) --- \n")
    # print(f'Moves made in each game: {avg_moves}')
    print(f'Mean: {sum(avg_moves) / len(avg_moves)}')
    print(f'Std: {sum((m - sum(avg_moves) / len(avg_moves))**2 for m in avg_moves) / len(avg_moves)}')
    print('\n')


def setup_game():
    ##### Basic game
    QUERY_CARDS = [[1, 2, 3, 4], [2, 5, 6, 7], [3, 5, 8, 9], [4, 6, 8, 10], [1, 7, 9, 10]]
    # g = Game(query_cards=QUERY_CARDS, total_symbols=10, num_cards_vienna=1, num_cards_player=3)
    test_run_game(1000, QUERY_CARDS, 10, 1, 3)


    ##### Standard game
    # QUERY_CARDS = [
    #     'acl', 'agm', 'aos', 'apq', 'bcy', 'bhv', 'blm', 'bqt', 'cfi', 
    #     'csx', 'dhr', 'djz', 'dls', 'dvy', 'egw', 'enq', 'e?r', 'euv',
    #     'f?y', 'frx', 'fsz', 'gko', 'gpx', 'hn?', 'huz', 'i?w', 'ipr',
    #     'itz', 'jmo', 'jqx', 'jty', 'kmu', 'knt', 'kpw', 'lnv', 'ouw',
    # ]
    # QUERY_CARDS = Game.convert_letter_string_to_number(QUERY_CARDS)
    # g = Game(query_cards=QUERY_CARDS, total_symbols=27, num_cards_vienna=3, num_cards_player=8)


    ##### Custom game 1
    QUERY_CARDS = [
        [1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7], [5, 6, 7, 8], [6, 7, 8, 9], 
        [7, 8, 9, 10], [8, 9, 10, 11], [9, 10, 11, 12], [10, 11, 12, 1], [11, 12, 1, 2], [12, 1, 2, 3]
    ]
    # g = Game(query_cards=QUERY_CARDS, total_symbols=12, num_cards_vienna=3, num_cards_player=3)
    test_run_game(1000, QUERY_CARDS, 12, 3, 3)


    ##### Custom game 2
    QUERY_CARDS_A = [
        [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6], [5, 6, 7], [6, 7, 8], 
        [7, 8, 9], [8, 9, 10], [9, 10, 11], [10, 11, 12], [11, 12, 1], [12, 1, 2], 
    ]
    QUERY_CARDS_B = [  
        [1, 4, 8], [2, 5, 9], [3, 6, 10], [4, 7, 11], [5, 8, 12], [6, 9, 1], 
        [7, 10, 2], [8, 11, 3], [9, 12, 4], [10, 1, 5], [11, 2, 6], [12, 3, 7]
    ]
    QUERY_CARDS = QUERY_CARDS_A + QUERY_CARDS_B

    # g = Game(query_cards=QUERY_CARDS, total_symbols=12, num_cards_vienna=3, num_cards_player=3)
    test_run_game(1000, QUERY_CARDS_A, 12, 3, 3)
    test_run_game(1000, QUERY_CARDS_B, 12, 3, 3)
    test_run_game(1000, QUERY_CARDS, 12, 3, 3)


def main(data):
    QUERY_CARDS = [[1, 2, 3, 4], [2, 5, 6, 7], [3, 5, 8, 9], [4, 6, 8, 10], [1, 7, 9, 10]]
    g = Game(query_cards=QUERY_CARDS, total_symbols=10, num_cards_vienna=1, num_cards_player=3)
    my_cards = input('\n\nEnter your cards: \n')
    g.player_cards['me'] = [int(c) for c in my_cards.split(',')]
    g.setup_db()

    moves, win_flag = 0, False

    while True:
        next_move = input("\nEnter\nquery = record someone else's query\nmove = for your move\npass = for someone else's move\nlose = to indicate a loss\nquit = to quit\n")
          
        if next_move == 'move':
            if g.check_if_ready_to_call():
                print(g.vienna_distribution())
                win_flag = True
                break
            else:
                best_query_card, best_to_player = g.best_query(query_deck=False, show_all=True)
                print(f'Best query: {best_query_card} to {best_to_player}')
                answers = input('Enter the answer to the query: \n')
                g.update_db(query_card=best_query_card, to_player=best_to_player, answer=int(answers))

        elif next_move == 'query':
            query_card = input('Enter the query card: \n').split(',')
            query_card = [int(q) for q in query_card]
            to_player = input('Enter the player to query: \n')
            answer = int(input('Enter the answer: \n'))
            g.update_db(query_card, to_player, answer)

        elif next_move == 'lose':
            break

        elif next_move == 'pass':
            pass

        elif next_move == 'quit':
            data.append((moves, win_flag))
            return True

        else:
            print('Invalid input')
            continue

        moves += 1

    data.append((moves, win_flag))
    return False


if __name__ == '__main__':
    data = []
    
    while True:
        if main(data):

            with open(f'game_data_{random.randint(10**8)}.pickle', 'wb') as f:
                pickle.dump(data, f)

            break





    ##### Setup for puzzle
    # queries_answers_b = [
    #     ('ouw', 'left', 0),
    #     ('kpw', 'left', 0),
    #     ('apq', 'left', 0),
    #     ('jqx', 'left', 1),
    #     ('aos', 'left', 1),
    #     ('csx', 'left', 2),
    # ]
    # queries_answers_c = [
    #     ('bcy', 'right', 0),
    #     ('itz', 'right', 1),
    #     ('e?r', 'right', 1),
    #     ('kpw', 'right', 1),
    #     ('apq', 'right', 1),
    #     ('gpx', 'right', 1),
    #     ('egw', 'right', 1),
    # ]
    # QUERY_CARDS = [
    #     'acl', 'agm', 'aos', 'apq', 'bcy', 'bhv', 'blm', 'bqt', 'cfi', 
    #     'csx', 'dhr', 'djz', 'dls', 'dvy', 'egw', 'enq', 'e?r', 'euv',
    #     'f?y', 'frx', 'fsz', 'gko', 'gpx', 'hn?', 'huz', 'i?w', 'ipr',
    #     'itz', 'jmo', 'jqx', 'jty', 'kmu', 'knt', 'kpw', 'lnv', 'ouw',
    # ]
    # QUERY_CARDS = Game.convert_letter_string_to_number(QUERY_CARDS)
    # queries_answers_b = [(Game.convert_letter_string_to_number(q), p, a) for q, p, a in queries_answers_b]
    # queries_answers_c = [(Game.convert_letter_string_to_number(q), p, a) for q, p, a in queries_answers_c] 
    # g = Game(query_cards=QUERY_CARDS, total_symbols=27, num_cards_vienna=3, num_cards_player=8)
    # g.player_cards['me'] = Game.convert_letter_string_to_number('bcdetouv')
    # g.setup_db()
    # g.update_db_bulk(queries_answers_b)
    # g.update_db_bulk(queries_answers_c)



