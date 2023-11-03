# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

import logging
from Entities.User import User
from Database.FileDatabaseHandler import FileDatabaseHandler
from Database.RemoteDatabaseHandler import RemoteDatabaseHandler

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

class HeimdallSystem:
     
    # ---------------------------
    # constructor
    # ---------------------------
    def __init__(self):   
        
        # database handler based on file systems (binary file)
        #self.sgbd = FileDatabaseHandler()
        
        # database handler based on MariaDB systems (remote access)
        self.sgbd = RemoteDatabaseHandler()
                        
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
       
        # cannot add an existing user
        query = self.sgbd.searchUserByCode(userCode=userCode)
        if(query == []):
            logging.debug("Adicionando um novo usuário.")
            self.sgbd.insertNewUser(newUser=user)
        else:
            logging.warning("Já existe um usuário com esse código. Operação não realizada!")
   
    # ---------------------------
    # --------------------------- 
    def removeUser(self):
        # remove a valid user
        userCode = self.readBarcodeOnce()
        filteredUsers = self.sgbd.searchUserByCode(userCode=userCode)
        if(filteredUsers == []):
            logging.warning("Não existe usuário com esse código para ser removido. Operação não realizada!")
        else:
            self.sgbd.removeAnUser(userCode=userCode)
            logging.debug("Removendo um usuário.")

    # ---------------------------
    # --------------------------- 
    def returningKey(self):    
        
        userCode = self.readBarcodeOnce()
        # only valid users can handle keys
        filteredUsers = self.sgbd.searchUserByCode(userCode=userCode)
        if(filteredUsers == []):
            logging.warning('Não existe usuário cadastrado com esse código. Por favor, cadastre antes!')
        else :
            # find the withdraw with the userCode (only not finished withdraws)
            filteredWithdraws = self.sgbd.searchWithdrawsByUsercode(userCode=userCode, status="opened")
            if(filteredWithdraws == []):
                logging.warning("Não foi feita nenhuma retirada pelo usuário.")
            # if there is an unique withdraw, just finish it     
            elif(len(filteredWithdraws) == 1):
                logging.info("Existe uma única retirada realizada pelo usuário.")
                filteredWithdraws[0].finishWithdraw()
                # make the key available
                filteredKey = self.sgbd.searchKeyByCode(keyCode=filteredWithdraws[0].getKeyCode()) 
                filteredKey[0].returnKey()
                self.sgbd.returnKey(userCode, filteredKey[0].getRoom())                   
                logging.info("A chave {} foi retornada com sucesso.".format(filteredKey[0].getRoom()))
            #there are more than one opened withdraws for this user
            else:
                logging.warning("Existem várias retiradas realizadas pelo mesmo usuário.")
                # showing all the withdraws with the userCode value
                for operation in filteredWithdraws:
                    print(operation)
                # ask which key will be returned (there is an option 'all' to return all of them)
                try:
                    returnedKey = input("Qual chave gostaria de retornar ? Digite \'Todas\' para retornar todas ao mesmo tempo. ").upper()
                except KeyboardInterrupt:
                    logging.debug('Keyboard interrupt')
                except Exception as err:
                    logging.error(err)
                
                if(returnedKey == "TODAS"):  # returning all the keys
                     for operation in filteredWithdraws:
                        operation.finishWithdraw()
                        keyQuery = self.sgbd.searchKeyByCode(keyCode=operation.getKeyCode())
                        keyQuery[0].returnKey()                    
                        self.sgbd.returnKey(userCode, keyQuery[0].getRoom())                   
                        logging.info("A chave {} foi retornada com sucesso.".format(operation.getKeyCode()))
                else: # returning a single key
                    retQuery = self.sgbd.searchWithdrawsByKeycode(keyCode=returnedKey, listOfWithdraws=filteredWithdraws)
                    if(retQuery == []):
                        logging.warning("A chave digitada não existe ou não foi retirada anteriormente")
                    else:
                        #finish the withdraw
                        retQuery[0].finishWithdraw()
                        # make the key available
                        keyQuery = self.sgbd.searchKeyByCode(keyCode=returnedKey)
                        keyQuery[0].returnKey()                    
                        self.sgbd.returnKey(userCode, keyQuery[0].getRoom())                   
                        logging.info("A chave {} foi retornada com sucesso.".format(retQuery[0].getKeyCode()))
    
    # ---------------------------
    # --------------------------- 
    def withdrawingKey(self):
        
        # ask which key will be withdrawn
        try:
            withKey = input("Qual chave tirar? ").upper()
        except KeyboardInterrupt:
            logging.debug('Keyboard interrupt')
        except Exception as err:
            logging.error(err)

        # check if the key is available
        filteredKey = self.sgbd.searchKeyByCode(keyCode=withKey)
        
        # check if the key exists
        if(filteredKey == []):
            logging.warning("A chave requerida não existe.!")
        # check if the key is available
        elif(not filteredKey[0].isAvailable()):
            logging.warning('A chave requerida não está disponível!')
        else: 
            # only valid users can withdraw a key
            userCode = self.readBarcodeOnce()
            filteredUser = self.sgbd.searchUserByCode(userCode=userCode)
            if(filteredUser == []):
                logging.warning('Não existe usuário cadastrado com esse código. Por favor, cadastre antes!')
            else : # key was withdrawn
                self.sgbd.withdrawKey(keyCode=withKey, userCode=userCode)
                filteredKey[0].withdrawKey()
                logging.info("A chave {} foi retirada com sucesso.".format(filteredKey[0].getRoom()))
        
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
                case "2": self.removeUser()
                case "3": self.withdrawingKey()
                case "4": self.returningKey()
                case '5': self.sgbd.listAllUsers()
                case '6': self.sgbd.listAllKeys()
                case '7': self.sgbd.listAllWithdraws()
                case "8": exit()

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------