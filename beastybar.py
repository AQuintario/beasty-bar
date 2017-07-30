#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 21:00:41 2017

@author: adrian
"""

from src.instant_actions import instant_actions, recurrent_actions
from src.Player import Player
from src.Table import Table
from src.LogNN import LogNN

import random
random.seed(123)


# Setting things up
table = Table()
players = []
players.append(Player("Blue"))
players.append(Player("Green"))
logNN = LogNN()

turn_counter = 1

while Player.cards_all_players:
    print("Turn", turn_counter)
    turn_counter += 1

    for player in players:
        # Read table and hands and convert to 01010100
        logNN.read_table(table, player)

        # Phases 1 and 2: choose card from hand and target card from queue
        chosen_card_from_hand, chosen_target = player.choose_cards(table)
        print("Hand:", player.hand, "Card chosen:", chosen_card_from_hand)

        # Phase 3: place selected card in queue
        table.queue.append(chosen_card_from_hand)

        # Phase 4: instant abilities
        instant_actions(table, chosen_card_from_hand, chosen_target)

        # Phase 5: recurrent abilities (starting for the nearest to the bar)
        recurrent_actions(table, chosen_card_from_hand)

        # Phase 6: resolve queue
        table.resolve_queue()
        if player == players[len(players)-1]:
            print("Phase 6")
            print("queue", table.queue)
            print("")

        # Phase 7: draw a card from deck
        player.draw_card()


print("Bar:", table.bar, "\n")
blue_points, green_points = 0, 0
winner_color = None
for c in table.bar:
    if c.color == "Green":
        green_points += 1
    if c.color == "Blue":
        blue_points += 1
if green_points == blue_points:
    print("Draw")
elif green_points > blue_points:
    print("Green player wins!")
    winner_color = "Green"
else:
    print("Blue player wins!")
    winner_color = "Blue"

logNN.remove_hand(winner_color)
logNN.printout(winner_color)


