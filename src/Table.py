class Table(object):
    queue = []
    bar = []
    alley = []
    max_num_cards_in_queue = 5

    def resolve_queue(self):
        if len(self.queue) == 5:
            self.alley.append(self.queue.pop())
            self.bar.append(self.queue.pop(0))
            self.bar.append(self.queue.pop(0))
