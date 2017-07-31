import random
from src.Card import Card


class Player(object):
    cards_all_players = 0
    num_cards_in_hand = 4

    def __init__(self, color, is_human=False):
        self.color = color
        self.deck = []
        self.hand = []
        self.is_human = is_human
        self.chosen_card_from_hand = None
        self.chosen_target = None
        self.populate_deck()
        self.shuffle_deck()
        self.initial_draw()
        Player.cards_all_players += len(self.deck) + len(self.hand)

    def __eq__(self, other):
        return self.color == other.color

    def populate_deck(self):
        for i in range(1, 13, 1):
            self.deck.append(Card(i, self.color))

    def shuffle_deck(self):
        random.shuffle(self.deck)
        return

    def initial_draw(self):
        # Throw exception if len(hand)
        for _ in range(Player.num_cards_in_hand):
            self.draw_card()
        return

    def draw_card(self):
        if len(self.deck):
            self.hand.append(self.deck.pop())
        return

    def choose_card(self, method='Random'):
        if method == 'Random':
            self.chosen_card_from_hand = random.choice(self.hand)  # Distant future: not random
        self.hand.remove(self.chosen_card_from_hand)
        Player.cards_all_players -= 1
        return self.chosen_card_from_hand

    def choose_card_from_queue(self, table, method='Random'):
        self.chosen_target = None
        # Choose Parrot's target
        if self.chosen_card_from_hand.id == 2:
            opp_cards_in_queue = []
            opp_cards_in_queue[:] = (c for c in table.queue if c.color != self.color)
            if len(opp_cards_in_queue):
                if method == 'Random':
                    self.chosen_target = random.choice(opp_cards_in_queue)
        # Choose Chameleon's target
        elif self.chosen_card_from_hand.id == 5:
            queue_ids = []
            queue_ids[:] = (c.id for c in table.queue if c.id != 2 and c.id != 5)
            queue_ids = list(set(queue_ids))
            if len(queue_ids):
                if method == 'Random':
                    target_id = random.choice(queue_ids)
                    self.chosen_target = Card(target_id, "")
        return self.chosen_target

    def choose_cards(self, table, method='Random'):
        self.chosen_card_from_hand = self.choose_card(method)
        self.chosen_target = None
        if self.chosen_card_from_hand.id == 2 or self.chosen_card_from_hand.id == 5:
            self.chosen_target = self.choose_card_from_queue(table, method)
        return self.chosen_card_from_hand, self.chosen_target
