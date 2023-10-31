# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

import logging
from User import *
from config import *
from Key import *

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

class HeimdalSystem:
    
    listOfUsers = list()
    listOfKeys  = list()
    # TODO: list of KeyWithdraw
    
    # ---------------------------
    # constructor
    # ---------------------------
    def __init__(self):   
        # initialize keys
        for value in KEYS:
            newKey = Key(room = value)
            self.listOfKeys.append(newKey)
                        
    # ---------------------------
    #  Text menu
    # ---------------------------
    def menu(self):
        print("#############")
        print("1 - Add new user")
        print("2 - Remove user")
        print("3 - Get a key")
        print("4 - Return a key")
        print("5 - Show users")
        print("6 - Show keys")
        print("7 - Exit the program")    
        print("#############")
    
        option = input(" ** Choose an option ** ")
        return(option)
   
    # ---------------------------
    # ---------------------------         
    def readBarcodeOnce(self):
        try:
            barcode_input = input("Scan the code: ")           
            print(barcode_input)
        except KeyboardInterrupt:
            logging.debug('Keyboard interrupt')
        except Exception as err:
            logging.error(err)
        return (barcode_input)
    
    # ---------------------------
    # ---------------------------     
    def addUser(self):
       
        user = User()
        try:
            user.setName(input("Digite o nome: "))
            user.setRole(input("Digite o papel: "))
        except KeyboardInterrupt:
            logging.debug('Keyboard interrupt')
        except Exception as err:
            logging.error(err)
        
        userCode = self.readBarcodeOnce()
        user.setCode(userCode)
        print(user) 
       
        # cannot add an existing user
        query = [item for item in self.listOfUsers if item.getCode() == userCode]
        if(query == []):
            logging.debug("Adding a new user")
            self.listOfUsers.append(user)
        else:
            logging.warning("An user already exists with this code. Not adding!")
   
    # ---------------------------
    # ---------------------------        
    def printListOfUsers(self):
        for user in self.listOfUsers:
            print (user)
             
    # ---------------------------
    # ---------------------------        
    def printListOfKeys(self):
        for key in self.listOfKeys:
            print (key)
            
    # ---------------------------
    # ---------------------------     
  
    def run(self):
        while True:
            try:
                option = self.menu()
            except KeyboardInterrupt:
                logging.debug('Keyboard interrupt')
            except Exception as err:
                logging.error(err)
            
            print("Opção Selecionada = ", option)
            match option:
                case "1": 
                    logging.debug("Adding a new user")
                    self.addUser()
                case "2": 
                    logging.debug("Removing an user")
                case "3":
                    logging.debug("Get a key")
                case "4":
                    logging.debug("Returning a Key")
                case '5':
                    logging.debug("Printing all the saved users")
                    self.printListOfUsers()
                case '6':
                    logging.debug("Printing all the keys")
                    self.printListOfKeys()
                case "7":
                    logging.debug("Done :)")
                    exit()

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------