import hashlib
from os import path, urandom
from base64 import b64encode, b64decode
import sqlite3
from UserClass import User
from Crypto.Cipher import  AES

def cipher_str(user, str):
    """
    encrypts a string using AES.
    :param user: the user's credentials
    :param str: the string to encrypt
    :type user: User
    :type str: String
    :return: the encrypted string
    :rtype: binary
    """
    key = hashlib.sha256(user.getPassword().encode()).digest()
    vector = hashlib.md5(key).digest()  # create vector in a size of 128-bit (16-bytes) for AES encryption calculations
    pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16) # unpad = lambda s : s[:-ord(s[len(s)-1:])] - unpadding command for later
    enc = AES.new(key, AES.MODE_CBC, vector)
    return enc.encrypt(pad(str).encode())

def decipher_str(user, str):
    """
    decrypts a string using AES.
    :param user: the user's credentials
    :param str: the string to decrypt
    :type user: User
    :type str: String
    :return: the decrypted string
    :rtype: String
    """
    key = hashlib.sha256(user.getPassword().encode()).digest()
    vector = hashlib.md5(key).digest()  # create vector in a size of 128-bit (16-bytes) for AES encryption calculations
    unpad = lambda s : s[:-ord(s[len(s)-1:])]
    dec = AES.new(key, AES.MODE_CBC, vector)
    return unpad(dec.decrypt(str)).decode()

class userDB():
    def __init__ (self, database_file_name):
        # constructor
        self.__conn = sqlite3.connect(database_file_name)
        self.__pos = self.__conn.cursor()
        try: # creating the database tables
            self.__pos.execute("""CREATE TABLE users (userID INTEGER PRIMARY KEY AUTOINCREMENT, username UNIQUE, password NOT NULL, salt NOT NULL) """)
            self.__pos.execute("""CREATE TABLE accounts (accID INTEGER PRIMARY KEY AUTOINCREMENT,userID NOT NULL, acc_name NOT NULL, url NOT NULL, acc_username NOT NULL, acc_password NOT NULL,  FOREIGN KEY (userID) REFERENCES users(userID)) """)
        except:
            pass

    def register_user(self, username, password):
        """
        registers a new user in the system.
        :param new_username: a new user to register
        :param new_password: a the new user's password
        :type new_username: String
        :type new_password: String
        :return: NONE
        """
        salt = urandom(64) # generating salt
        new_password = password.encode() + salt
        salt = b64encode(salt).decode()
        hash_password = b64encode(hashlib.sha512(new_password).digest()).decode() # encrypting the password with the salt using sha512
        self.__pos.execute("INSERT INTO users (username, password, salt) VALUES(?,?,?)", (username, hash_password, salt))
        self.__conn.commit()
        print("Hello new user!")

    def confirm_User(self, username, password):
        """
        verifies the user to grant login access.
        :param username: the username of the user
        :param password: the user's password
        :type username: str
        :type password: str
        :return: if the password is verified or not
        :rtype: boolean
        """
        salt = b64decode(self.__pos.execute('SELECT salt FROM users WHERE username = ?', (username,)).fetchone()[0].encode())  # retrieving salt from the database
        password = password.encode() + salt
        hash_password =  b64encode(hashlib.sha512(password).digest()).decode()
        cond = self.__pos.execute('SELECT password FROM users WHERE username = ?', (username,)).fetchone()[0] == hash_password # checking whether the passwords match
        if cond:
             return True
        return False

    def user_in_DB (self, username):
        """
        checks for a username in the database
        :param username: the current user's username
        :type username: String
        :return: whether the user is present in the DB
        :rtype: Booelean
        """
        if self.__pos.execute("SELECT username FROM users WHERE username = ?", (username,)).fetchone() != None:
            return True
        else:
            return False

    def getID(self, username):
        """
        gets the current user's ID
        :param username: the current user's username
        :type username: String
        :return: NONE
        """
        return self.__pos.execute('SELECT userID FROM users WHERE username LIKE ?', (username,)).fetchone()[0]


    def inset_account(self, user, acc_url, acc_name, acc_username, acc_password):
        """
        insets a user's account to the accounts database
        :param user: the user's credentials
        :param acc_url: the url of the account
        :param acc_name: the name of the account
        :param acc_username: the username of the account
        :param acc_password: the password of the account
        :type user: User
        :type acc_url: String
        :type acc_name: String
        :type acc_username: String
        :type acc_password: String
        :return: NONE
        """
        acc_username = cipher_str(user, acc_username)
        acc_password = cipher_str(user, acc_password)
        try: # inserting the account to the database
            self.__pos.execute("INSERT INTO accounts (userID, acc_name, url, acc_username, acc_password) VALUES(?,?,?,?,?)", (user.getID(), acc_name, acc_url, acc_username, acc_password))
            self.__conn.commit()
            print("Account saved successfully")
        except :
            print("an error occurred, please try again")

    def remove_account(self, user, acc_name, acc_username):
        """
        removes a user's account to the accounts database
        :param user: the user's credendtials
        :param acc_name: the name of the account
        :param acc_username: the username of the account
        :type user: User
        :type acc_name: String
        :type acc_username: String
        :return: NONE
        """
        acc_username = cipher_str(user, acc_username)
        self.__pos.execute('DELETE FROM accounts WHERE userID LIKE ? AND acc_name LIKE ? AND acc_username LIKE ?', (user.getID(), acc_name, acc_username)) # deleting the desired account
        if self.__pos.execute(' SELECT changes()').fetchone()[0] > 0: # checking if the account was deleted
            print("account removed successfully!")
        else:
            print("account removal failed, please try entering an existing account")
        self.__conn.commit()

    def get_account (self, user, acc_name):
        """
        retrives a user's account to the accounts database
        :param user: the user's credendtials
        :param acc_name: the name of the account
        :type username: User
        :type acc_name: String
        :return: the account's information
        :rtype: Strings
        """
        acc_list = [] # a list of all the accounts with the given name in the user's database
        acc_list = self.__pos.execute('SELECT url, acc_username, acc_password FROM accounts WHERE userID LIKE ? AND acc_name LIKE ?', (user.getID(), acc_name)).fetchall()
        if len(acc_list) == 0:
            print("invalid account name, please enter an existing account")
        for cred in acc_list:
            acc_url = cred[0]
            acc_username = decipher_str(cred[1]) # decrypting the account's username
            acc_password = decipher_str(cred[2]) # decrypting the account's password
            print("account url: %s \naccount your username: %s \nyour account password: %s \n" % (acc_url, acc_username, acc_password)) # printing the user's account information
