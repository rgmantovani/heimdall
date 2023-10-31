# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

import time
from datetime import datetime
from config import *

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

class KeyWithdraw:
    
    # ---------------------------
    # constructor
    # ---------------------------

    def __init__(self, id, userCode, keyCode):
        
        self.id = WITHDRAW_ID
        WITHDRAW_ID = WITHDRAW_ID + 1
       
        self.setUserCode(userCode)
        self.setKeyCode(keyCode)
       
        timestamp = time.time()
        date_time = datetime.fromtimestamp(timestamp)
        self.setInitialTime(date_time.strftime("%d-%m-%Y, %H:%M:%S"))
        
        self.setFinalTime(None)
        
    # ---------------------------
    # finish the key Withdraw
    # ---------------------------

    def finishWithdraw(self):
        timestamp = time.time()
        date_time = datetime.fromtimestamp(timestamp)
        self.setFinalTime(date_time.strftime("%d-%m-%Y, %H:%M:%S"))
    
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