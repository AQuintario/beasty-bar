from src.Player import Player


def move_from_queue_to_alley(table, cards_to_kill):
    if not isinstance(cards_to_kill, list):
        cards_to_kill = [cards_to_kill]
    table.alley.extend(cards_to_kill)
    table.queue[:] = (c for c in table.queue if c not in cards_to_kill)


def move_last_in_queue_to_alley(table):
    table.alley.append(table.queue.pop())


def swap(table, i, j):
    table.queue[i], table.queue[j] = table.queue[j], table.queue[i]


def sort_descending(table):
    table.queue.sort(reverse=True)


def get_n_highest_except_self(lst, n, self_id):
    l = []
    l[:] = lst
    l = list(set(l))
    l.sort(reverse=True)
    l.remove(self_id)
    l = l[:n]
    return l


def recurrent_actions(table, chosen_card_from_hand):
    for c in table.queue[:]:  # Make a copy of the queue before shaking it
        if c.is_recurrent and c != chosen_card_from_hand:
            instant_actions(table, c)


def instant_actions(table, chosen_card_from_hand, target_card=None):
    id = chosen_card_from_hand.id
    if id == 1:
        queue_ids = [c.id for c in table.queue]
        ids_to_kill = get_n_highest_except_self(queue_ids, 2, 1)
        cards_to_kill = [c for c in table.queue if c.id in ids_to_kill]
        move_from_queue_to_alley(table, cards_to_kill)
        return
    elif id == 2:
        if target_card is None:
            return
        # print("Parrot kills", target_card)
        move_from_queue_to_alley(table, target_card)
        return
    elif id == 3:
        i = chosen_card_from_hand.index_in_queue(table)
        for _ in range(2):  # For the moment, it can't jump only one animal
            if i > 0:
                swap(table, i, i-1)
                i = chosen_card_from_hand.index_in_queue(table)
        return
    elif id == 4:
        queue_ids = [c.id for c in table.queue]
        n_monkeys = queue_ids.count(4)
        if n_monkeys > 1:
            # Kill hippos and crocs
            hippos = [c for c in table.queue if c.id == 11]
            crocs = [c for c in table.queue if c.id == 10]
            move_from_queue_to_alley(table, hippos)
            move_from_queue_to_alley(table, crocs)
            # Move to the front
            sub_monkeys = [c for c in table.queue if c.id == 4]
            table.queue[:] = (c for c in table.queue if c.id != 4)
            sub_monkeys.reverse()
            table.queue = sub_monkeys + table.queue
        return
    elif id == 5:
        if target_card is None:
            return
        # print("Chameleon acts as", target_card)
        # Let's try some cheap trick
        true_color = chosen_card_from_hand.color
        chosen_card_from_hand.id = target_card.id
        chosen_card_from_hand.color = "Grey"
        instant_actions(table, chosen_card_from_hand)
        chosen_card_from_hand.id = 5
        chosen_card_from_hand.color = true_color
        return
    elif id == 6:
        table.queue.reverse()
        return
    elif id == 7:
        return
    elif id == 8:
        i = chosen_card_from_hand.index_in_queue(table)
        id_in_front = table.queue[i - 1].id
        if i > 0 and id_in_front < 8:
            swap(table, i, i - 1)
        return
    elif id == 9:
        sort_descending(table)
        return
    elif id == 10:
        i = chosen_card_from_hand.index_in_queue(table)
        id_in_front = table.queue[i-1].id
        cards_to_kill = []
        while i != 0 and id_in_front < 10 and id_in_front != 7:
            cards_to_kill.append(table.queue[i-1])
            swap(table, i, i - 1)
            i = chosen_card_from_hand.index_in_queue(table)
            id_in_front = table.queue[i-1].id
        move_from_queue_to_alley(table, cards_to_kill)
        return
    elif id == 11:
        i = chosen_card_from_hand.index_in_queue(table)
        id_in_front = table.queue[i - 1].id
        while i != 0 and id_in_front < 11 and id_in_front != 7:
            swap(table, i, i - 1)
            i = chosen_card_from_hand.index_in_queue(table)
            id_in_front = table.queue[i - 1].id
        return
    elif id == 12:
        queue_ids = [c.id for c in table.queue]
        if queue_ids.count(12) > 1:
            move_last_in_queue_to_alley(table)
            return
        else:
            # Get first
            table.queue.insert(0, table.queue.pop())
            # Kill Monkeys
            sub_monkeys = [c for c in table.queue if c.id == 4]
            move_from_queue_to_alley(table, sub_monkeys)
        return

verbose = False
verboseprint = print if verbose else lambda *a, **k: None


def play_a_turn(table, player, logNN):
    # Read table and hands and convert to 01010100
    logNN.read_table(table, player)

    # Phases 1 and 2: choose card from hand and target card from queue
    chosen_card_from_hand, chosen_target = player.choose_cards(table)
    logNN.read_choices(chosen_card_from_hand, chosen_target)
    verboseprint("Hand:", player.hand, "Card chosen:", chosen_card_from_hand)

    # Phase 3: place selected card in queue
    table.queue.append(chosen_card_from_hand)

    # Phase 4: instant abilities
    instant_actions(table, chosen_card_from_hand, chosen_target)

    # Phase 5: recurrent abilities (starting for the nearest to the bar)
    recurrent_actions(table, chosen_card_from_hand)

    # Phase 6: resolve queue
    table.resolve_queue()
    if player.is_last():
        verboseprint("queue", table.queue)
        verboseprint("")

    # Phase 7: draw a card from deck
    player.draw_card()


def play_a_game(table, players, logNN):
    for player in players:
        player.reset()
    while Player.cards_all_players:
        for player in players:
            play_a_turn(table, player, logNN)
    winner_color = table.determine_winner()
    logNN.assemble_log(winner_color, table)
    return winner_color
