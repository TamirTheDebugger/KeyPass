import hashlib
from os import path, urandom
from base64 import b64encode, b64decode
import sqlite3

class userDB():
    def __init__ (self, database_file_name):
        self.__conn = sqlite3.connect(database_file_name)
        self.__pos = self.__conn.cursor()
    
    def create_tables(self):
        try:
            self.__pos.execute("""CREATE TABLE users (userID PRIMARY KEY, username UNIQUE, password NOT NULL, salt NOT NULL) """)
        except:
            pass
        try:
            self.__pos.execute("""CREATE TABLE accounts (accID PRIMARY KEY, userID FOREIGN KEY REFRENCES users(userID), url NOT NULL, acc_user NOT NULL, acc_password NOT NULL) """)
        except:
            pass

    def register_user(self, username, password):
        salt = urandom(64)
        new_password = password.encode() + salt
        salt = b64encode(salt).decode()
        hash_password = b64encode(hashlib.sha256(new_password).digest()).decode()
        self.__pos.execute("INSERT INTO users VALUES(?,?,?)", (username, hash_password, salt))
        self.__pos.execute('SELECT last_rowid()')
        self.__conn.commit()

    def confirm_User(self, username, password):
        salt = b64decode(self.__pos.execute('SELECT salt FROM users WHERE username = ?', (username,)).fetchone()[0].encode())
        password = password.encode() + salt
        hash_password =  b64encode(hashlib.sha256(password).digest()).decode()
        cond = self.__pos.execute('SELECT password FROM users WHERE username = ?', (username,)).fetchone()[0] == hash_password
        if cond:
             return True
        return False

    def user_in_DB (self, username):
        if self.__pos.execute("SELECT username FROM users WHERE LIKE ?", (username,)).fetchone() != None:
            return True
        else:
            return False
    
    def getID(self, username):
        return self.__pos.execute('SELECT userID FROM users WHERE username LIKE ?', (username,))

    

    