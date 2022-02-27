import json
import sqlite3


class DataException(Exception):
    pass


class LoginException(Exception):
    pass


class LoginMain(object):

    def __init__(self, database='user_info.db'):
        self.conn = sqlite3.connect(database)
        self.curs = self.conn.cursor()

    def create_table(self):
        try:
            self.curs.execute(
                'CREATE TABLE user_info(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, PASSWORD STRING)'
            )
            return True
        except Exception as e:
            print(e)
            return False

    def insert_data(self, user_name: str, password: str):
        try:
            self.curs.execute(
                f'INSERT INTO user_info(name, password) values("{user_name}", "{password}")'
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def login_check(self, user_name: str, password: str):
        try:
            self.curs.execute(
                f'SELECT * FROM user_info WHERE name = "{user_name}"'
            )
            datas = self.curs.fetchall()
            if len(datas) != 1:
                raise DataException('DataBase Information Exception')

            data = datas[0]
            registered_name = data[1]
            registered_password = data[2]
            if registered_name == user_name and registered_password == password:
                user_info = {
                    'username': registered_name,
                    'password': registered_password,
                }
                return json.dumps(user_info)
            else:
                raise LoginException('Login denied')

        except LoginException as e:
            print(f'{e}: Username or Password doesn\'t match with registered it')
            return False

        except DataException as e:
            print(f'{e}: Registered information is wrong')
            return False
        except Exception as e:
            print(e)
            return False

    def __del__(self):
        self.curs.close()
        self.conn.close()
