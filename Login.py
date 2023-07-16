import mysql.connector
import getpass
from Customer import Customer
from Stock import Stock

def connect_to_mysql():
    host = input("Enter the MySQL server host (default: localhost): ") or 'localhost'
    user = input("Enter the MySQL server username: ")
    password = input("Enter the MySQL server password: ")
    port = input("Enter the MySQL server port (default: 3306): ") or '3306'

    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        print("Connected to MySQL server successfully!")
        return connection
    except mysql.connector.Error as error:
        print(f"Failed to connect to MySQL server: {error}")
        return None

class Login:
    def __init__(self):
        self.choices = {
            '1': '1. For Project Manager:',
            '2': '2. For Customers:',
            '3': '3. Exit:'
        }
        self.choice_input = None
        self.cursor = connect.cursor()

    def login_window(self):
        while True:
            for choice in self.choices.values():
                print(choice)
            
            self.choice_input = input('Enter choice number: ')
            if self.choice_input in self.choices.keys():
                if self.choice_input == '1':
                    self.check_login()
                    #self.stock_functions()
                elif self.choice_input == '2':
                    # self.customer.
                    pass
                elif self.choice_input == '3':
                    self.disconnect_cursor()
                    break
                else:
                    print("Invalid Choice.")
            else:
                print("Invalid Choice.")

    def check_login(self):
        while True:
            user = input("Enter the username: ")
            passwd = getpass.getpass("Enter the password: ")
            self.cursor.execute("USE Raxit;")
            self.cursor.execute("SELECT * FROM login;")
            login_details = self.cursor.fetchall()
            
            for login in login_details:
                if login[0] == user and login[1] == passwd:
                    print('Login Successful')
                    usr=Stock(user)                           # stock methods calling is left out.
                    return
            
            print('Login Unsuccessful')
            print('Either username or password is incorrect.')

    def disconnect_cursor(self):
        self.cursor.close()


if __name__ == '__main__':
    connect = connect_to_mysql()
    if connect is not None:
        login = Login()
        login.login_window()
        connect.close()