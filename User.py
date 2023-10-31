# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------

class User:
        
    # ---------------------------
    # constructor
    # ---------------------------

    def __init__(self, name = None, surname = None, code = None, 
            photo = None, role = None, course = None):
        self.setName(name)
        self.setSurname(surname)
        self.setCode(code)
        self.setPhoto(photo)
        self.setRole(role)
        self.setCourse(course)
    
    # ---------------------------
    # convert object to string
    # ---------------------------
    
    def __str__(self):
        return(str(self.__dict__))
      
    # ---------------------------
    # ---------------------------
           
    def setName(self, name):
        self.name = name

    # ---------------------------
    # ---------------------------
           
    def setSurname(self, surname):
        self.surname = surname

    # ---------------------------
    # ---------------------------
           
    def setCourse(self, course):
        self.course = course

    # ---------------------------
    # ---------------------------
        
    def setCode(self, code):
        self.code = code
 
    # ---------------------------
    # ---------------------------
        
    def setPhoto(self, photo):
        self.photo = photo
    
    # ---------------------------
    # ---------------------------
        
    def setRole(self, role):
        self.role = role
    
    # ---------------------------
    # ---------------------------
        
    def getName(self):
        return(self.name)
    
    # ---------------------------
    # ---------------------------
        
    def getSurname(self):
        return(self.surname)
    
    # ---------------------------
    # ---------------------------
        
    def getCourse(self):
        return(self.course)
    
    # ---------------------------
    # ---------------------------
    
    def getCode(self):
        return(self.code)
    
    # ---------------------------
    # ---------------------------
    
    def getRole(self):
        return(self.role)
    
    # ---------------------------
    # ---------------------------
    
    def getPhoto(self):
        return(self.photo)
        
# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
