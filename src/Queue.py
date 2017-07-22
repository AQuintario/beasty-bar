class Queue:
   
    def __init__(self):
        self.queue = []
        self.max_number = 5
   
    def instant_action(self, card_played, card_chosen):
        self.queue.append(card_played)

        if card_played.id == 9:
            self.sort_ascending()
        elif card_played.id == 2
            self.queue.remove(card_chosen)    

    def sort_ascending(self):
        self.queue.sort(key=lambda x: x.value, reverse = True)



    def show(self):
        print(*self.queue, sep='\n')




