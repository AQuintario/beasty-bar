import random
from src.Card import Card


class Player(Game):
    cards_all_players = 0
    num_cards_in_hand = 4

    def __init__(self, color, is_human = False):
        self.color = color
        self.deck = []
        self.hand = []
        self.is_human = is_human
        self.populate_deck()
        Player.cards_all_players += len(self.deck)

    def populate_deck(self):
        for i in range(1, 13, 1):
            self.deck.append(Card(i, self.color))

    def shuffle_deck(self):
        random.shuffle(self.deck)
        return

    def initial_draw(self):
        # Throw exception if len(hand)
        for _ in Player.num_cards_in_hand:
            self.draw_card()
        return

    def draw_card(self):
        if len(self.deck):
            self.hand.append(self.deck.pop())
        return

    def chose_card(self, method='Random'):
        if method == 'Random':
            chosen_card_from_hand = random.choice(self.hand)  # Distant future: not random
        return chosen_card_from_hand

    def