class Player:

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, Player):
            return False
        return self.id == other.id
    
    def __str__(self):
        return self.name
