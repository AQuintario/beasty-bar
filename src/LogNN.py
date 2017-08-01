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
    player_offset = 8*12  # n_pos*n_cards
    number_of_choices = 36  # 10 (normal animals) + 2 (Cham & Parrot) * 13 (animals + None)

    def __init__(self):
        self.inputs_dict = {'Blue': [], 'Green': []}   # For a single game
        self.outputs_dict = {'Blue': [], 'Green': []}
        # self.inputs = []  # For a single game, but only the winner
        # self.outputs = []
        self.X = []  # For all the games
        self.Y = []

    def read_table(self, table, player):
        pc = player.color
        table_status = [0] * (LogNN.n_cards*(LogNN.n_pos + (LogNN.n_players - 1)*(LogNN.n_pos - 1)))
        for o in range(len(table.queue)):
            i = table.queue[o].id
            c = table.queue[o].color
            if c == pc:
                player_offset = 0
                n_pos = LogNN.n_pos
            else:
                player_offset = LogNN.player_offset
                n_pos = LogNN.n_pos - 1
            pos = n_pos * (i - 1) + player_offset + LogNN.queue_offset + o
            table_status[pos] = 1
        for card in table.bar:
            i = card.id
            c = card.color
            if c == pc:
                player_offset = 0
                n_pos = LogNN.n_pos
            else:
                player_offset = LogNN.player_offset
                n_pos = LogNN.n_pos - 1
            pos = n_pos * (i - 1) + player_offset + LogNN.bar_offset
            table_status[pos] = 1
        for card in table.alley:
            i = card.id
            c = card.color
            if c == pc:
                player_offset = 0
                n_pos = LogNN.n_pos
            else:
                player_offset = LogNN.player_offset
                n_pos = LogNN.n_pos - 1
            pos = n_pos * (i - 1) + player_offset + LogNN.alley_offset
            table_status[pos] = 1
        for card in player.hand:
            i = card.id
            pos = LogNN.n_pos * (i - 1) + LogNN.hand_offset
            table_status[pos] = 1
        self.inputs_dict[pc].append(table_status)
        return

    def read_choices(self, chosen_card_from_hand, chosen_target):
        pc = chosen_card_from_hand.color
        id_played = chosen_card_from_hand.id
        if chosen_target is None:
            id_target = 13
        else:
            id_target = chosen_target.id
        self.outputs_dict[pc].append(self.ids_to_vector(id_played, id_target))

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

    def reset_game_logs(self):
        self.inputs_dict = {'Blue': [], 'Green': []}  # For a single game
        self.outputs_dict = {'Blue': [], 'Green': []}
        # self.inputs = []  # For a single game, but only the winner
        # self.outputs = []

    def assemble_log(self, winner_color):
        if winner_color != 'Draw':
            self.X.extend(self.inputs_dict[winner_color])
            self.Y.extend(self.outputs_dict[winner_color])
        self.reset_game_logs()
        return

    # def return_log_game(self):
    #     return self.inputs, self.outputs

    def return_log(self):
        return self.X, self.Y

    def printout(self):
        print("  SSSSSSSSSSSSSSSSSSSSSS, PPPPPPPPPPPPPPPPPPPPPP, KKKKKKKKKKKKKKKKKKKKKK, MMMMMMMMMMMMMMMMMMMMMM, "
              "CCCCCCCCCCCCCCCCCCCCCC, SSSSSSSSSSSSSSSSSSSSSS, ZZZZZZZZZZZZZZZZZZZZZZ, GGGGGGGGGGGGGGGGGGGGGG, "
              "SSSSSSSSSSSSSSSSSSSSSS, CCCCCCCCCCCCCCCCCCCCCC, HHHHHHHHHHHHHHHHHHHHHH, LLLLLLLLLLLLLLLLLLLLLL, "
              "SSSSSSSSSSSSSSSSSSS, PPPPPPPPPPPPPPPPPPP, KKKKKKKKKKKKKKKKKKK, MMMMMMMMMMMMMMMMMMM, "
              "CCCCCCCCCCCCCCCCCCC, SSSSSSSSSSSSSSSSSSS, ZZZZZZZZZZZZZZZZZZZ, GGGGGGGGGGGGGGGGGGG, "
              "SSSSSSSSSSSSSSSSSSS, CCCCCCCCCCCCCCCCCCC, HHHHHHHHHHHHHHHHHHH, LLLLLLLLLLLLLLLLLLL")
        for i in zip(self.X, self.Y):
            print(i)
        return

