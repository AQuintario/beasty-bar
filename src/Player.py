import random
import numpy
from src.Card import Card
from src.LogNN import LogNN


class Player(object):
    cards_all_players = 0
    num_cards_in_hand = 4
    num_players = 0

    def __init__(self, color, method='Random', clf=None, is_human=False):
        self.color = color
        self.method = method
        if self.method == 'NN':
            self.clf = clf
        self.is_human = is_human
        self.deck = []
        self.hand = []
        Player.num_players += 1
        self.turn_pos = Player.num_players
        self.chosen_card_from_hand = None
        self.chosen_target = None

    def reset(self):
        self.deck = []
        self.hand = []
        self.populate_deck()
        self.shuffle_deck()
        self.initial_draw()
        Player.cards_all_players += len(self.deck) + len(self.hand)

    def __eq__(self, other):
        return self.color == other.color

    def is_last(self):
        return self.turn_pos == Player.num_players

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

    def choose_card_random(self):
        self.chosen_card_from_hand = random.choice(self.hand)  # Distant future: not random
        return self.chosen_card_from_hand

    def place_card_in_queue(self):
        self.hand.remove(self.chosen_card_from_hand)
        Player.cards_all_players -= 1

    def choose_card_from_queue_random(self, table):
        self.chosen_target = None
        # Choose Parrot's target
        if self.chosen_card_from_hand.id == 2:
            opp_cards_in_queue = []
            opp_cards_in_queue[:] = (c for c in table.queue if c.color != self.color)
            if len(opp_cards_in_queue):
                self.chosen_target = random.choice(opp_cards_in_queue)
        # Choose Chameleon's target
        elif self.chosen_card_from_hand.id == 5:
            queue_ids = []
            queue_ids[:] = (c.id for c in table.queue if c.id != 2 and c.id != 5)
            queue_ids = list(set(queue_ids))
            if len(queue_ids):
                target_id = random.choice(queue_ids)
                self.chosen_target = Card(target_id, "")
        return self.chosen_target

    def choose_cards(self, table):
        if self.method == 'NN':
            self.chosen_card_from_hand, self.chosen_target = self.choose_cards_NN(table)
        elif self.method == 'Random':
            self.chosen_card_from_hand = self.choose_card_random()
            self.chosen_target = None
            if self.chosen_card_from_hand.id == 2 or self.chosen_card_from_hand.id == 5:
                self.chosen_target = self.choose_card_from_queue_random(table)
        self.place_card_in_queue()
        return self.chosen_card_from_hand, self.chosen_target

    def read_table(self, table):
        pc = self.color
        table_status = [0] * (LogNN.n_cards*(LogNN.n_pos + (LogNN.n_players - 1)*(LogNN.n_pos - 1)))
        for o, card in enumerate(table.queue):
            i = card.id
            c = card.color
            player_offset, n_pos = (0, LogNN.n_pos) if c == pc else (LogNN.player_offset, LogNN.n_pos-1)
            pos = n_pos * (i - 1) + player_offset + LogNN.queue_offset + o
            table_status[pos] = 1
        for card in table.bar:
            i = card.id
            c = card.color
            player_offset, n_pos = (0, LogNN.n_pos) if c == pc else (LogNN.player_offset, LogNN.n_pos-1)
            pos = n_pos * (i - 1) + player_offset + LogNN.bar_offset
            table_status[pos] = 1
        for card in table.alley:
            i = card.id
            c = card.color
            player_offset, n_pos = (0, LogNN.n_pos) if c == pc else (LogNN.player_offset, LogNN.n_pos-1)
            pos = n_pos * (i - 1) + player_offset + LogNN.alley_offset
            table_status[pos] = 1
        for card in self.hand:
            i = card.id
            pos = LogNN.n_pos * (i - 1) + LogNN.hand_offset
            table_status[pos] = 1
        return table_status

    def get_log_prob_pred(self, table):
        # table_status = self.read_table(table)
        table_status = LogNN.get_table_status(table, self)
        table_status = numpy.array(table_status)
        table_status = table_status.reshape(1, -1)
        return self.clf.predict_log_proba(table_status)[0]

    def vector_index_to_ids(self, index):
        id_played, id_target = 0, 0
        if index == 0:
            id_played = 1
        elif index == 1:
            id_played = 3
        elif index == 2:
            id_played = 4
        elif 3 <= index <= 9:
            id_played = index + 3
        elif 10 <= index <= 22:
            id_played = 2
            id_target = index - 9
        elif 23 <= index <= 35:
            id_played = 5
            id_target = index - 22
        return id_played, id_target

    def choose_cards_NN(self, table):
        probs = self.get_log_prob_pred(table)
        sort_index = numpy.argsort(probs)
        sort_index = sort_index.tolist()
        sort_index.reverse()
        own_color = self.color
        for c in 'Blue', 'Green':
            if c != own_color:
                rival_color = c
        for i in sort_index:
            id_candidate_from_hand, id_candidate_from_table = self.vector_index_to_ids(i)
            candidate_from_hand = Card(id_candidate_from_hand, own_color)
            if candidate_from_hand not in self.hand:
                continue
            if id_candidate_from_hand == 2:  # What happens when playing the Parrot
                if id_candidate_from_table < 13:
                    candidate_from_table = Card(id_candidate_from_table, rival_color)
                    if candidate_from_table not in table.queue:
                        continue
            elif id_candidate_from_hand == 5:  # What happens when playing the Chameleon
                if id_candidate_from_table < 13:
                    queue_ids = []
                    queue_ids[:] = (c.id for c in table.queue)
                    if id_candidate_from_table not in queue_ids:
                        continue
                    candidate_from_table = Card(id_candidate_from_hand, '')
                    # I think it's ok to leave blank the color of the mimicked card
            if id_candidate_from_table == 0 or id_candidate_from_table == 13:
                candidate_from_table = None
            try:
                return candidate_from_hand, candidate_from_table
            except UnboundLocalError:
                print(candidate_from_hand, id_candidate_from_table)
                exit(1)

