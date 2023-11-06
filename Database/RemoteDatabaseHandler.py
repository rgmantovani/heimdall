# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

from Database.DatabaseHandler import DatabaseHandler
from Entities.Key import Key
from Entities.User import User
from Entities.KeyWithdraw import KeyWithdraw
from icecream import ic

import logging
import mariadb
import Utils.config as config

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

class RemoteDatabaseHandler(DatabaseHandler):

    # ---------------------------
    # constructor
    # --------------------------- 

    def __init__(self):

        try:
            self.dbConn = mariadb.connect(**config.DATABASE)
            self.db = self.dbConn.cursor()
            config.WITHDRAW_ID = 0
        except Exception as err:
            logging.debug(err)
            
        
        # ----------------
        # for debugging
        # ---------------
        #user = User(name="Rafael", surname="Mantovani", code="02120186", 
        #            role="professor", course="Eng. Computação")
        #query = self.searchUserByCode(userCode=user.getCode())
        #if(query == []):
        #    self.insertNewUser(newUser=user)

    # ---------------------------
    # destructor
    # ---------------------------
    def __del__(self):
        logging.debug("Encerrando conexão com o Banco de Dados.")
        self.db.close()
        self.dbConn.close()   
    
    # ---------------------------
    # search an user
    # --------------------------- 

    def searchUserByCode(self, userCode):
        code = (str(userCode),)
        self.db.execute("SELECT * FROM users WHERE code=?", code)
        dbSearch = self.db.fetchone()
        if dbSearch == None:
            return []
        else:
            return dbSearch

    # ---------------------------
    # ---------------------------

    def searchKeyByCode(self, keyCode):
        key = (str(keyCode),)
        self.db.execute("SELECT * FROM roomKeys WHERE room=?", key)
        dbSearch = self.db.fetchone()
        if dbSearch == None:
            return []
        else:
            key = Key(dbSearch[0])
            key.available = dbSearch[1]
            return [key]

    # ---------------------------
    # ---------------------------

    def searchWithdrawsByUsercode(self, userCode, status="all"):

        returnedWithdraws = []
        userCode = (str(userCode),)   
        match status:
            case "opened":
                self.db.execute("SELECT * FROM withdraws WHERE (userCode=?) AND (finalTime IS NULL)", userCode)
                dbSearch = self.db.fetchall()
            case "finished":
                self.db.execute("SELECT * FROM withdraws WHERE (userCode=?) AND (finalTime IS NOT NULL)", userCode)
                dbSearch = self.db.fetchall()
            case "all":
                self.db.execute("SELECT * FROM withdraws")
                dbSearch = self.db.fetchall()
                
        for i in range(len(dbSearch)):
            witd = KeyWithdraw(dbSearch[i][1], dbSearch[i][2])
            witd.setInitialTime(dbSearch[i][3])
            witd.setFinalTime(dbSearch[i][4])
            returnedWithdraws.append(witd)
 
        return (returnedWithdraws) 

    # ---------------------------
    # ---------------------------

    def searchWithdrawsByKeycode(self, keyCode, listOfWithdraws=None, status="all"):
        
        returnedWithdraws = []
        keyCode = (str(keyCode),)   
        match status:
            case "opened":
                self.db.execute("SELECT * FROM withdraws WHERE (keyCode=?) AND (finalTime IS NULL)", keyCode)
                dbSearch = self.db.fetchall()
            case "finished":
                self.db.execute("SELECT * FROM withdraws WHERE (keyCode=?) AND (finalTime IS NOT NULL)", keyCode)
                dbSearch = self.db.fetchall()
            case "all":
                self.db.execute("SELECT * FROM withdraws")
                dbSearch = self.db.fetchall()
                
        for i in range(len(dbSearch)):
            witd = KeyWithdraw(dbSearch[i][1], dbSearch[i][2])
            witd.setInitialTime(dbSearch[i][3])
            witd.setFinalTime(dbSearch[i][4])
            returnedWithdraws.append(witd)
 
        return (returnedWithdraws)

    # ---------------------------
    # ---------------------------

    def searchWithdrawsByStatus(self, status="all"):
        
        returnedWithdraws = []  
        match status:
            case "opened":
                self.db.execute("SELECT * FROM withdraws WHERE finalTime IS NULL")
                dbSearch = self.db.fetchall()
            case "finished":
                self.db.execute("SELECT * FROM withdraws WHERE finalTime IS NOT NULL")
                dbSearch = self.db.fetchall()
            case "all":
                self.db.execute("SELECT * FROM withdraws")
                dbSearch = self.db.fetchall()
                
        for i in range(len(dbSearch)):
            witd = KeyWithdraw(dbSearch[i][1], dbSearch[i][2])
            witd.setInitialTime(dbSearch[i][3])
            witd.setFinalTime(dbSearch[i][4])
            returnedWithdraws.append(witd)
 
        return (returnedWithdraws) 

    # ---------------------------
    # ---------------------------

    def insertNewUser(self, newUser):
        usr = User()
        usr = newUser
        self.db.execute("INSERT INTO users(name, surname, code, photo, role, course) VALUES (?, ?, ?, ?, ?, ?)",
                   (usr.getName(), usr.getSurname(), usr.getCode(), usr.getPhoto(), usr.getRole(), usr.getCourse()))
        self.dbConn.commit()

    # ---------------------------
    # ---------------------------

    def removeAnUser(self, userCode):       
        code = (str(userCode),)
        self.db.execute("DELETE FROM users WHERE code=?", code)
        self.dbConn.commit()

    # ---------------------------
    # ---------------------------

    def insertNewKey(self, newKey):
        key = (str(newKey),)
        self.db.execute("INSERT INTO roomKeys(room, isAvailable) VALUES (?, True)", key)
        self.dbConn.commit() 

    # ---------------------------
    # ---------------------------

    def withdrawKey(self, keyCode, userCode):
        operation = KeyWithdraw(userCode=userCode, keyCode=keyCode)
        self.db.execute("INSERT INTO withdraws(userCode, keyCode, initialTime) VALUES (?, ?, ?)",
                   (operation.getUserCode(), operation.getKeyCode(), operation.initialTime))
        keyCode = (str(keyCode),)
        self.db.execute("UPDATE roomKeys SET isAvailable=0 WHERE room=?", keyCode)
        self.dbConn.commit()

    # ---------------------------
    # ---------------------------

    def returnKey(self, userCode, keyCode=None):
        finalTime = KeyWithdraw(0, 0)
        finalTime.finishWithdraw()
        finalTime = finalTime.getFinalTime()
        self.db.execute("UPDATE roomKeys SET isAvailable=1 WHERE room=?", (str(keyCode),))
        self.db.execute("UPDATE withdraws SET finalTime=? WHERE (userCode=?) AND (keyCode=?) AND (finalTime IS NULL)",
                        (finalTime, userCode, keyCode))
        self.dbConn.commit() 

    # ---------------------------
    # ---------------------------        
 
    def listAllKeys(self, status="all"):
        self.db.execute("SELECT * FROM roomKeys")
        print(*self.db.fetchall(), sep='\n')

    # ---------------------------
    # ---------------------------        
 
    def listAllUsers(self):
        self.db.execute("SELECT * FROM users")
        print(*self.db.fetchall(), sep='\n')        
 
    # ---------------------------
    # --------------------------- 

    def listAllWithdraws(self, status="all"):
        self.db.execute("SELECT * FROM withdraws")
        print(*self.db.fetchall(), sep='\n') 

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------