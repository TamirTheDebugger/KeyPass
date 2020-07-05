from dataBase import userDB
from UserClass import User
import pyperclip
from ctypes import windll
import time
import threading
from getpass import getpass

curr_user = "placeholder"
user_database = userDB("test_DB")
def user_login():
    """
    login process - verifying the user - username & password.
    :return: if the login was successful
    :rtype: boolean
    """
    global curr_user, user_database
    username_input = input("enter your username: ")
    password_input = getpass(prompt="enter your password: ", stream = None)
    if(not user_database.user_in_DB(username_input)): # checking if the user in the databse
        user_database.register_user(username_input, password_input)
    curr_user = User(username_input, password_input, user_database.getID(username_input)) # creating a User object with its credentials
    return user_database.confirm_User(username_input, password_input)

def copy_creds(str):
    """
    copies data to the clipboard and deletes it after 30s
    :param str: information to copy
    :type str: String
    :return: None
    """
    pyperclip.copy(str)
    time.sleep(15) # waiting 15 seceonds
    if windll.user32.OpenClipboard(None): # clearing the clipboard
        windll.user32.EmptyClipboard()
        windll.user32.CloseClipboard()

def copy_menu(cred_list):
    """
    the menu to copy the account credentials
    :param cred_list: a list of all accounts retrieved with their information in tuples
    :type cred_list: list
    :return: None
    """
    print("here are the accounts we found:")
    if len(cred_list) == 0: # checking if any accounts were found
        print("no accounts were found\n")
        return None
    for i in range(len(cred_list)):
        acc = cred_list[i]
        print("\t" + str(i) + ". url: " + acc[0]) # displaying the retrieved accounts to the user
    chosen_account = int(input("insert the number of the account to copy: "))
    if chosen_account > len(cred_list): # checking if the chosen account exists in the list
        print("invalid number, please try again")
        return None
    print("""what would you like to copy?
            1. the url
            2. the username
            3. the password
            4. nothing""")
    copy_info = input("enter the number of what you want to copy: ") # the user enters what information to copy
    while copy_info != "4":
        cred_to_copy = ""
        if copy_info == "1":
            cred_to_copy = cred_list[chosen_account][0] # copying the url and clearing the clipboard afterwards
        elif copy_info == "2":
            cred_to_copy = cred_list[chosen_account][1] # copying the username and clearing the clipboard afterwards
        elif copy_info == "3":
            cred_to_copy = cred_list[chosen_account][2] # copying the password and clearing the clipboard afterwards
        t = threading.Thread(target=copy_creds, args=(cred_to_copy,))
        t.start()
        copy_info = input("enter the number of what else you want to copy: ")

def accountDB_menu():
    """
    the menu to control the database
    :return: None
    """
    global curr_user, user_database
    print("hello " + curr_user.getUsername() + " please choose an action to perform:")
    welcome = """
             1: Enter a new Account to the database
             2: Remove an Account from the database
             3: Get an Account url, username and password
             4: exit the program"""
    print(welcome)
    action = input("what would you like to do? enter the corresponding number: ")
    while action != "4":
        if action == "1": # inserting an account to the database
            acc_url = input("enter the account's url: ")
            acc_name = input("enter the account's name: ")
            acc_username = input("enter the account's username: ")
            acc_password = getpass(prompt="enter the account's password: ", stream = None)
            user_database.inset_account(curr_user, acc_url, acc_name, acc_username, acc_password)
        elif action == "2": # removing an account to the databse
            acc_name = input("enter the account's name you desire to delete: ")
            acc_username = input("enter the account's username you desire to delete: ")
            user_database.remove_account(curr_user, acc_name, acc_username)
        elif action == "3": # retrieving an account from the database
            acc_name = input("enter the account's name: ")
            copy_menu(user_database.get_account(curr_user, acc_name))
        else:
            print("invalid input, please try again")
        print(welcome)
        action = input("what else would you like to do? enter the corresponding number: ")
    print("\n thank you and goodbye :)")

def main():
    if(user_login()):
        print("logged in successfully")
        accountDB_menu()
    else:
        print("login failed")


if __name__ == '__main__':
    main()
