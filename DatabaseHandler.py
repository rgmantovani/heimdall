# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

# python abstract class representation 
from abc import ABC, abstractmethod

from User import *
from Key import *
from KeyWithdraw import *

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

class DatabaseHandler(ABC):

    @abstractmethod
    def searchUserByCode(self, userCode):
        pass 

    @abstractmethod
    def searchKeyByCode(self, keyCode):
        pass

    @abstractmethod
    def searchWithdrawsByUsercode(self, userCode, status="all"):
        pass 

    @abstractmethod
    def searchWithdrawsByKeycode(self, keyCode, status="all"):
        pass 

    @abstractmethod
    def searchWithdrawsByStatus(self, status="all"):
        pass

    @abstractmethod
    def insertNewUser(self, newUser):
        pass 

    @abstractmethod
    def insertNewKey(self, newKey):
        pass 

    @abstractmethod
    def withdrawKey(self, keyCode, userCode):
        pass 

    @abstractmethod
    def returnKey(self, userCode, keyCode=None):
        pass 

    @abstractmethod
    def listAllKeys(self, status="all"):
        pass 

    @abstractmethod
    def listAllUsers(self):
        pass 

    @abstractmethod
    def listAllKeys(self):
        pass 

    @abstractmethod
    def listAllWithdraws(self, status="all"):
        pass

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------