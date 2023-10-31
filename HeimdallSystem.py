# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

import logging
import config

from User import *
from Key import *
from KeyWithdraw import *

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

class HeimdalSystem:
    
    listOfUsers     = list()
    listOfKeys      = list()
    listOfWithdraws = list()
    
    # ---------------------------
    # constructor
    # ---------------------------
    def __init__(self):   
        # initialize keys
        for value in config.KEYS:
            newKey = Key(room = value)
            self.listOfKeys.append(newKey)
            
        #for debugging
        user = User(name="Rafael", code="02120186", role="professor")
        self.listOfUsers.append(user)
                        
    # ---------------------------
    #  Text menu
    # ---------------------------
    def menu(self):
        print("#############")
        print("1 - Adicionar um novo usuário")
        print("2 - Remover um usuário")
        print("3 - Retirar uma chave")
        print("4 - Retornar uma chave")
        print("5 - Mostrar usuários cadastrados")
        print("6 - Mostrar chaves cadastradas")
        print("7 - Mostrar histórico de retirada de chaves") 
        print("8 - Encerrar o programa")    
        print("#############")
    
        option = input(" ** Escolha uma opção ** \n")
        return(option)
   
    # ---------------------------
    # ---------------------------         
    def readBarcodeOnce(self):
        try:
            barcode_input = input("Escaneie o código: ")           
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
            logging.debug("Adicionando um novo usuário.")
            self.listOfUsers.append(user)
        else:
            logging.warning("Já existe um usuário com esse código. Operação não realizada!")
   
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
    def printListOfWithdraws(self):
        for wtd in self.listOfWithdraws:
            print (wtd)

    # ---------------------------
    # TODO 
    # --------------------------- 

    # search a key
    # search an user
    # search a withdraw
    
    # ---------------------------
    # --------------------------- 
    def returningKey(self):    
        
        # scan code
        userCode = self.readBarcodeOnce()
        
        # only valid users can handle keys
        userQuery = [user for user in self.listOfUsers if user.getCode() == userCode]
        if(userQuery == []):
            logging.warning('Não existe usuário cadastrado com esse código. Por favor, cadastre antes!')
        else :
            # find the withdraw with the userCode
            withQuery = [request for request in self.listOfWithdraws if request.getUserCode() == userCode]
            if(withQuery == []):
                logging.warning("Não foi feita nenhuma retirada pelo usuário.")
            
            elif(len(withQuery) == 1):
                logging.info("Existe uma única retirada realizada pelo usuário.")
                print(withQuery[0])
                withQuery[0].finishWithdraw()
              
                # make the key available
                keyQuery = [key for key in self.listOfKeys if key.getRoom() == withQuery[0].getKeyCode()]
                keyQuery[0].returnedKey()                    
                logging.info("A chave {} foi retornada com sucesso.".format(retQuery[0].getRoom()))
            
            else:
                logging.warning("Existem várias retiradas realizadas pelo mesmo usuário.")
                # showing all the withdraws with the userCode value
                for operation in withQuery:
                    print(operation)
                # ask which key will be returned (include option - all, to return all of them)
                #TODO: add 'all' option
                try:
                    returnedKey = input("Qual chave gostaria de retornar ?")
                except KeyboardInterrupt:
                    logging.debug('Keyboard interrupt')
                except Exception as err:
                    logging.error(err)

                retQuery = [request for request in withQuery if request.getKeyCode() == returnedKey]
                if(retQuery == []):
                    logging.warning("A chave digitada não existe ou não foi retirada anteriormente")
                else:
                    #finish the withdraw
                    print(retQuery[0])
                    retQuery[0].finishWithdraw()
                    # make the key available
                    keyQuery = [key for key in self.listOfKeys if key.getRoom() == returnedKey]
                    keyQuery[0].returnedKey()                    
                    logging.info("A chave {} foi retornada com sucesso.".format(retQuery[0].getRoom()))
    
    # ---------------------------
    # --------------------------- 
    def withdrawingKey(self):
        
        # ask which key will be withdrawn
        try:
            withKey = input("Qual chave tirar? ")
        except KeyboardInterrupt:
            logging.debug('Keyboard interrupt')
        except Exception as err:
            logging.error(err)

        # check if the key is available
        keyQuery = [key for key in self.listOfKeys if key.getRoom() == withKey]
        
        # ver se tem chave
        if(keyQuery == []):
            logging.warning("A chave requerida não existe.!")
        elif(not keyQuery[0].isAvailable()):
            logging.warning('A chave requerida não está disponível!')
        else: 
            # only valid users can withdraw a key
            userCode = self.readBarcodeOnce()
            userQuery = [user for user in self.listOfUsers if user.getCode() == userCode]
            if(userQuery == []):
                logging.warning('Não existe usuário cadastrado com esse código. Por favor, cadastre antes!')
            else :
                operation = KeyWithdraw(userCode = userCode, keyCode = withKey)
                # key was withdrawn
                keyQuery[0].withdrawKey()
                self.listOfWithdraws.append(operation)
                logging.info("A chave {} foi retirada com sucesso.".format(keyQuery[0].getRoom()))
                print(operation)  
        
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
                case "1": self.addUser()
                case "2": 
                    logging.debug("Removing an user")
                case "3": self.withdrawingKey()
                case "4": self.returningKey()
                case '5': self.printListOfUsers()
                case '6': self.printListOfKeys()
                case '7': self.printListOfWithdraws()
                case "8": exit()

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------