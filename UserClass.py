class User():
   def __init__(self, username, password, id):
       self._username = username 
       self._password = password
       self._id = id
       
   def getID(self):
      return self._id
    
   def getUsername(self):
      return self._username

   def getPassword(self):
      return self._password