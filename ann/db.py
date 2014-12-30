import sqlite3
import uuid

def debug(f):
    def wrapper(*args, **kargs):
        print args, kargs
        return f(*args, **kargs)
    return wrapper

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()

    @debug
    def read_db(self, query, *args):
        self.c.execute(query, *args)
        return self.c.fetchall()

    @debug
    def write_db(self, query, *args):
        self.c.execute(query, *args)
        self.conn.commit()

    @debug
    def is_table_existing(self, table):
        query = '''
        SELECT name FROM sqlite_master WHERE type='table' AND name = ?
        '''
        r = self.read_db(query, (table, ))
        return True if r else False
    
    def is_key_existing(self, key, value, table):
        query = '''
        SELECT ? FROM ? WHERE ? = ?
        '''
        r = self.read_db(query, (key, table, key, value))
        return True if r else False

    def detele_db(self,*data):
        pass
    def update_db(self,*data):
        pass

class AccountDB(Database):
    """
    AccountDB is respect for account data base operations
    """
    def create_table(self):
        sql = '''
        CREATE TABLE account (
        uuid TEXT PRIMARY KEY,
        name VARCHAR(20),
        passwd TEXT
        )
        '''
        if not self.is_table_existing('account'):
            self.write_db(sql)
        
    def is_user_existing(self, user):
        query = '''
        SELECT name FROM account WHERE name = ?
        '''
        r = self.read_db(query, (user, ))
        return True if r else False

    def add_user(self, username, pw):
        if not self.is_user_existing(username):
            sql = '''
            INSERT INTO account VALUES (?,?,?)
            '''
            uid = str(uuid.uuid4()) 
            self.write_db(sql, (uid, username, pw))
        else:
            pass

    def get_user(self, user):
        query = '''
        SELECT * FROM account WHERE name = ?
        '''
        return self.read_db(query, (user, ))
