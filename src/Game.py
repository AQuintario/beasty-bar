class Game(object):
    num_cards_in_hand = 4
    num_cards_in_queue = 5

    def __init__(self):
        "holi"

    def move_from_queue_to_alley(self, table, cards_to_kill):
        table.alley.extend(cards_to_kill)
        table.queue[:] = (c for c in queue if c not in cards_to_kill)

    def move_from_queue_to_alley(self, table, card_to_kill):
        cards_to_kill = [card_to_kill]
        table.alley.extend(cards_to_kill)
        table.queue[:] = (c for c in queue if c not in cards_to_kill)

    def swap(self, table, i, j):
            table.queue[i], table.queue[j] = table.queue[j], table.queue[i]

    def get_n_highest_except_self(self, lst, n, self_id):
        l = []
        l[:] = lst
        l = list(set(l))
        l.sort(reverse=True)
        l.remove(self_id)
        l = l[:n]
        return l
