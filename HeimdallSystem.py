# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

import logging
from People import *

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

class HeimdalSystem:
    
    # list of users
    users = list()
    
    # TODO: list of keys
    
    # ---------------------------
    # ---------------------------
    def __init__(self):
        pass
        
    # ---------------------------
    # ---------------------------
    def menu(self):
        print("#############")
        print("1 - Add new user")
        print("2 - Remove user")
        print("3 - Get a key")
        print("4 - Return a key")
        print("5 - Show users")
        print("6 - Exit the program")    
        print("#############")
    
        option = input("O que fazer? ")
        return(option)
   
    # ---------------------------
    # ---------------------------         
    def read_barcode_one_time(self):
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
        user = People()
        user.setName(input("Digite o nome: "))
        userCode = self.read_barcode_one_time()
        user.setCode(userCode)
        user.setRole(input("Digite o papel: "))
        print(user)
        #add user to the list of users
        self.users.append(user)

    # ---------------------------
    # ---------------------------        
    def printListOfUsers(self):
        for user in self.users:
            print (user)
             
    # ---------------------------
    # ---------------------------     
  
    def run(self):
        while True:
            option = self.menu()
            print("Opção Selecionada = ", option)
            match option:
                case "1": 
                    print("Cadastrando novo user")
                    self.addUser()
                case "2": 
                    print("Removendo user")
                case "3":
                    print("Retirar uma chave")
                case "4":
                    print("Devolver uma chave")
                case '5':
                    print("Show users")
                    self.printListOfUsers()
                case "6":
                    print("Encerrandommmm ...")
                    exit()

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------