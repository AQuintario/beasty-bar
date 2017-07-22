#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 21:00:41 2017

@author: adrian
"""

import random
random.seed(123)

######### GAME PARAMETERS #########
num_cards_in_hand = 5
num_cards_in_queue = 5
Queue = []
Bar = []
Alley = []
######### GAME PARAMETERS #########

######### DEFINE TURN'S SEQUENCE #########
# def turn(color)
# Phase 1: choose card from hand
# chosen_card_from_hand =







######### DEFINE TURN'S SEQUENCE #########




######### SETTING THINGS UP #########

deck_blue = ["B01", "B02", "B03", "B04", "B05", "B06",
             "B07", "B08", "B09", "B10", "B11", "B12"]
deck_green = ["G01", "G02", "G03", "G04", "G05", "G06",
              "G07", "G08", "G09", "G10", "G11", "G12"]

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
        print("Phase 1")
        print("Hand:", hand[color])
        print("Queue", Queue)
        # End phase 1
        
        # Phase 2: choose card from Queue
        
        # Phase 3: place selected card in Queue
        Queue.append(chosen_card_from_hand)
        # Printouts
        print("Phase 3")
        print("Hand:", hand[color])
        print("Queue", Queue)
        # End phase 3
        
        # Phase 4: instant habilities
        
        # Phase 5: recurrent habilities
        
        # Phase 6: resolve Queue
        if len(Queue) == 5:
            Alley.append(Queue.pop())
            Bar.append(Queue.pop(0))
            Bar.append(Queue.pop(0))
        
        # Printouts
        print("Phase 6")
        print("Hand:", hand[color])
        print("Queue", Queue)
        # End phase 6
        
        # Phase 7: draw a card from deck
        if len(deck[color]):
            hand[color].append(deck[color].pop())
        # Printouts
        print("Phase 7")
        print("Hand:", hand[color])
        print("Queue", Queue)
        # End phase 7
        
        print("")

