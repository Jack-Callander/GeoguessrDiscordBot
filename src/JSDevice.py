from abc import ABC, abstractmethod

class JSDevice(ABC):

    @abstractmethod
    def fetch_html(url: str) -> str:
        """Fetches the HTML data from the given webpage."""
        pass
