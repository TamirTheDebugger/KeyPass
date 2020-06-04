import hashlib
from os import path, urandom
from base64 import b64encode, b64decode
import sqlite3
from UserClass import User
from Crypto.Cipher import  AES

class userDB():
    def __init__ (self, database_file_name):
        # constructor
        self.__conn = sqlite3.connect(database_file_name)
        self.__pos = self.__conn.cursor()
        try:
            self.__pos.execute("""CREATE TABLE users (userID INTEGER PRIMARY KEY AUTOINCREMENT, username UNIQUE, password NOT NULL, salt NOT NULL) """)
            self.__pos.execute("""CREATE TABLE accounts (accID INTEGER PRIMARY KEY AUTOINCREMENT,userID NOT NULL, url NOT NULL, acc_username NOT NULL, acc_password NOT NULL,  FOREIGN KEY (userID) REFERENCES users(userID)) """)
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
        salt = urandom(64)
        new_password = password.encode() + salt
        salt = b64encode(salt).decode()
        hash_password = b64encode(hashlib.sha512(new_password).digest()).decode()
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
        salt = b64decode(self.__pos.execute('SELECT salt FROM users WHERE username = ?', (username,)).fetchone()[0].encode())
        password = password.encode() + salt
        hash_password =  b64encode(hashlib.sha512(password).digest()).decode()
        cond = self.__pos.execute('SELECT password FROM users WHERE username = ?', (username,)).fetchone()[0] == hash_password
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


    def inset_account(self, user):
        acc_name = input("enter the account's name: ")
        acc_username = input("enter the account's username: ")
        acc_password = input("enter the account's password: ")
        key = hashlib.sha256(user.getPassword().encode()).digest()
        vector = hashlib.md5(key).digest()  # create vector in a size of 128-bit (16-bytes) for AES encryption calculations
        pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        enc = AES.new(key, AES.MODE_CBC, vector)
        acc_username = enc.encrypt(pad(acc_username).encode())
        acc_password = enc.encrypt(pad(acc_password).encode())
        """try:"""
        self.__pos.execute("INSERT INTO accounts (userID, url, acc_username, acc_password) VALUES(?,?,?,?)", (user.getID(), acc_name, acc_username, acc_password))
        self.__conn.commit()
        print("Account saved successfully")
        """except Exception as e:
             print("an error occured, please try again: "  e)"""
