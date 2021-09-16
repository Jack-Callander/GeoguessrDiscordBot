class Player:

    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, Player):
            return False
        return self.id == other.id
