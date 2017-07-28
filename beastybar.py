#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 21:00:41 2017

@author: adrian
"""

from src.instant_actions import instant_actions
from src.Card import Card
from src.Player import Player

import random
random.seed(123)


######### GAME PARAMETERS #########
num_cards_in_hand = 4


class Table(object):
    queue = []
    bar = []
    alley = []
    max_num_cards_in_queue = 5

    def resolve_queue(self):
        if len(self.queue) == 5:
            self.alley.append(self.queue.pop())
            self.bar.append(self.queue.pop(0))
            self.bar.append(self.queue.pop(0))

table = Table()

######### GAME PARAMETERS #########


######### SETTING THINGS UP #########
players = []
players.append(Player("Blue"))

# Old style:
# deck_blue = []
# deck_green = []
# player_blue.populate_deck()
# for i in range(1, 13, 1):
#     color = "Blue"
#     deck_blue.append(Card(i, color))
    # color = "Green"
    # deck_green.append(Card(i, color))
# hand_blue = []
# hand_green = []
# random.shuffle(deck_blue)
# random.shuffle(deck_green)
# for i in range(num_cards_in_hand):
    # hand_blue.append(deck_blue.pop())
    # hand_green.append(deck_green.pop())
# hand = {"blue": hand_blue, "green": hand_green}
# deck = {"blue": deck_blue, "green": deck_green}
######### SETTING THINGS UP #########


turn_counter = 1
# while len(hand_blue)+len(deck_blue) and len(hand_green)+len(deck_green):
while Player.cards_all_players:
    print("Turn", turn_counter)
    turn_counter += 1

    # for color in "blue", "green":
    for player in players:
        # Phase 1: choose card from hand
        # chosen_card_from_hand = random.choice(hand[color])  # Distant future: not random
        # hand[color].remove(chosen_card_from_hand)
        # Printouts
        chosen_card_from_hand = player.choose_card()
        print("Phases 1, 2")
        print("Hand:", player.hand, "Card chosen:", chosen_card_from_hand,
              Player.cards_all_players, "total cards, left")
        print("queue", table.queue)
        # End phase 1
        
        # # Phase 2: choose card from queue
        # chosen_target = None
        # if len(table.queue) and chosen_card_from_hand.id == 2 or chosen_card_from_hand.id == 5:
        #     chosen_target = random.choice(table.queue)
        chosen_target = player.choose_card_from_queue(table)

        # Phase 3: place selected card in queue
        table.queue.append(chosen_card_from_hand)
        # Printouts
        print("Phase 3")
        print("queue", table.queue)
        # End phase 3
        
        # Phase 4: instant abilities
        instant_actions(table, chosen_card_from_hand, chosen_target)
        print("Phase 4")
        print("queue", table.queue)

        # Phase 5: recurrent abilities (starting for the nearest to the bar)
        for c in table.queue[:]:  # Make a copy of the queue before shaking it
            if c.is_recurrent and c != chosen_card_from_hand:
                instant_actions(table, c)
        print("Phase 5")
        print("queue", table.queue)

        # Phase 6: resolve queue
        table.resolve_queue()
        # Printouts
        print("Phase 6")
        print("queue", table.queue)

        # Phase 7: draw a card from deck
        # if len(deck[color]):
        #     hand[color].append(deck[color].pop())
        player.draw_card()

        print("")

print("Bar:", table.bar, "\n")
blue_points, green_points = 0, 0
for c in table.bar:
    if c.color == "Green":
        green_points += 1
    if c.color == "Blue":
        blue_points += 1
if green_points == blue_points:
    print("Draw")
elif green_points > blue_points:
    print("Green player wins!")
else:
    print("Blue player wins!")