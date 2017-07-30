class LogNN(object):
    # class LogNN global vars
    n_cards = 12
    n_turns = 12
    n_pos = 8
    n_players = 2
    bar_offset = 5
    alley_offset = 6
    hand_offset = 7
    # class LogNN global vars

    def __init__(self):
        self.b_play = []
        self.g_play = []
        self.col_map_play = {"Blue": self.b_play, "Green": self.g_play}

        self.hand_indexes = [LogNN.n_pos * i + LogNN.hand_offset for i in range(LogNN.n_cards)]
        self.hand_indexes.sort(reverse=True)

    def read_table(self, table, player):
        # Read table and hands and convert to 01010100
        b_turn = [0] * (LogNN.n_cards * LogNN.n_pos)
        g_turn = [0] * (LogNN.n_cards * LogNN.n_pos)
        col_map = {"Blue": b_turn, "Green": g_turn}
        pc = player.color

        for o in range(len(table.queue)):
            i = table.queue[o].id
            c = table.queue[o].color
            pos = LogNN.n_pos * (i - 1) + o
            col_map[c][pos] = 1
        for card in table.bar:
            i = card.id
            c = card.color
            pos = LogNN.n_pos * (i - 1) + LogNN.bar_offset
            col_map[c][pos] = 1
        for card in table.alley:
            i = card.id
            c = card.color
            pos = LogNN.n_pos * (i - 1) + LogNN.alley_offset
            col_map[c][pos] = 1
        for card in player.hand:
            i = card.id
            pos = LogNN.n_pos * (i - 1) + LogNN.hand_offset
            col_map[pc][pos] = 1

        self.col_map_play[pc].append(col_map[pc])
        return

    def remove_hand(self, winner_color):
        print("Winner color:", winner_color)
        for c in self.col_map_play:
            print("c:", c)
            if c != winner_color:
                print(c, "is a loser")
                print("col_map[c]:", self.col_map_play[c][0][0:20], "...")
                for log in self.col_map_play[c]:
                    for i in self.hand_indexes:
                        del log[i]
        return

    def printout(self, winner_color):
        for color in self.col_map_play:
            if color == winner_color:
                print(" SSSSSSSSSSSSSSSSSSSSSS, PPPPPPPPPPPPPPPPPPPPPP, KKKKKKKKKKKKKKKKKKKKKK, MMMMMMMMMMMMMMMMMMMMMM, "
                      "CCCCCCCCCCCCCCCCCCCCCC, SSSSSSSSSSSSSSSSSSSSSS, ZZZZZZZZZZZZZZZZZZZZZZ, GGGGGGGGGGGGGGGGGGGGGG, "
                      "SSSSSSSSSSSSSSSSSSSSSS, CCCCCCCCCCCCCCCCCCCCCC, HHHHHHHHHHHHHHHHHHHHHH, LLLLLLLLLLLLLLLLLLLLLL")
                for i in self.col_map_play[color]:
                    print(i)
                print("")
            else:
                print(" SSSSSSSSSSSSSSSSSSS, PPPPPPPPPPPPPPPPPPP, KKKKKKKKKKKKKKKKKKK, MMMMMMMMMMMMMMMMMMM, "
                      "CCCCCCCCCCCCCCCCCCC, SSSSSSSSSSSSSSSSSSS, ZZZZZZZZZZZZZZZZZZZ, GGGGGGGGGGGGGGGGGGG, "
                      "SSSSSSSSSSSSSSSSSSS, CCCCCCCCCCCCCCCCCCC, HHHHHHHHHHHHHHHHHHH, LLLLLLLLLLLLLLLLLLL")
                for i in self.col_map_play[color]:
                    print(i)
