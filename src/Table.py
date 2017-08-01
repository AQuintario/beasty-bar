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
        blue_points, green_points = 0, 0

        for c in self.bar:
            if c.color == "Green":
                green_points += 1
            if c.color == "Blue":
                blue_points += 1
        if green_points == blue_points:
            winner_color = 'Draw'
        elif green_points > blue_points:
            winner_color = "Green"
        else:
            winner_color = "Blue"
        return winner_color
