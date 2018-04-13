import sqlite3


__author__ = "igor.nazarov"


class DbConnector:
    def __init__(self):
        self.__db_file = "./db.sqlite3"
        self.__conn = sqlite3.connect(self.__db_file)
        self.cursor = self.__conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS settings (file text, format text)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS url_stat 
                              (url text, method text, day real, month real, year real, count real)''')
        self.__conn.commit()

    def close(self):
        self.cursor.execute('''DROP TABLE IF EXISTS settings''')
        self.cursor.execute('''DROP TABLE IF EXISTS url_stat''')
        self.__conn.commit()
        self.__conn.close()

    def set_log(self, path, log_format):
        self.cursor.execute('''INSERT INTO settings VALUES ("{}", "{}")'''.format(path, log_format))
        self.__conn.commit()

    def get_log(self):
        self.cursor.execute('''SELECT * FROM settings''')
        return self.cursor.fetchone()

    def add_url_stat(self, url, method, day, month, year):
        self.cursor.execute('''SELECT * FROM url_stat WHERE 
                            url = "{}" AND method = "{}" AND day = {} AND month = {} AND year = {}'''
                            .format(url, method, day, month, year))
        result = self.cursor.fetchone()
        if not result:
            self.cursor.execute('''INSERT INTO url_stat VALUES ("{}", "{}", {}, {}, {}, {})'''
                                .format(url, method, day, month, year, 1))
            self.__conn.commit()
            return 200

        count = int(result[5]) + 1
        self.cursor.execute('''UPDATE url_stat SET count = {}
                              WHERE url = "{}" AND method = "{}" AND day = {} AND month = {} AND year = {} '''
                            .format(count, url, method, day, month, year))
        self.__conn.commit()
        return 200

    def get_url_stat(self, url, method):
        self.cursor.execute('''SELECT day, month, year, count FROM url_stat WHERE url = "{}" AND method = "{}"'''
                            .format(url, method))
        return self.cursor.fetchall()


