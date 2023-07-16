import mysql.connector
import pandas as pd
from prettytable import PrettyTable

# Establish a connection to MySQL
connect = mysql.connector.connect(
    host='localhost',
    user='root',
    port='3306',
    password='root'
)


class Stock:
    def __init__(self, username):
        self.user_name = username
        self.cursor = connect.cursor()
        self.show_methods()

    def show_methods(self):
        methods = {
            '1': '1. Create Table',
            '2': '2. Data Insert',
            '3': '3. Update Table Data',
            '4': '4. Update Table Structure',
            '5': '5. Drop Table',
            '6': '6. Truncate Table',
            '7': '7. List Available Tables',
            '8': '8. Show Table Data',
            '9': '9. Exit'
        }

        while True:
            for method in methods.values():
                print(method)

            choice = input('Enter choice number: ')
            if choice == '1':
                self.create_table()
            elif choice == '2':
                self.data_input()
            elif choice == '3':
                self.update_data_table()
            elif choice == '4':
                self.update_table_structure()
            elif choice == '5':
                self.drop_table()
            elif choice == '6':
                self.truncate_table()
            elif choice == '7':
                self.show_tables()
            elif choice == '8':
                self.show_data()
            elif choice == '9':
                break
            else:
                print('Invalid choice. Please try again.')



    def create_user_profile(self):
        new_username = input("Enter the new username: ")
        
        # Check if the username already exists in the login table
        self.cursor.execute("SELECT * FROM login WHERE username = %s;", (new_username,))
        existing_user = self.cursor.fetchone()
        if existing_user:
            raise Exception("Username already exists. Please choose a different username.")
        
        # Check if the username exists as a database
        self.cursor.execute("SHOW DATABASES;")
        databases = [db[0] for db in self.cursor.fetchall()]
        if new_username in databases:
            raise Exception("Username already exists as a database. Please choose a different username.")
        
        new_password=input("Enter your password: ")
        # Add the new user to the login table and create their user profile
        self.cursor.execute("INSERT INTO login (username,password) VALUES (%s,%s);", (new_username),new_password)
        self.cursor.execute(f"CREATE DATABASE {new_username};")
        self.cursor.execute(f"USE {new_username};")
        self.cursor.execute("CREATE TABLE user_profile (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), surname VARCHAR(255), phone_no VARCHAR(20), date_of_join DATE);")
        connect.commit()
        
        print(f"User profile created successfully for {new_username}.")


    def create_table(self):
        self.cursor.execute(f"use {self.user_name};")
        table_name = input("Enter the table name: ")
        num_columns = int(input("Enter the number of columns: "))

        columns = []
        for i in range(num_columns):
            column_name = input(f"Enter the name for column {i + 1}: ")
            data_type = input(f"Enter the data type for column {i + 1} (int/float/varchar/date): ")

            if data_type == 'int':
                column_info = f"{column_name} INT"
            elif data_type == 'float':
                column_info = f"{column_name} FLOAT"
            elif data_type == 'varchar':
                varchar_length = int(input(f"Enter the varchar length for column {i + 1}: "))
                column_info = f"{column_name} VARCHAR({varchar_length})"
            elif data_type == 'date':
                column_info = f"{column_name} DATE"
            else:
                print("Invalid data type. Please choose int, float, varchar, or date.")
                return

            columns.append(column_info)

        query = f"CREATE TABLE {table_name} ({', '.join(columns)});"
        self.cursor.execute(query)
        connect.commit()
        print(f"Table {table_name} created successfully.")

    def data_input(self):
        self.cursor.execute(f"use {self.user_name};")
        self.cursor.execute("show tables;")
        list_tables = self.cursor.fetchall()

        while True:
            for i, table in enumerate(list_tables):
                print(f'{i + 1}: {table[0]}')

            select_table = int(input("Enter the option number for selecting the table: "))
            if select_table not in range(1, len(list_tables) + 1):
                print("Invalid Choice...")
            else:
                selected_table = list_tables[select_table - 1][0]
                self.cursor.execute(f"DESCRIBE {selected_table};")
                list_column = self.cursor.fetchall()

                for column in list_column:
                    print(column[0])

                print("Enter the data for the given columns:")
                query = f'INSERT INTO {selected_table} VALUES ('
                for i, column in enumerate(list_column):
                    column_name = column[0]
                    column_datatype = column[1]

                    if column_datatype.startswith(('varchar', 'char')):
                        value = input(f"Enter the value for column '{column_name}': ")
                        query += f"'{value}'"
                    elif column_datatype.startswith(('int', 'float')):
                        value = input(f"Enter the value for column '{column_name}': ")
                        query += value
                    elif column_datatype == 'date':
                        value = input(f"Enter the value for column '{column_name}' (YYYY-MM-DD): ")
                        query += f"'{value}'"
                    else:
                        print(f"Unsupported datatype '{column_datatype}' for column '{column_name}'.")
                        return

                    if i < len(list_column) - 1:
                        query += ', '

                query += ');'
                self.cursor.execute(query)
                connect.commit()
                print(f"Data inserted into table {selected_table} successfully.")
                break


    
    def update_data_table(self):
        self.cursor.execute(f"USE {self.user_name};")
        self.cursor.execute("SHOW TABLES;")
        table_list = self.cursor.fetchall()

        # Display the available tables
        print("Available Tables:")
        for i, table in enumerate(table_list):
            print(f"{i+1}. {table[0]}")

        # Prompt the user to select a table
        table_num = int(input("Enter the table number to update: "))
        if table_num not in range(1, len(table_list) + 1):
            print("Invalid table number.")
            return

        selected_table = table_list[table_num - 1][0]

        # Fetch the current data from the selected table
        self.cursor.execute(f"SELECT * FROM {selected_table};")
        rows = self.cursor.fetchall()

        # Display the current data using pandas DataFrame
        df = pd.DataFrame(rows, columns=self.cursor.column_names)
        print("Current Data:")
        print(df)

        # Prompt the user to select a row to update
        row_num = int(input("Enter the row number to update: "))
        if row_num not in range(1, len(rows) + 1):
            print("Invalid row number.")
            return

        selected_row = rows[row_num - 1]

        # Get the column names
        column_names = self.cursor.column_names

        # Prompt the user for new data for each column
        num_columns = len(selected_row)
        new_data = []
        for i in range(num_columns):
            column_name = column_names[i]
            value = input(f"Enter the new value for {column_name}: ")
            new_data.append(value)

        # Construct the update query to update the selected row
        update_query = f"UPDATE {selected_table} SET "
        update_query += ", ".join([f"{column_names[i]} = '{new_data[i]}'" for i in range(num_columns)])
        update_query += " WHERE "
        update_query += " AND ".join([f"{column_names[i]} = '{selected_row[i]}'" for i in range(num_columns)])
        update_query += ";"
        self.cursor.execute(update_query)
        connect.commit()

        # Fetch the updated data from the table
        self.cursor.execute(f"SELECT * FROM {selected_table};")
        updated_rows = self.cursor.fetchall()

        # Display the updated data using pandas DataFrame
        df = pd.DataFrame(updated_rows, columns=self.cursor.column_names)
        print("Updated Data:")
        print(df)

    def update_table_structure(self):
        self.cursor.execute(f"USE {self.user_name};")
        self.cursor.execute("SHOW TABLES;")
        table_list = self.cursor.fetchall()

        # Display the available tables
        print("Available Tables:")
        for i, table in enumerate(table_list):
            print(f"{i+1}. {table[0]}")

        # Prompt the user to select a table
        table_num = int(input("Enter the table number to update: "))
        if table_num not in range(1, len(table_list) + 1):
            print("Invalid table number.")
            return

        selected_table = table_list[table_num - 1][0]

        # Fetch the current structure of the selected table
        self.cursor.execute(f"DESCRIBE {selected_table};")
        columns = self.cursor.fetchall()

        # Display the current structure of the table using pandas DataFrame
        df = pd.DataFrame(columns, columns=["Field", "Type", "Null", "Key", "Default", "Extra"])
        print("Current Structure:")
        print(df)

        # Prompt the user to select a column to alter
        column_num = int(input("Enter the column number to alter: "))
        if column_num not in range(1, len(columns) + 1):
            print("Invalid column number.")
            return

        selected_column = columns[column_num - 1]

        # Prompt the user for the type of alteration
        print("Select the type of alteration:")
        print("1. Rename column")
        print("2. Change data type")
        print("3. Change constraint")
        print("4. Drop column")
        alteration_type = int(input("Enter the alteration type: "))

        if alteration_type == 1:  # Rename column
            new_column_name = input("Enter the new column name: ")
            alter_query = f"ALTER TABLE {selected_table} CHANGE COLUMN '{selected_column[0]}' '{new_column_name}' {selected_column[1]};"
            self.cursor.execute(alter_query)
            connect.commit()
            print("Column renamed successfully.")
        elif alteration_type == 2:  # Change data type
            new_column_datatype = input("Enter the new column datatype: ")
            alter_query = f"ALTER TABLE {selected_table} MODIFY COLUMN '{selected_column[0]}' {new_column_datatype};"
            self.cursor.execute(alter_query)
            connect.commit()
            print("Data type changed successfully.")
        elif alteration_type == 3:  # Change constraint
            new_column_constraint = input("Enter the new column constraint: ")
            alter_query = f"ALTER TABLE {selected_table} MODIFY COLUMN '{selected_column[0]}' {selected_column[1]} {new_column_constraint};"
            self.cursor.execute(alter_query)
            connect.commit()
            print("Constraint changed successfully.")
        elif alteration_type == 4:  # Drop column
            confirm_drop = input("Are you sure you want to drop this column? (yes/no): ")
            if confirm_drop.lower() == "yes":
                alter_query = f"ALTER TABLE {selected_table} DROP COLUMN '{selected_column[0]}';"
                self.cursor.execute(alter_query)
                connect.commit()
                print("Column dropped successfully.")
            else:
                print("Column drop cancelled.")
        else:
            print("Invalid alteration type.")

    def disconnect_cursor(self):
        self.cursor.close()

    def drop_table(self):
        self.cursor.execute(f"USE {self.user_name}")
        self.cursor.execute("SHOW TABLES;")
        table_list = self.cursor.fetchall()

        # Display the available tables
        print("Available Tables:")
        for i, table in enumerate(table_list):
            print(f"{i+1}. {table[0]}")

        # Prompt the user to select a table to drop
        table_num = int(input("Enter the table number to drop: "))
        if table_num not in range(1, len(table_list) + 1):
            print("Invalid table number.")
            return

        selected_table = table_list[table_num - 1][0]

        # Prompt the user for confirmation
        confirm_drop = input("Are you sure you want to drop this table? (yes/no): ")
        if confirm_drop.lower() == "yes":
            drop_query = f"DROP TABLE {selected_table};"
            self.cursor.execute(drop_query)
            connect.commit()
            print("Table dropped successfully.")
        else:
            print("Table drop cancelled.")

    def truncate_table(self):
        self.cursor.execute(f"USE {self.user_name}")
        self.cursor.execute("SHOW TABLES;")
        table_list = self.cursor.fetchall()

        # Display the available tables
        print("Available Tables:")
        for i, table in enumerate(table_list):
            print(f"{i+1}. {table[0]}")

        # Prompt the user to select a table to truncate
        table_num = int(input("Enter the table number to truncate: "))
        if table_num not in range(1, len(table_list) + 1):
            print("Invalid table number.")
            return

        selected_table = table_list[table_num - 1][0]

        # Prompt the user for confirmation
        confirm_truncate = input("Are you sure you want to truncate this table? (yes/no): ")
        if confirm_truncate.lower() == "yes":
            truncate_query = f"TRUNCATE TABLE {selected_table};"
            self.cursor.execute(truncate_query)
            connect.commit()
            print("Table truncated successfully.")
        else:
            print("Table truncate cancelled.")
    

    def show_tables(self):
        self.cursor.execute(f"USE {self.user_name}")
        self.cursor.execute("SHOW TABLES;")
        table_list = self.cursor.fetchall()

        if not table_list:
            print("Oops! No tables found.")
            return

        table_names = [table[0] for table in table_list]
        df = pd.DataFrame(table_names, columns=["Tables"])
        print(df)

    def show_data(self):
        self.cursor.execute(f"USE {self.user_name}")
        self.cursor.execute("SHOW TABLES;")
        table_list = self.cursor.fetchall()

        if not table_list:
            print("Oops! No tables found.")
            return

        print("Available Tables:")
        for i, table in enumerate(table_list):
            print(f"{i+1}. {table[0]}")

        table_num = int(input("Enter the table number to view data: "))
        if table_num not in range(1, len(table_list) + 1):
            print("Invalid table number.")
            return

        selected_table = table_list[table_num - 1][0]

        self.cursor.execute(f"SELECT * FROM {selected_table};")
        data = self.cursor.fetchall()

        if not data:
            print(f"Oops! No data found in table {selected_table}.")
            return

        # Display the data using pandas DataFrame
        df = pd.DataFrame(data, columns=self.cursor.column_names)
        print(df)

if __name__ == '__main__':
    # Code for testing the Stock class if needed
    pass