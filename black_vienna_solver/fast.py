import random
import itertools
from math import log2
from collections import Counter



class Game:


    def __init__(self, card_piles=None, query_cards=None, **config):
        self.query_history = [] # This is from the perspective of player 'me' and will not include any queries to 'me'.
        self.config = config
        self.player_cards = dict()
        self.useless_query_flag = False # If a query has been made that was useless / did not make any difference in the vienna dist.

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
            self.player_cards = dict(zip(['me', 'left', 'right', 'v'], card_piles))            


        if query_cards is not None: # If query cards given, assign to self.query_cards and fill out the config.
            config['symbols_per_query_card'] = len(query_cards[0])
            config['appearances_per_symbol'] = len(query_cards) * config['symbols_per_query_card'] // config['total_symbols']

            query_counter_values = Counter(itertools.chain(*query_cards)).values()
            assert all(v == config['appearances_per_symbol'] for v in query_counter_values), 'Asymmetric query cards'

            self.query_cards = query_cards
        
        else: # If query cards not given, generate query cards using config.
            self.generate_query_cards()


        # Is maintaining 3 available query cards.
        self.available_query_cards_deck = self.query_cards.copy()
        random.shuffle(self.available_query_cards_deck)

        self.available_query_cards_in_play = []


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


    def query(self, query_card, to_player, update_db=False):
        assert query_card in self.query_cards, 'Invalid query card'
        assert to_player in ['left', 'right'], 'Invalid player'

        answer = sum(q_symbol in self.player_cards[to_player] for q_symbol in query_card)

        if update_db:
            self.update_db(query_card, to_player, answer)

        # If the query card was already on the table
        if query_card in self.available_query_cards_in_play:
            pass
        # If the query card was in the deck, it will be moved to the table
        elif query_card in self.available_query_cards_deck:
            self.available_query_cards_deck.remove(query_card)
            self.available_query_cards_in_play.append(query_card)
        # Something went wrong
        else:
            raise ValueError('Query card not available')

        return answer
    
    
    def setup_db(self):
        self.db = dict()

        # Possibilities of the form all combinaitons of (left, right, v)
        cards = set(range(1, self.config['total_symbols'] + 1))
        for my_card in self.player_cards['me']:
            cards.remove(my_card)

        for b_combination in itertools.combinations(cards, self.config['num_cards_player']):
            remaining_after_b = cards - set(b_combination)
            for c_combinaiton in itertools.combinations(remaining_after_b, self.config['num_cards_player']):
                v_combination = tuple(remaining_after_b - set(c_combinaiton))
                self.all_possibilites.append((b_combination, c_combinaiton, v_combination))


    @staticmethod
    def convert_letter_string_to_number(cards):
        symbols = 'abcdefghijklmnopqrstuvwxyz?'
        if type(cards) == list:
            return [[symbols.index(letter) + 1 for letter in card] for card in cards]
        else:
            return [symbols.index(letter) + 1 for letter in cards]


