from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    @abstractmethod
    def fetch_advisories(self, *args, **kwargs):
        pass
