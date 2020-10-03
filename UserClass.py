class User():
   def __init__(self, username, password, id):
       # constructor
       self._username = username
       self._password = password
       self._id = id

   def getID(self):
      """
      gets the current user's ID.
      :return: id
      :rtype: String
      """
      return self._id

   def getUsername(self):
      """
      gets the current user's username.
      :return: username
      :rtype: String
      """
      return self._username

   def getPassword(self):
      """
      gets the current user's password.
      :return: password
      :rtype: String
      """
      return self._password
