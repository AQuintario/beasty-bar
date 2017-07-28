#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 21:00:41 2017

@author: adrian
"""

from src.instant_actions import instant_actions, recurrent_actions
from src.Player import Player
from src.Table import Table

import random
random.seed(123)


######### SETTING THINGS UP #########
table = Table()
players = []
players.append(Player("Blue"))
players.append(Player("Green"))
######### SETTING THINGS UP #########


turn_counter = 1

while Player.cards_all_players:
    print("Turn", turn_counter)
    turn_counter += 1

    # for color in "blue", "green":
    for player in players:
        # Phase 1: choose card from hand
        chosen_card_from_hand = player.choose_card()
        print("Phases 1, 2")
        print("Hand:", player.hand, "Card chosen:", chosen_card_from_hand,
              Player.cards_all_players, "total cards, left")
        print("queue", table.queue)

        # Phase 2: choose card from queue
        chosen_target = player.choose_card_from_queue(table)

        # Phase 3: place selected card in queue
        table.queue.append(chosen_card_from_hand)
        print("Phase 3")
        print("queue", table.queue)

        # Phase 4: instant abilities
        instant_actions(table, chosen_card_from_hand, chosen_target)
        print("Phase 4")
        print("queue", table.queue)

        # Phase 5: recurrent abilities (starting for the nearest to the bar)
        recurrent_actions(table, chosen_card_from_hand)
        print("Phase 5")
        print("queue", table.queue)

        # Phase 6: resolve queue
        table.resolve_queue()
        print("Phase 6")
        print("queue", table.queue)

        # Phase 7: draw a card from deck
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