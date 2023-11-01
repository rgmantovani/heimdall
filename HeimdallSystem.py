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
        # initialize all available keys
        for value in config.KEYS:
            newKey = Key(room = value)
            self.listOfKeys.append(newKey)
            
        #for debugging
        user = User(name="Rafael", surname="Mantovani", code="02120186", 
                    role="professor", course="Eng.Computação")
        self.listOfUsers.append(user)
                        
    # ---------------------------
    #  Text menu
    # ---------------------------
    def menu(self):
        print("#######################################")
        print("#####     HEIMDALL KEY  KEEPER     ####")
        print("#######################################")
        
        print("1 - Adicionar um novo usuário")
        print("2 - Remover um usuário")
        print("3 - Retirar uma chave")
        print("4 - Retornar uma chave")
        print("5 - Mostrar usuários cadastrados")
        print("6 - Mostrar chaves cadastradas")
        print("7 - Mostrar histórico de retirada de chaves") 
        print("8 - Encerrar o programa")    
        print("#######################################")
    
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
            user.setSurname(input("Digite o sobrenome: "))
            user.setRole(input("Digite o papel: "))
            user.setCourse(input("Digite o curso: "))
        except KeyboardInterrupt:
            logging.debug('Keyboard interrupt')
        except Exception as err:
            logging.error(err)
        
        # reading barcode
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
    # search an user
    # --------------------------- 

    def searchUserByCode(self, userCode):
        returnedUsers = [user for user in self.listOfUsers if user.getCode() == userCode]
        return(returnedUsers)

    # ---------------------------
    # ---------------------------

    # search a key
    def searchKeyByCode(self, keyCode):
        keyQuery = [key for key in self.listOfKeys if key.getRoom() == keyCode]
        return(keyQuery)

    # ---------------------------
    # ---------------------------

    # search a withdraw
    def searchWithdraws(self, userCode, status = "all"):
   
        # opened, finished, all
        returnedWithdraws = []     
        if(status == "opened"):
            returnedWithdraws = [witd for witd in self.listOfWithdraws if witd.getUserCode() == userCode 
                        and witd.getFinalTime() == None]
        elif(status == "finished"):
            returnedWithdraws = [witd for witd in self.listOfWithdraws if witd.getUserCode() == userCode 
                        and witd.getFinalTime() != None]
        else:
            returnedWithdraws = [witd for witd in self.listOfWithdraws if witd.getUserCode() == userCode]
        return (returnedWithdraws)
    
    # ---------------------------
    # --------------------------- 
    def returningKey(self):    
        
        userCode = self.readBarcodeOnce()

        # only valid users can handle keys
        filteredUsers = self.searchUserByCode(userCode=userCode)
        if(filteredUsers == []):
            logging.warning('Não existe usuário cadastrado com esse código. Por favor, cadastre antes!')
        else :
            # find the withdraw with the userCode (only not finished withdraws)
            filteredWithdraws = self.searchWithdraws(userCode=userCode, status="opened")
            if(filteredWithdraws == []):
                logging.warning("Não foi feita nenhuma retirada pelo usuário.")
            
            elif(len(filteredWithdraws) == 1):
                logging.info("Existe uma única retirada realizada pelo usuário.")
                print(filteredWithdraws[0])
                filteredWithdraws[0].finishWithdraw()
                print(filteredWithdraws[0])
                # make the key available
                filteredKey = self.searchKeyByCode(keyCode=filteredWithdraws[0].getKeyCode()) 
                filteredKey[0].returnKey()                    
                logging.info("A chave {} foi retornada com sucesso.".format(filteredKey[0].getRoom()))
            
            else:
                logging.warning("Existem várias retiradas realizadas pelo mesmo usuário.")
                # showing all the withdraws with the userCode value
                for operation in filteredWithdraws:
                    print(operation)
                # ask which key will be returned (include option - all, to return all of them)
                #TODO: add 'all' option
                try:
                    returnedKey = input("Qual chave gostaria de retornar ?")
                    returnedKey.upper()
                except KeyboardInterrupt:
                    logging.debug('Keyboard interrupt')
                except Exception as err:
                    logging.error(err)

                retQuery = [request for request in filteredWithdraws if request.getKeyCode() == returnedKey]
                if(retQuery == []):
                    logging.warning("A chave digitada não existe ou não foi retirada anteriormente")
                else:
                    #finish the withdraw
                    print(retQuery[0])
                    retQuery[0].finishWithdraw()
                    # make the key available
                    keyQuery = [key for key in self.listOfKeys if key.getRoom() == returnedKey]
                    keyQuery[0].returnKey()                    
                    logging.info("A chave {} foi retornada com sucesso.".format(retQuery[0].getKeyCode()))
    
    # ---------------------------
    # --------------------------- 
    def withdrawingKey(self):
        
        # ask which key will be withdrawn
        try:
            withKey = input("Qual chave tirar? ")
            withKey = withKey.upper()
            print(withKey)
        except KeyboardInterrupt:
            logging.debug('Keyboard interrupt')
        except Exception as err:
            logging.error(err)

        # check if the key is available
        filteredKey = self.searchKeyByCode(keyCode=withKey)
        
        # ver se tem chave
        if(filteredKey == []):
            logging.warning("A chave requerida não existe.!")
        elif(not filteredKey[0].isAvailable()):
            logging.warning('A chave requerida não está disponível!')
        else: 
            # only valid users can withdraw a key
            userCode = self.readBarcodeOnce()
            filteredUser = self.searchUserByCode(userCode=userCode)
            if(filteredUser == []):
                logging.warning('Não existe usuário cadastrado com esse código. Por favor, cadastre antes!')
            else :
                operation = KeyWithdraw(userCode = userCode, keyCode = withKey)
                # key was withdrawn
                filteredKey[0].withdrawKey()
                self.listOfWithdraws.append(operation)
                logging.info("A chave {} foi retirada com sucesso.".format(filteredKey[0].getRoom()))
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
            print("#######################################")
            
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