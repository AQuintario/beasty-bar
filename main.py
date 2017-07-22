import src/Queue

cards = []
queue = Queue()

for card in cards:

    cards_in_play = queue.get()
    card_hand  = hand.select_card(cards_in_play)
    card_queue = hand.get_target_card(cards_in_play)
     
    play.instant_action(card_hand, card_queue)
    play.recurrent_action(card_hand, card_queue)
    play.resolve() # Do things when Q has 5 cards

    play.print(queue)
