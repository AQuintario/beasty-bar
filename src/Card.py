# import Game

class Card(object):

    def __init__(self, id, color):
        self.id = id
        self.color = color
        self.is_recurrent = False
        if self.id == 8 or self.id == 10 or self.id == 11:
            self.is_recurrent = True
        self.name = self.card_names[self.id]

    def __eq__(self, other):
        return self.id == other.id and self.color == other.color

    def __gt__(self, other):
        return self.id > other.id

    def __lt__(self, other):
        return self.id < other.id

    def __repr__(self):
        return "%s %s (%d)" % (self.color, self.name, self.id)

    def __hash__(self):
        return self.id

    card_names = {1: "Skunk", 2: "Parrot", 3: "Kangaroo", 4: "Monkey",
                  5: "Chameleon", 6: "Seal", 7: "Zebra", 8: "Giraffe",
                  9: "Snake", 10: "Crocodile", 11: "Hippo", 12: "Lion"}

    def index_in_queue(self, table):
        index = 0
        for i in table.queue:
            if i.id == self.id and i.color == self.color:
                return index
            index += 1

class Skunk(Card):
    def __init__(self, color):
        # Card.__init__(self, id = 1, color, recurrent  = "False")
        self.id = 1
        self.name = "Skunk"
        self.color = color
#        super(Skunk, self).__init__(id, color)

    def instant_action(self, table):
        queue_ids = []
        queue_ids[:] = (c.id for c in table.queue)
        ids_to_kill = self.get_n_highest(queue_ids, 2)
        cards_to_kill = []
        cards_to_kill[:] = (c for c in queue if c.id in ids_to_kill)
        Game.move_from_queue_to_alley(table, cards_to_kill)
        return

    def get_n_highest(self, lst, n):
        l = []
        l[:] = lst
        l = list(set(l))
        l.sort(reverse=True)
        l.remove(self.id)
        l = l[:n]
        return l

class Parrot(Card):
    def __init__(self, color):
        self.id = 2
        self.name = "Parrot"
        self.color = color
        # super(Skunk, self).__init__()

    def instant_action(self, table, target_card):
        Game.move_from_queue_to_alley(table, target_card)
        return

class Kangaroo(Card):
    def __init__(self, color):
        self.id = 3
        self.name = "Kangaroo"
        self.color = color

    def instant_action(self, table, n = 2):
        # Assuming it is already at the end of the queue
        i = self.index_in_queue(table)
        # Throw an exception if i != len(queue) would be nice
        for _ in range(n):
            if i > 0:
                Game.swap(table, i, i-1)
        return

class Monkey(Card):
    def __init__(self, color):
        self.id = 4
        self.name = "Monkey"
        self.color = color

    def instant_action(self, table):
        queue_ids = []
        queue_ids[:] = (c.id for c in table.queue)
        n_monkeys = queue_ids.count(self.id)
        if n_monkeys > 1:
            # Kill hippos and crocs
            hippos = []
            hippos[:] = (c for c in table.queue if c.id == 11)
            crocs = []
            crocs[:] = (c for c in table.queue if c.id == 10)
            Game.move_from_queue_to_alley(table, hippos)
            Game.move_from_queue_to_alley(table, crocs)
            # Move to the front
            sub_monkeys = []
            sub_monkeys[:] = (c for c in table.queue if c.id == self.id)
            table.queue[:] = (c for c in table.queue if c.id != self.id)
            sub_monkeys.reverse()
            table.queue = sub_monkeys + table.queue
        return

class Chameleon(Card):
    def __init__(self, color):
        self.id = 5
        self.name = "Chameleon"
        self.color = color

    def instant_action(self, table):
        """Ni idea"""

class Seal(Card):
    def __init__(self, color):
        self.id = 6
        self.name = "Seal"
        self.color = color

    def instant_action(self, table):
        table.queue.reverse()
        return

class Zebra(Card):
    def __init__(self, color):
        self.id = 7
        self.name = "Zebra"
        self.color = color

class Giraffe(Card):
    def __init__(self, color):
        self.id = 8
        self.name = "Giraffe"
        self.color = color
        self.recurrent = True

    def instant_action(self, table):
        table.queue.reverse()

class Snake(Card):
    def __init__(self):
        self.id = 9
        super(Snake, self).__init__()

    def instant_action(self, table):
        self.sort_descending(table)

    def sort_descending(self, table):
        table.queue.sort(reverse=True)

class Crocodile(Card):
    def __init__(self, color):
        self.id = 10
        self.name = "Crocodile"
        self.color = color
        self.recurrent = True

    def instant_action(self, table):
        i = self.index_in_queue(table)
        id_in_front = table.queue[i-1].id
        cards_to_kill = []
        while i != 0 and id_in_front < self.id and id_in_front != Zebra.id:
            cards_to_kill.append(table.queue[i-1])
            Game.swap(table, i, i - 1)
            i = self.index_in_queue(table)
            id_in_front = table.queue[i-1].id
        Game.move_from_queue_to_alley(table, cards_to_kill)
        return


class Hippo(Card):
    def __init__(self, color):
        self.id = 11
        self.name = "Hippo"
        self.color = color
        self.recurrent = True

    def instant_action(self, table):
        i = self.index_in_queue(table)
        id_in_front = table.queue[i - 1].id
        while i != 0 and id_in_front < self.id and id_in_front != Zebra.id:
            Game.swap(table, i, i - 1)
            i = self.index_in_queue(table)
            id_in_front = table.queue[i - 1].id
        return

class Lion(Card):
    def __init__(self, color):
        self.id = 12
        self.name = "Lion"
        self.color = color

    def instant_action(self, table):
        queue_ids = []
        queue_ids[:] = (c.id for c in table.queue)
        if queue_ids.count(self.id) > 1:
            Game.move_from_queue_to_alley(table, self)
        else:
            # Get first
            i = self.index_in_queue(table)
            while i:
                Game.swap(table, i, i-1)
            # Kill Monkeys
            sub_monkeys = []
            sub_monkeys[:] = (c for c in table.queue if c.id == Monkey.id)
            Game.move_from_queue_to_alley(table, sub_monkeys)
        return
