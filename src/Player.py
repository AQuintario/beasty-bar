class Player(Game):
    def __init__(self, color):
        self.color = color
        self.deck = []
        self.hand = []
        populate_deck()

    def populate_deck(self):
