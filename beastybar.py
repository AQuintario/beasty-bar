#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 21:00:41 2017

@author: adrian
"""

# from src.instant_actions import instant_actions, recurrent_actions
from src.instant_actions import play_a_game
from src.Player import Player
from src.Table import Table
from src.LogNN import LogNN

from sklearn.neural_network import MLPClassifier
import pickle


import time
import random
random.seed(123456)


# Setting things up
logNN = LogNN()

verbose = False

wins = {'Blue': 0, 'Green': 0, 'Draw': 0}

n_games = 10000
with open('log/trained_nn_1000_hlu_10000_games.pkl', 'rb') as nn_file:
    clf = pickle.load(nn_file)
logNN.clf = clf

try:
    with open('log/NNvsNN_ngames'+str(n_games)+'.pkl', 'rb') as log_file:
        X = pickle.load(log_file)
        Y = pickle.load(log_file)
except FileNotFoundError:
        tic = time.clock()
        for g in range(n_games):
            table = Table()
            players = [Player('Blue', 'NN'), Player('Green', 'NN')]
            winner_color = play_a_game(table, players, logNN)
            wins[winner_color] += 1

        # logNN.printout()
        X, Y = logNN.return_log()
        with open('log/NNvsNN_ngames'+str(n_games)+'.pkl', 'wb') as output_file:
            pickle.dump(X, output_file, -1)
            pickle.dump(Y, output_file, -1)
        toc = time.clock()
        print(n_games, 'games:', toc-tic, 'seconds')
        print(wins)

hl_size = 1000
try:
    with open('log/trained_nn_' + str(hl_size) + '_hlu_' + str(n_games) + '_games_NNvsNN.pkl', 'rb') as nn_file:
        clf = pickle.load(nn_file)
except FileNotFoundError:
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(hl_size,), random_state=1, verbose=False)
    tic = time.clock()
    clf.fit(X, Y)
    with open('log/trained_nn_' + str(hl_size) + '_hlu_' + str(n_games) + '_games_NNvsNN.pkl', 'wb') as nn_file:
        pickle.dump(clf, nn_file, -1)
    toc = time.clock()
    print('Fitting takes', toc-tic, 'seconds')


logNN.clf = clf
n_games = 10000
for g in range(n_games):
    table = Table()
    players = [Player('Blue', 'NN'), Player('Green', 'Random')]
    winner_color = play_a_game(table, players, logNN)
    wins[winner_color] += 1

# logNN.printout()
X, Y = logNN.return_log()
with open('log/ngames' + str(n_games) + '.pkl', 'wb') as output_file:
    pickle.dump(X, output_file, -1)
    pickle.dump(Y, output_file, -1)
toc = time.clock()
print(wins)
