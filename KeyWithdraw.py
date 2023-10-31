# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

import config
import time
from datetime import datetime

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

class KeyWithdraw:
    
    # ---------------------------
    # constructor
    # ---------------------------

    def __init__(self, userCode, keyCode, finalTime = None):
        
        self.id = config.WITHDRAW_ID
        config.WITHDRAW_ID = config.WITHDRAW_ID + 1
       
        self.setUserCode(userCode)
        self.setKeyCode(keyCode)
       
        timestamp = time.time()
        date_time = datetime.fromtimestamp(timestamp)
        self.setInitialTime(date_time.strftime("%d-%m-%Y, %H:%M:%S"))
                
    # ---------------------------
    # to string
    # ---------------------------
        
    def __str__(self):
        return(str(self.__dict__))
        
    # ---------------------------
    # finish the key Withdraw
    # ---------------------------

    def finishWithdraw(self):
        timestamp = time.time()
        date_time = datetime.fromtimestamp(timestamp)
        self.setFinalTime = date_time.strftime("%d-%m-%Y, %H:%M:%S")

    # ---------------------------
    # ---------------------------
    
    def setInitialTime(self, initialTime):
        self.setInitialTime = initialTime

    # ---------------------------
    # ---------------------------

    def setUserCode(self, userCode):
        self.userCode = userCode
    
    # ---------------------------
    # ---------------------------
    
    def getUserCode(self):
        return (self.userCode)
     
    # ---------------------------
    # ---------------------------
   
    def setKeyCode(self, keyCode):
        self.keyCode = keyCode
     
    # ---------------------------
    # ---------------------------
   
    def getKeyCode(self):
        return (self.keyCode)
    
# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------