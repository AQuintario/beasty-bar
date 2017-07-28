import random
import src.Card


class Player(Game):
    cards_all_players = 0

    def __init__(self, color, is_human = False):
        self.color = color
        self.deck = []
        self.hand = []
        self.is_human = is_human
        self.populate_deck()
        cards_all_players = len(self.deck)

    def populate_deck(self):
        self.deck.append(Skunk(self.color))
        self.deck.append(Parrot(self.color))
        self.deck.append(Kangaroo(self.color))
        self.deck.append(Monkey(self.color))
        self.deck.append(Chameleon(self.color))
        self.deck.append(Seal(self.color))
        self.deck.append(Zebra(self.color))
        self.deck.append(Giraffe(self.color))
        self.deck.append(Snake(self.color))
        self.deck.append(Crocodile(self.color))
        self.deck.append(Hippo(self.color))
        self.deck.append(Lion(self.color))
        return

    def shuffle_deck(self):
        random.shuffle(self.deck)
        return

    def initial_draw(self):
        # Throw exception if len(hand)
        for _ in Game.num_cards_in_hand:
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