from dataBase import userDB
from UserClass import User

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
    password_input = input("enter your password: ")
    if(not user_database.user_in_DB(username_input)):
        user_database.register_user(username_input, password_input)
    curr_user = User(username_input, password_input, user_database.getID(username_input))
    return user_database.confirm_User(username_input, password_input)

def accountDB_menu():
    global curr_user, user_database
    print("hello " + curr_user.getUsername() + " please choose an action to perform:")
    welcome = """
             1: Enter a new Account to the database
             2: Remove an Account from the database
             3: Get an Account url, username and password
             4: exit the program"""
    print(welcome)
    # IDEA: adding a log out function
    action = input("what would you like to do? enter the corresponding number: ")
    while action != "4":
        if action == "1":
            acc_url = input("enter the account's url: ")
            acc_name = input("enter the account's name: ")
            acc_username = input("enter the account's username: ")
            acc_password = input("enter the account's password: ")
            user_database.inset_account(curr_user, acc_url, acc_name, acc_username, acc_password)
        elif action == "2":
            acc_name = input("enter the account's name you desire to delete: ")
            acc_username = input("enter the account's username you desire to delete: ")
            user_database.remove_account(curr_user, acc_name, acc_username)
        elif action == "3":
            acc_name = input("enter the account's name: ")
            user_database.get_account(curr_user, acc_name)
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
