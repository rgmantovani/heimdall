# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

class People:
    
    def __init__(self, name = None, code = None, photo = None, role = None):
        self.setName(name)
        # TODO: split name and surname
        self.setCode(code)
        self.setPhoto(photo)
        self.setRole(role)
    
    # convert object to string
    def __str__(self):
        return(str(self.__dict__))
            
    def setName(self, name):
        self.name = name
        
    def setCode(self, code):
        self.code = code
        
    def setPhoto(self, photo):
        self.photo = photo
        
    def setRole(self, role):
        self.role = role
        
    def getName(self):
        return(self.name)
    
    def getCode(self):
        return(self.code)
    
    def getRole(self):
        return(self.role)
    
    def getPhoto(self):
        return(self.photo)
        
# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
