class Table(object):

    max_num_cards_in_queue = 5

    def __init__(self):
        self.queue = []
        self.bar = []
        self.alley = []

    def resolve_queue(self):
        if len(self.queue) == Table.max_num_cards_in_queue:
            self.alley.append(self.queue.pop())
            self.bar.append(self.queue.pop(0))
            self.bar.append(self.queue.pop(0))

    def determine_winner(self):
        blue_points = sum(1 for c in self.bar if c.color == 'Blue')
        green_points = sum(1 for c in self.bar if c.color == 'Green')
        if green_points == blue_points:
            winner_color = 'Draw'
        elif green_points > blue_points:
            winner_color = "Green"
        else:
            winner_color = "Blue"
        return winner_color
