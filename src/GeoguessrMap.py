class GeoguessrMap:

    def __init__(self, device, code: str):
        self.__device = device
        self.__code = code
    
    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, GeoguessrMap):
            return False
        return self.__code == other.__code

    @property
    def name(self):
        # TODO
        pass

    @property
    def author(self):
        # TODO
        pass
