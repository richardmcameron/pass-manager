import psycopg2, random, string


class PGL:
    def __init__(self):
        self.conn = None
        self.dbid = None

        self.db_list = None

    def connect(self, dbname = 'postgres'):
        self.conn = psycopg2.connect(user="",
                            password="",
                            host="127.0.0.1",
                            port="",
                            database=f"{dbname}")

        return self.conn

    def create_database(self, dbname):
        self.conn = self.connect()
        self.conn.autocommit = True
        cur = self.conn.cursor()
        cur.execute("CREATE DATABASE %s" % (dbname))
        self.conn.close()

    def insert(self, email, password, appid):
        self.conn = self.connect()
        cur = self.conn.cursor()
        cur.execute("INSERT INTO accounts VALUES('%s','%s','%s')" % (email, password, appid))
        self.conn.commit()
        self.conn.close()

    def view(self):
        self.conn = self.connect()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM accounts")
        self.conn.commit()
        self.conn.close()

    def delete(self, item):
        self.conn = self.connect()
        cur = self.conn.cursor()
        cur.execute("DELETE FROM accounts WHERE item=?", (item,))
        self.conn.commit()
        self.conn.close()

    def print_table(self):
        self.conn = self.connect()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM accounts")
        rows = cur.fetchall()

        for row in rows:
            print(row)

        self.conn.close()

    def view_db(self):
        self.conn = self.connect()
        cur = self.conn.cursor()
        cur.execute("SELECT datname FROM pg_database")
        rows = cur.fetchall()

        for row in rows:
            print(row)

        self.conn.close()

    '''---------------------------------------------------------------------'''

    def check_user_found(self, username):
        account_found = False
        self.conn = self.connect(dbname="logins")
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM login_accounts")
        data = cur.fetchall()
        for t in data:
            if t[0] == username:
                print("[ACCOUNT FOUND]")
                account_found = True
            else:
                account_found = False
        self.conn.close()
        return account_found

    def search_login(self, username, password):
        account_found = False
        self.conn = self.connect(dbname= "logins")
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM login_accounts")
        data = cur.fetchall()
        for t in data:
            if t[0] == username:
                if t[1] == password:
                    print("[ACCOUNT FOUND]")
                    account_found = True
                else:
                    account_found = False
        self.conn.close()
        return account_found

    def create_login(self, username, password):
        if not self.search_login(username, password):
            ID = ''.join(random.choice(string.ascii_lowercase) for _ in range(64))
            self.conn = self.connect(dbname= 'logins')
            cur = self.conn.cursor()
            cur.execute("INSERT INTO login_accounts VALUES('%s','%s', '%s')" % (username, password, ID))
            self.conn.commit()
            self.conn.close()
            return True

        else:
            return False

    def create_table(self, ID):
        table_name = 'accounts_' + ID

        self.conn = self.connect(dbname= ID)
        cur = self.conn.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (email TEXT, password TEXT, appid TEXT)")
        self.conn.commit()
        self.conn.close()

    '''---------------------------------------------------------------------'''

    def connect_db(self, username):
        self.conn = self.connect(dbname="logins")
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM login_accounts")
        data = cur.fetchall()

        for t in data:
            if t[0] == username:
                ID = t[2]

        self.conn.close()

        self.dbid = ID

        try:
            self.create_database(self.dbid)
        except:
            print('[DATABASE FOUND]')

        self.create_table(self.dbid)


    '''---------------------------------------------------------------------'''

    def get_database_entries(self):
        self.db_list = []
        table_name = 'accounts_' + self.dbid
        self.conn = self.connect(dbname = self.dbid)
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        data = cur.fetchall()
        for d in data:
            self.db_list.append(d)
        self.conn.close()

    def insert_user_db(self, email, password, description):
        table_name = 'accounts_' + self.dbid
        self.conn = self.connect(dbname=self.dbid)
        cur = self.conn.cursor()
        cur.execute("INSERT INTO %s VALUES('%s','%s','%s')" % (table_name, email, password, description))
        self.conn.commit()
        self.conn.close()
