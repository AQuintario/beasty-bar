import random

"""Tests for the skunk"""
"""
def remove_n_highest(lst, n):
    for _ in range(n):
        m = max(lst)
        if m == 1:
            lc = []
            lc[:] = (i for i in lst if i != 1)
            if len(lc):
                m = max(lc)
            else:
                return
        lst[:] = (x for x in lst if x != m)

def determine_who_dies(lst, n):
    death_list = []
    death_list[:] = lst
    death_list = list(set(death_list))
    death_list.sort(reverse=True)
    death_list.remove(1)
    death_list = death_list[:2]
    return death_list


for i in range(20):
    n = random.randint(0, 4)
    print(i, n)
    l = []
    for _ in range(n):
        l.append(random.randint(0, 3))
    l.append(1)
    print("Original:", l)
#    remove_n_highest(l, 2)
    d = determine_who_dies(l ,2)
#    print("2Removed:", l)
    print("Dead:    ", d)
    print("")
"""
"""Tests for the skunk"""





"""Tests for Card class"""
class Card(object):
    def __init__(self, id, color):
        self.id = id
        self.color = color
        self.name = self.card_names[self.id]

    card_names = {1: "Skunk", 2: "Parrot", 3: "Kangaroo", 4: "Monkey",
                  5: "Chameleon", 6: "Seal", 7: "Zebra", 8: "Jiraffe",
                  9: "Snake", 10: "Crocodile", 11: "Hippo", 12: "Lion"}

    def __eq__(self, other):
        return self.id == other.id

    def __gt__(self, other):
        return self.id > other.id

    def __repr__(self):
        return "%s %s (%d)" % (self.color, self.name, self.id)

    def __hash__(self):
        return self.id

class Skunk(Card):
    def __init__(self, color):
        self.id = 1
        self.name = "Skunk"
        self.color = color
#        super(Skunk, self).__init__(id, color)

    def instant_action(self, queue, alley):
        queue_ids = []
        queue_ids[:] = (c.id for c in queue)
        ids_to_kill = self.get_n_highest(queue_ids, 2)
        cards_to_kill = []
        cards_to_kill[:] = (c for c in queue if c.id in ids_to_kill)

        alley.extend(cards_to_kill)
        queue[:] = (c for c in queue if c not in cards_to_kill)

    def get_n_highest(self, lst, n):
        l = []
        l[:] = lst
        l = list(set(l))
        l.sort(reverse=True)
        l.remove(self.id)
        l = l[:n]
        return l

"""
gl = Card(12, "green")
bm = Card(4, "blue")
gm = Card(4, "green")
gs = Skunk("green")
lst = []
lst.append(bm)
lst.append(gl)
lst.append(gm)
lst.append(gs)
"""

"""print(gl, bm)
print(bm < gl)
print(bm < gm)
print(bm == gm)

print(lst)
lst.sort(reverse=True)
print(lst)

lst = list(set(lst))
print(lst)
lst.remove(bm)
print(lst)
"""
"""
print("")
ids_to_kill = [12, 4]
def to_save(c): return c.id not in ids_to_kill
print(lst)
queue = list(filter(to_save, lst))
print(queue)
"""

"""
alley = []
print(lst, alley)
gs.instant_action(lst, alley)
print(lst, alley)
"""

"""Tests for Card class"""



"""Tests for chameleon"""

"""
class Parent(object):
    def __init__(self):
        self.someattr = 10

    def do_A_thing(self):
        """"""

class ChildA(Parent):
    def __init__(self):
        Parent.__init__(self)
        print("Im a big girl")

    def do_A_thing(self):
        self.someattr += 1
        print("I believe I can fly", self.someattr)

class ChildB(Parent):
    def __init__(self):
        Parent.__init__(self)
        print("Im a copypcat")

    def do_copycat(self):
        print("I can do that too")
        print("First", self.someattr)
        ChildA.do_A_thing(self)

parent = Parent()
print(parent.someattr)
childa = ChildA()
childb = ChildB()
childa.do_A_thing()
# ChildA.do_A_thing(childb)
childb.do_copycat()
print(childb.someattr)
"""

"""Tests for chameleon"""





"""Test for seal"""
gl = Card(12, "green")
bm = Card(4, "blue")
gm = Card(4, "green")
gs = Skunk("green")
lst = []
lst.append(bm)
lst.append(gl)
lst.append(gm)
lst.append(gs)

print(lst)
print(lst.index(bm))
lst.reverse()
print(lst)
print(lst.index(bm))

li = [5, 7, 8, 0, 2]
print(li, "   ", li.index(0))
li.reverse()
print(li, "   ", li.index(0))


"""Test for seal"""