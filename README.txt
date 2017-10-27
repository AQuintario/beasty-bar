

This is a virtual implementation of the board game Beasty Bar: https://boardgamegeek.com/boardgame/165950/beasty-bar

In this game, every player controls a a deck of 12 animal cards that get in line to go into a bar.
When the line reaches five animals, the two firsts get into the bar and the last "dies".
Also, whenever an animal gets in line, their special skills are played to try to be first or kick out rivals.

This program has 2 parts: a simulator of the game and a learning module.
In the simulator, the decks and table are virtualized, and the rules programmed.
It also generates games where the plays and state of the table and players hands get logged.

In the learning module, the game logs are fed to a neural network that tries to learn the best card to play
depending on the state of the game table.

The idea is that at the beginning two virtual players play against each other in random mode
and the game log of a high number of games is passed to the neural network for training.
Then, the virtual players use the predict mode of the NN to choose what card to play.
These games are in turn logged, the net is retrained and so on.

At the moment, the Multilayer Perceptron (MLP) provided in the SciKit library is used.
The main goal achieved so far has come after the first training of the NN on random data.
When the game is random, the winning rate are around 30% (and a 40% probability of reaching a draw).
From this, the virtual player using the trained neural net achieves a winning rate of 60%
(and draw probability descends to 30%).