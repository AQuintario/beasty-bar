class Table:
   
    def __init__(self):
        self.queue = []
        self.queue_id = []
        self.max_number_in_queue = 5
        self.alley = []
        self.bar = []
   


    def show(self):
        print(*self.queue, sep='\n')




