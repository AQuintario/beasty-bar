#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 21:00:41 2017

@author: adrian
"""

from src.instant_actions import play_a_game
from src.Player import Player
from src.Table import Table
from src.LogNN import LogNN
from src.MyMLPClassifier import MyMLPClassifier

import os
import time
import random
random.seed(1235)

# Training log
n_games = 10
log_file = 'log/ngames'+str(n_games)+'_RvR.pkl'
logNN = LogNN(log_file)
tic = time.clock()
if not logNN.log_exists:
    print('Random vs Random')
    players = [Player('Blue', 'Random'), Player('Green', 'Random')]
    logNN.reset_wins()
    for _ in range(n_games):
        table = Table()
        winner_color = play_a_game(table, players, logNN)
        logNN.wins[winner_color] += 1
    # logNN.printout()
    logNN.save()
toc = time.clock()
print(logNN.wins)
print(n_games, 'games:', toc-tic, 'seconds')

# Actual training
hl_size = 1000
nn_file = 'log/trained_nn_' + str(hl_size) + '_hls.pkl'
warm_start = True
clf = MyMLPClassifier(nn_file, solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(hl_size,),
                      random_state=1, verbose=False, warm_start=warm_start)
tic = time.clock()
if not clf.nn_exists or warm_start:
    print('Starting fit...')
    X, Y = logNN.X, logNN.Y
    clf.fit(X, Y)
    clf.save()
toc = time.clock()
print('Fitting took', toc-tic, 'seconds')

# Testing
testing_file = clf.filename.split('/')
testing_file = 'log/testing_of_' + testing_file[1]
logNN = LogNN(testing_file)
tic = time.clock()
print('NN vs Random')
players = [Player('Blue', 'NN', clf), Player('Green', 'Random')]
logNN.reset_wins()
for _ in range(10000):
    table = Table()
    winner_color = play_a_game(table, players, logNN)
    logNN.wins[winner_color] += 1
# logNN.printout()
logNN.save()
toc = time.clock()
print(logNN.wins)
print(10000, 'games:', toc-tic, 'seconds')
print(clf)


# This is the end, my friend
os.system("afplay ../dundunduuun.mp3")
