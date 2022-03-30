import mysql.connector
from mysql.connector import errorcode


class OppslagReg:
    def __init__(self) -> None:
        dbconfig = {'host': '127.0.0.1',
                    'user': 'user',
                    'password': 'test',
                    'database': 'myDb', }
        self.configuration = dbconfig

    # Kode hentet fra forelesning
    def __enter__(self) -> 'cursor':
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor(prepared=True)
        return self

    # Kode hentet fra forelesning
    def __exit__(self, exc_type, exc_val, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    # Kode hentet fra forelesning
    def query(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def show_all(self):
        try:
            self.cursor.execute("SELECT * FROM oppslag")
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return result

    def show_oppslag(self, id):
        try:
            self.cursor.execute(
                "SELECT * FROM oppslag WHERE id=(%s)",
                (id,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
            print(err)
        return result

    def show_kategori(self, kategori):
        try:
            kategori = self.get_kategori(kategori)
            self.cursor.execute(
                "SELECT * FROM oppslag WHERE kategori=(%s)",
                (kategori,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        return result

    def new_oppslag(self, oppslag):
        try:
            sql = '''
            INSERT INTO oppslag VALUES (tittel = %s, ingress = %s,
            oppslagtekst = %s, kategori = %s, dato = date(now()), bruker = %s
            treff = 0)
            '''
            self.cursor.excecute(sql, (oppslag,))
        except mysql.connector.Error as err:
            print(err)

    def delete_oppslag(self, id):
        try:
            self.cursor.execute("DELETE FROM oppslag WHERE id=(%s)", (id,))
        except mysql.connector.Error as err:
            print(err)

    def update_oppslag(self, oppslag):
        try:
            sql1 = '''UPDATE oppslag 
            SET tittel = %s, ingress = %s, oppslagtekst = %s,
            kategori = %s, dato = now()
            WHERE id = %s'''
            self.cursor.execute(sql1, (oppslag,))
        except mysql.connector.Error as err:
            print(err)

    def count_treff(self, id):
        try:
            sql = '''
            UPDATE oppslag
            SET treff = treff+1
            WHERE id = %s'''
            self.cursor.execute(sql, (id,))
        except mysql.connector.Error as err:
            print(err)

    def get_kategori(self, kat):
        if kat == "hjem":
            return 1
        elif kat == "bil":
            return 2
        elif kat == "motorsykkel":
            return 3
        elif kat == "båt":
            return 4
        elif kat == "fly":
            return 5
        elif kat == "diverse":
            return 6
        else:
            return "hjem"
