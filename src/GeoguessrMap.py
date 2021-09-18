from bs4 import BeautifulSoup

class GeoguessrMap:

    def __init__(self, device, code: str, db):
        self.__device = device
        self.__code = code
        self.__URL_PREFIX = 'https://www.geoguessr.com/maps/'
        self.__MAP_NAME_H1_CLASS = 'map-block__title'
        
        name = None
        if code in db.map_names:
            name = db.map_names[code]
        else:
            name = self.__fetch_name()
            db.map_names[code] = name
            db.save()
        
        self.__name = name
    
    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, GeoguessrMap):
            return False
        return self.__code == other.__code
    
    def __lt__(self, other):
        if self is other:
            return False
        if not isinstance(other, GeoguessrMap):
            raise Exception("Cannot compare GeoguessrMap type to other type")
        # TODO compare the maps name
        return self.__code < other.__code
    
    def __str__(self) -> str:
        return self.__name
    
    def __fetch_name(self):
        try:
            html = self.__device.fetch_html(self.__URL_PREFIX + self.__code)
        except:
            raise Exception("Failed to connect to Map Link.")
        else:
            soup = BeautifulSoup(html, 'html.parser')
            h1_map_name = soup.find('h1', {'class': self.__MAP_NAME_H1_CLASS})
            return h1_map_name.text
            
    
    def get_print(self) -> str:
        return str(self)

    @property
    def code(self):
        return self.__code

    @property
    def name(self):
        return self.__name
        pass

    @property
    def author(self):
        # TODO
        pass
