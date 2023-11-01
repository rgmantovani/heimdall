# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

# python abstract class representation 
from DatabaseHandler import *
import config
import pickle
import os
import logging

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

class FileDatabaseHandler(DatabaseHandler):

    # ---------------------------
    # constructor
    # --------------------------- 

    def __init__(self, filepath=None):

        #create a binary file using pickle (filepath) / restoring existing values
        self.datafile = "filedatabase.db"
        if os.path.exists(self.datafile):
            print(" - reading an existing file")
            with open(self.datafile, 'rb') as pickled_file:
                self.listOfUsers     = pickle.load(pickled_file)
                self.listOfKeys      = pickle.load(pickled_file)
                self.listOfWithdraws = pickle.load(pickled_file)
                # countinously couting the withdraws
                config.WITHDRAW_ID = len(self.listOfWithdraws) + 1
        else:
            self.listOfUsers     = list()
            self.listOfKeys      = list()
            self.listOfWithdraws = list()
            # starting the counting of withdraws
            config.WITHDRAW_ID = 1
        
            # initialize all keys as available (othersiwe it already exists)
            for value in config.KEYS:
                newKey = Key(room=value)
                self.insertNewKey(newKey)
            
        # ----------------
        # for debugging
        # ---------------
        user = User(name="Rafael", surname="Mantovani", code="02120186", 
                    role="professor", course="Eng. Computação")
        query = self.searchUserByCode(userCode=user.getCode())
        if(query == []):
            self.insertNewUser(newUser=user)

    # ---------------------------
    # destructor
    # ---------------------------
    def __del__(self):
        logging.debug("Exportando os dados no arquivo de dados.")
        with open(self.datafile, 'wb') as pickled_file:
            pickle.dump(self.listOfUsers, pickled_file)
            pickle.dump(self.listOfKeys, pickled_file)
            pickle.dump(self.listOfWithdraws, pickled_file)

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
        # TODO: add exception if an invalid option is choosen
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

    def searchWithdrawsByKeycode(self, keyCode, listOfWithdraws, status="all"):
        # status = {opened, finished, all}
        # TODO: add exception if an invalid option is choosed
        returnedWithdraws = []     
        if(status == "opened"):
            returnedWithdraws = [witd for witd in listOfWithdraws 
                                 if witd.getKeyCode() == keyCode 
                                 and witd.getFinalTime() == None]
        elif(status == "finished"):
            returnedWithdraws = [witd for witd in listOfWithdraws 
                                 if witd.getKeyCode() == keyCode 
                                 and witd.getFinalTime() != None]
        else:
            returnedWithdraws = [witd for witd in listOfWithdraws 
                                 if witd.getKeyCode() == keyCode]
        return (returnedWithdraws) 

    # ---------------------------
    # ---------------------------

    def searchWithdrawsByStatus(self, status="all"):
        # status = {opened, finished, all}
        # TODO: add exception if an invalid option is choosen
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

    def removeAnUser(self, userCode):
       
        index = []
        #TODO: improve this
        for i in range(0, len(self.listOfUsers)):
            user = self.listOfUsers[i]
            if user.getCode() == userCode:
                index = i
        self.listOfUsers.pop(index)

    # ---------------------------
    # ---------------------------

    def insertNewKey(self, newKey):
        self.listOfKeys.append(newKey) 

    # ---------------------------
    # ---------------------------

    def withdrawKey(self, keyCode, userCode):
        operation = KeyWithdraw(userCode=userCode, keyCode=keyCode)
        self.listOfWithdraws.append(operation) 

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