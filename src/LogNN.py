class LogNN(object):
    # class LogNN global vars
    n_cards = 12
    n_turns = 12
    n_pos = 8
    n_players = 2
    queue_offset = 0
    bar_offset = 5
    alley_offset = 6
    hand_offset = 7
    number_of_choices = 34
    # class LogNN global vars

    def __init__(self):
        self.hand_indexes = [LogNN.n_pos * i + LogNN.hand_offset for i in range(LogNN.n_cards)]
        self.hand_indexes.sort(reverse=True)

        # self.blue_cards
        # self.green_cards
        # self.choice
        # self.game_seen = {'Turn': self.turn, 'Player Playing': self.player_playing, 'Blue Cards': self.blue_cards,
        #                   'Choice': self.choice}
        self.game_seen = []
        self.inputs = []
        self.choices_seen = []
        self.outputs = []

    def read_table(self, table, player):
        # Read table and hands and convert to 01010100
        col_map = {"Blue": [0] * (LogNN.n_cards * LogNN.n_pos), "Green": [0] * (LogNN.n_cards * LogNN.n_pos)}
        pc = player.color
        game_seen_turn = {'PlayerPlaying': pc, 'BlueCards': col_map['Blue'],
                          'GreenCards': col_map['Green']}

        for o in range(len(table.queue)):
            i = table.queue[o].id
            c = table.queue[o].color
            pos = LogNN.n_pos * (i - 1) + LogNN.queue_offset + o
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

        self.game_seen.append(game_seen_turn)
        return

    def remove_loser(self, winner_color):
        self.game_seen[:] = (g for g in self.game_seen if g['PlayerPlaying'] == winner_color)
        self.choices_seen[:] = (g for g in self.choices_seen if g['PlayerPlaying'] == winner_color)

    def remove_hand(self, winner_color):
        for c in self.game_seen:
            for col in 'Blue', 'Green':
                if col != winner_color:
                    for i in self.hand_indexes:
                        del c[col + 'Cards'][i]
        return

    def join_cards(self, winner_color):
        inputs = []
        loser_colors = []
        loser_colors[:] = (col for col in ('Blue', 'Green') if col != winner_color)
        for c in self.game_seen:
            winner_cards = c[winner_color + 'Cards']
            loser_cards = []
            for col in loser_colors:
                loser_cards = loser_cards + c[col + 'Cards']
            inputs.append(winner_cards + loser_cards)
        return inputs

    def assemble_log(self, winner_color):
        self.remove_loser(winner_color)
        self.remove_hand(winner_color)
        self.inputs = self.join_cards(winner_color)
        self.outputs[:] = (c['Choice'] for c in self.choices_seen)

    def printout(self):
        print("  SSSSSSSSSSSSSSSSSSSSSS, PPPPPPPPPPPPPPPPPPPPPP, KKKKKKKKKKKKKKKKKKKKKK, MMMMMMMMMMMMMMMMMMMMMM, "
              "CCCCCCCCCCCCCCCCCCCCCC, SSSSSSSSSSSSSSSSSSSSSS, ZZZZZZZZZZZZZZZZZZZZZZ, GGGGGGGGGGGGGGGGGGGGGG, "
              "SSSSSSSSSSSSSSSSSSSSSS, CCCCCCCCCCCCCCCCCCCCCC, HHHHHHHHHHHHHHHHHHHHHH, LLLLLLLLLLLLLLLLLLLLLL, "
              "SSSSSSSSSSSSSSSSSSS, PPPPPPPPPPPPPPPPPPP, KKKKKKKKKKKKKKKKKKK, MMMMMMMMMMMMMMMMMMM, "
              "CCCCCCCCCCCCCCCCCCC, SSSSSSSSSSSSSSSSSSS, ZZZZZZZZZZZZZZZZZZZ, GGGGGGGGGGGGGGGGGGG, "
              "SSSSSSSSSSSSSSSSSSS, CCCCCCCCCCCCCCCCCCC, HHHHHHHHHHHHHHHHHHH, LLLLLLLLLLLLLLLLLLL")
        for i in zip(self.inputs, self.outputs):
            print(i)
        return

    def read_choices(self, chosen_card_from_hand, chosen_target):
        col = chosen_card_from_hand.color
        id_played = chosen_card_from_hand.id
        if chosen_target is None:
            id_target = None
        else:
            id_target = chosen_target.id
        choice_turn = {'PlayerPlaying': col, 'Choice': self.ids_to_vector(id_played, id_target)}
        self.choices_seen.append(choice_turn)

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
