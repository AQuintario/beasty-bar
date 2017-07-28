#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 21:00:41 2017

@author: adrian
"""

from src.instant_actions import instant_actions
from src.Card import Card

import random
random.seed(123)


######### GAME PARAMETERS #########
num_cards_in_hand = 4
num_cards_in_queue = 5


class Table(object):
    queue = []
    bar = []
    alley = []

table = Table()

######### GAME PARAMETERS #########






######### SETTING THINGS UP #########
deck_blue = []
deck_green = []
for i in range(1, 13, 1):
    color = "Blue"
    deck_blue.append(Card(i, color))
    color = "Green"
    deck_green.append(Card(i, color))

hand_blue = []
hand_green = []

random.shuffle(deck_blue)
random.shuffle(deck_green)

for i in range(num_cards_in_hand):
    hand_blue.append(deck_blue.pop())
    hand_green.append(deck_green.pop())

######### SETTING THINGS UP #########


hand = {"blue": hand_blue, "green": hand_green}
deck = {"blue": deck_blue, "green": deck_green}

turn_counter = 1
while len(hand_blue)+len(deck_blue) and len(hand_green)+len(deck_green):
    print("Turn", turn_counter)
    turn_counter += 1

    for color in "blue", "green":
    
        # Phase 1: choose card from hand
        chosen_card_from_hand = random.choice(hand[color])  # Distant future: not random
        hand[color].remove(chosen_card_from_hand)
        # Printouts
        print("Phases 1, 2")
        print("Hand:", hand[color], "Card chosen:", chosen_card_from_hand)
        print("queue", table.queue)
        # End phase 1
        
        # Phase 2: choose card from queue
        chosen_target = None
        if len(table.queue) and chosen_card_from_hand.id == 2 or chosen_card_from_hand.id == 5:
            chosen_target = random.choice(table.queue)

        # Phase 3: place selected card in queue
        table.queue.append(chosen_card_from_hand)
        # Printouts
        print("Phase 3")
        # print("Hand:", hand[color])
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
        if len(table.queue) == 5:
            table.alley.append(table.queue.pop())
            table.bar.append(table.queue.pop(0))
            table.bar.append(table.queue.pop(0))
        
        # Printouts
        print("Phase 6")
        print("queue", table.queue)

        # Phase 7: draw a card from deck
        if len(deck[color]):
            hand[color].append(deck[color].pop())
        # Printouts

        
        print("")

print("Bar:", table.bar)