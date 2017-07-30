class LogNN(object):
    # class LogNN global vars
    n_cards = 12
    n_turns = 12
    n_pos = 8
    n_players = 2
    bar_offset = 5
    alley_offset = 6
    hand_offset = 7
    number_of_choices = 34
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
        for c in self.col_map_play:
            if c != winner_color:
                for log in self.col_map_play[c]:
                    for i in self.hand_indexes:
                        del log[i]
        return

    def printout(self, winner_color):
        for color in self.col_map_play:
            print(color)
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

    def ids_to_vector(self, id_played, id_target):
        output_vector = [0]*LogNN.number_of_choices
        index = 0
        if id_played == 1:
            index = 0
        elif id_played == 3:
            index = 1
        elif id_played == 4:
            index = 2
        elif 6 <= id_played <= 12:
            index = id_played - 3
        elif id_played == 2:
            index = 9 + id_target
        elif id_played == 5:
            index = 21 + id_target

        output_vector[index] = 1
        return output_vector

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
        elif 10 <= index <= 21:
            id_played = 2
            id_target = index - 9
        elif 22 <= index <= 33:
            id_played = 5
            id_target = index - 21
        return id_played, id_target
