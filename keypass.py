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
    print(curr_user.getID())
    return user_database.confirm_User(username_input, password_input)

def accountDB_menu():
    global curr_user, user_database
    print("hello " + curr_user.getUsername() + " please choose an action to perform:")
    print("""
             1: Enter a new Account to the database
             2: Remove an Account from the database
             3: Get an Account url, username and password
             4: exit the program""")
    action = input("what would you like to do? enter the corresponding number: ")
    while action != "4":
        if action == "1":
            user_database.inset_account(curr_user)
        elif action == "2":
            pass
        elif action == "3":
            pass
        else:
            print("invalid input, please try again")
        action = input("what else would you like to do? enter the corresponding number: ")

def main():
    if(user_login()):
        print("logged in successfully")
        accountDB_menu()
    else:
        print("login failed")


if __name__ == '__main__':
    main()
