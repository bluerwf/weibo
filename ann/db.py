import sqlite3
import uuid
class UserAlreadyExists(Exception):
    def __init__(self, user):
        self.user = user

    def __str__(self):
        return "User: {user} already exists!".format(user=self.user)

def debug(f):
    def wrapper(*args, **kargs):
        print args, kargs
        return f(*args, **kargs)
    return wrapper

class Database:
    @debug
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
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
        passwd TEXT,
        follower  TEXT,
        following   TEXT
        )
        '''
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
            INSERT INTO account VALUES (?,?,?,?,?)
            '''
            uid = str(uuid.uuid4()) 
            self.write_db(sql, (uid, username, pw, None, None))
        else:
            raise UserAlreadyExists(username) 

    def get_user(self, user):
        query = '''
        SELECT * FROM account WHERE name = ?
        '''
        return self.read_db(query, (user, ))
    def add_follower(self, user, follower):
        if user == follower:
            raise Exception("Can't follow self")
        if self.get_user(follower):
            q = '''
            SELECT follower FROM account WHERE name = ?
            '''
            followers = self.read_db(q, (user, ))
            follower = followers[0]['follower'] + ", " + follower

            sql = '''
            UPDATE account SET follower = ? WHERE name = ?
            '''
            self.write_db(sql, (follower, user))
            query = '''
            SELECT name, follower, following FROM account WHERE name = ?
            '''
            return self.read_db(query, (user, ))
        else:
            raise Exception("Invalid user: {}".format(follower))
