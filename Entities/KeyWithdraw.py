# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

import Utils.config as config
import time
from datetime import datetime

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

class KeyWithdraw:
    
    # ---------------------------
    # constructor
    # ---------------------------

    def __init__(self, userCode, keyCode):
        
        self.id = config.WITHDRAW_ID
        config.WITHDRAW_ID = config.WITHDRAW_ID + 1
       
        self.setUserCode(userCode)
        self.setKeyCode(keyCode)
       
        timestamp = time.time()
        date_time = datetime.fromtimestamp(timestamp)
        self.setInitialTime(date_time.strftime("%d-%m-%Y, %H:%M:%S"))
        self.finalTime = None
                
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
        self.setFinalTime(date_time.strftime("%d-%m-%Y, %H:%M:%S"))

    # ---------------------------
    # ---------------------------
    
    def setInitialTime(self, initialTime):
        self.initialTime = initialTime

    # ---------------------------
    # ---------------------------
    
    def setFinalTime(self, finalTime):
        self.finalTime = finalTime

    # ---------------------------
    # ---------------------------
    
    def getFinalTime(self):
       return (self.finalTime)

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