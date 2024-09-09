import random
import itertools
from math import log2




class Game:


    def __init__(self, card_piles=None, query_cards=None, **config):
        self.query_history = [] # This is from the perspective of player 'a' and will not include any queries to 'a'.
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
            self.query_cards = query_cards
        
        else: # If query cards not given, generate query cards using config.
            self.generate_query_cards()


    def assign_cards_randomly(self):
        """
        Uses self.config to assign cards randomly to players 'a', 'b', 'c', and 'v'.
        """

        assert self.config is not None, 'Config not set'
        
        card_piles = list(range(1, self.config['total_symbols'] + 1))
        random.shuffle(card_piles)

        num_cards_player = self.config['num_cards_player']
        self.player_cards = {
            'a': card_piles[:num_cards_player],
            'b': card_piles[num_cards_player:2*num_cards_player],
            'c': card_piles[2*num_cards_player:3*num_cards_player],
            'v': card_piles[3*num_cards_player:]
        }


    def generate_query_cards(self): #TODO: Implement this
        pass 


    def query(self, query_card, to_player, update_db=False):
        assert query_card in self.query_cards, 'Invalid query card'
        assert to_player in 'abc', 'Invalid player'

        answer = sum(q_symbol in self.player_cards[to_player] for q_symbol in query_card)

        if update_db:
            self.update_db(query_card, to_player, answer)

        return answer
    
    
    def setup_db(self):
        """
        Assumes you are player 'a' and sets up the database of all possible card combinations for players 'b', 'c', and 'v'
        """

        self.all_possibilites = []

        # Possibilities of the form all combinaitons of (b, c, v)
        cards = set(range(1, self.config['total_symbols'] + 1))
        for my_card in self.player_cards['a']:
            cards.remove(my_card)

        for b_combination in itertools.combinations(cards, self.config['num_cards_player']):
            remaining_after_b = cards - set(b_combination)
            for c_combinaiton in itertools.combinations(remaining_after_b, self.config['num_cards_player']):
                v_combination = tuple(remaining_after_b - set(c_combinaiton))
                self.all_possibilites.append((b_combination, c_combinaiton, v_combination))


    def update_db(self, query_card, to_player, answer):
        """
        Given a query card, a player to query, and the answer, 
        updates the database of all possible card combinations for players 'b', 'c', and 'v'
        based on that information.
        """

        if not hasattr(self, 'all_possibilites'):
            self.setup_db()

        player_index = 0 if to_player == 'b' else 1 if to_player == 'c' else None
        func = lambda possibility: sum(q_symbol in possibility[player_index] for q_symbol in query_card) == answer
        self.all_possibilites = list(filter(func, self.all_possibilites))

        self.query_history.append((query_card, to_player, answer))


    def update_db_bulk(self, query_tuples):
        """
        Given a list of query tuples (query_card, to_player, answer), 
        updates the database of all possible card combinations for players 'b', 'c', and 'v'
        based on that information.
        """

        if not hasattr(self, 'all_possibilites'):
            self.setup_db()

        out = []
        for possibility in self.all_possibilites:
            for query_tuple in query_tuples:
                query_card, to_player, answer = query_tuple
                player_index = 0 if to_player == 'b' else 1 if to_player == 'c' else None
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
            player_index = 0 if to_player == 'b' else 1 if to_player == 'c' else None
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
            player_index = 0 if to_player == 'b' else 1 if to_player == 'c' else None
            
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


    def best_query(self, show_all=False):
        """
        Finds the best query to make based on the current state of the game.
        """

        best_query = None
        best_entropy = float('inf')
        if show_all:
            all_queries = {}

        # Iterating through all possible queries (query card, player being asked) and all possible
        # answers with the probabilities of being that answer.
        for query_card in self.query_cards:
            for to_player in 'bc':

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
                    all_queries[(query_card, to_player)] = expected_entropy

        
        if show_all:
            print(sorted(all_queries, key=all_queries.get))
        
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



if __name__ == '__main__':

    ##### Basic game
    # QUERY_CARDS = [[1, 2, 3, 4], [2, 5, 6, 7], [3, 5, 8, 9], [4, 6, 8, 10], [1, 7, 9, 10]]
    # g = Game(query_cards=QUERY_CARDS, total_symbols=10, symbols_per_query_card=4, appearances_per_symbol=2, num_cards_vienna=1)


    ##### Standard game
    QUERY_CARDS = [
        'acl', 'agm', 'aos', 'apq', 'bcy', 'bhv', 'blm', 'bqt', 'cfi', 
        'csx', 'dhr', 'djz', 'dls', 'dvy', 'egw', 'enq', 'e?r', 'euv',
        'f?y', 'frx', 'fsz', 'gko', 'gpx', 'hn?', 'huz', 'i?w', 'ipr',
        'itz', 'jmo', 'jqx', 'jty', 'kmu', 'knt', 'kpw', 'lnv', 'ouw',
    ]
    QUERY_CARDS = Game.convert_letter_string_to_number(QUERY_CARDS)
    g = Game(query_cards=QUERY_CARDS, total_symbols=27, symbols_per_query_card=3, appearances_per_symbol=4, num_cards_vienna=3, num_cards_player=8)


    # Setup for puzzle

    queries_answers_b = [
        ('ouw', 'b', 0),
        ('kpw', 'b', 0),
        ('apq', 'b', 0),
        ('jqx', 'b', 1),
        ('aos', 'b', 1),
        ('csx', 'b', 2),
    ]

    queries_answers_c = [
        ('bcy', 'c', 0),
        ('itz', 'c', 1),
        ('e?r', 'c', 1),
        ('kpw', 'c', 1),
        ('apq', 'c', 1),
        ('gpx', 'c', 1),
        ('egw', 'c', 1),
    ]

    queries_answers_b = [(Game.convert_letter_string_to_number(q), p, a) for q, p, a in queries_answers_b]
    queries_answers_c = [(Game.convert_letter_string_to_number(q), p, a) for q, p, a in queries_answers_c]


    # g.assign_cards_randomly()
    # g.setup_db()
    # print(g.player_cards)
    # print(g.vienna_distribution())
    # print(g.best_query())
