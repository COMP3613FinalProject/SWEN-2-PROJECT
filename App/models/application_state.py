from abc import ABC, abstractmethod

class ApplicationState(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def next(self,application):
        pass

    @abstractmethod
    def previous(self,application):
        pass

    @abstractmethod
    def withdraw(self,application):
        pass

    def getStateName(self):
        return self.name

    @abstractmethod
    def getMatchedCompanies(self,application):
        pass