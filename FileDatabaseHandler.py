# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

# python abstract class representation 
from DatabaseHandler import *
import config

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

class FileDatabaseHandler(DatabaseHandler):

    # ---------------------------
    # constructor
    # --------------------------- 

    def __init__(self, filepath=None):

        #TODO: create a binary file using pickle (filepath)
    
        self.listOfUsers     = list()
        self.listOfKeys      = list()
        self.listOfWithdraws = list()
        
        # initialize all keys as available
        for value in config.KEYS:
            newKey = Key(room=value)
            self.insertNewKey(newKey)
            
        #for debugging
        user = User(name="Rafael", surname="Mantovani", code="02120186", 
                    role="professor", course="Eng. Computação")
        self.listOfUsers.append(user)

    # ---------------------------
    # search an user
    # --------------------------- 

    def searchUserByCode(self, userCode):
        returnedUsers = [user for user in self.listOfUsers if user.getCode() == userCode]
        return(returnedUsers) 

    # ---------------------------
    # ---------------------------

    def searchKeyByCode(self, keyCode):
        keyQuery = [key for key in self.listOfKeys if key.getRoom() == keyCode]
        return(keyQuery)

    # ---------------------------
    # ---------------------------

    def searchWithdrawsByUsercode(self, userCode, status="all"):
        # status = {opened, finished, all}
        # TODO: add exception if an invalid option is choosed
        returnedWithdraws = []     
        if(status == "opened"):
            returnedWithdraws = [witd for witd in self.listOfWithdraws 
                                 if witd.getUserCode() == userCode 
                                 and witd.getFinalTime() == None]
        elif(status == "finished"):
            returnedWithdraws = [witd for witd in self.listOfWithdraws 
                                 if witd.getUserCode() == userCode 
                                 and witd.getFinalTime() != None]
        else:
            returnedWithdraws = [witd for witd in self.listOfWithdraws 
                                 if witd.getUserCode() == userCode]
        return (returnedWithdraws) 

    # ---------------------------
    # ---------------------------

    def searchWithdrawsByKeycode(self, keyCode, status="all"):
        # status = {opened, finished, all}
        # TODO: add exception if an invalid option is choosed
        returnedWithdraws = []     
        if(status == "opened"):
            returnedWithdraws = [witd for witd in self.listOfWithdraws 
                                 if witd.getKeyCode() == keyCode 
                                 and witd.getFinalTime() == None]
        elif(status == "finished"):
            returnedWithdraws = [witd for witd in self.listOfWithdraws 
                                 if witd.getKeyCode() == keyCode 
                                 and witd.getFinalTime() != None]
        else:
            returnedWithdraws = [witd for witd in self.listOfWithdraws 
                                 if witd.getKeyCode() == keyCode]
        return (returnedWithdraws) 

    # ---------------------------
    # ---------------------------

    def searchWithdrawsByStatus(self, status="all"):
        # status = {opened, finished, all}
        # TODO: add exception if an invalid option is choosed
        returnedWithdraws = []     
        if(status == "opened"):
            returnedWithdraws = [witd for witd in self.listOfWithdraws 
                                 if witd.getFinalTime() == None]
        elif(status == "finished"):
            returnedWithdraws = [witd for witd in self.listOfWithdraws 
                                 if witd.getFinalTime() != None]
        else:
            returnedWithdraws = self.listOfWithdraws 
        return (returnedWithdraws) 

    # ---------------------------
    # ---------------------------

    def insertNewUser(self, newUser):
        self.listOfUsers.append(newUser) 

    # ---------------------------
    # ---------------------------

    def insertNewKey(self, newKey):
        self.listOfKeys.append(newKey) 

    # ---------------------------
    # ---------------------------

    def withdrawKey(self, keyCode, userCode):
        pass 

    # ---------------------------
    # ---------------------------

    def returnKey(self, userCode, keyCode=None):
        pass 

    # ---------------------------
    # ---------------------------        
 
    def listAllKeys(self, status="all"):
        for key in self.listOfKeys:
            print (key) 

    # ---------------------------
    # ---------------------------        
 
    def listAllUsers(self):
        for user in self.listOfUsers:
            print (user) 
 
    # ---------------------------
    # --------------------------- 

    def listAllWithdraws(self, status="all"):
        for wtd in self.listOfWithdraws:
            print (wtd)

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------