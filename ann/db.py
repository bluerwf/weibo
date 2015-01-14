import sqlite3
import uuid
from weibo_exception import InvalidUser, UserAlreadyExists, DuplicateUserException


def debug(f):
    def wrapper(*args, **kargs):
        print f.__name__, args, kargs
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
        following   TEXT,
        token TEXT
        )
        '''
        self.write_db(sql)
        
    def is_user_existing(self, user):
        query = '''
        SELECT name FROM account WHERE name = ?
        '''
        r = self.read_db(query, (user, ))
        return True if r else False

    def is_follower_existing(self, uuid, follower):
        query = '''
        SELECT follower FROM account WHERE uuid = ?
        '''
        r = self.read_db(query, (uuid, ))
        if r[0]['follower'] and follower in r[0]['follower'].split(", "):
            return True
        else:
            return False

    def is_following_existing(self, uuid, following):
        query = '''
        SELECT following FROM account WHERE uuid = ?
        '''
        r = self.read_db(query, (uuid, )) 
        if r[0]['following'] and following in r[0][following].split(', '):
            return True
        else:
            return False           

    def add_user(self, username, pw):
        if not self.is_user_existing(username):
            sql = '''
            INSERT INTO account VALUES (?,?,?,?,?,?)
            '''
            uid = str(uuid.uuid4()) 
            self.write_db(sql, (uid, username, pw, None, None, None))
        else:
            raise UserAlreadyExists(username) 

    def get_user(self, user):
        query = '''
        SELECT * FROM account WHERE name = ?
        '''
        return self.read_db(query, (user, ))

    def get_user_by_uuid(self, uuid):
        query = '''
        SELECT name FROM account WHERE uuid = ?
        '''
        return self.read_db(query, (uuid,))
    
    def add_follower(self, uuid, follower):
        if self.get_user_by_uuid(uuid)[0]['name'] == follower or self.is_follower_existing(uuid, follower):
            raise DuplicateUserException(follower)
        if self.get_user(follower):
            q = '''
            SELECT follower FROM account WHERE uuid = ?
            '''
            followers = self.read_db(q, (uuid, ))
            if followers[0]['follower']:
                follower = followers[0]['follower'] + ", " + follower
            sql = '''
            UPDATE account SET follower = ? WHERE uuid = ?
            '''
            self.write_db(sql, (follower, uuid))
            query = '''
            SELECT uuid, name, follower, following FROM account WHERE uuid = ?
            '''
            return self.read_db(query, (uuid, ))
        else:
            raise InvalidUser(follower)
     
    def delete_follower(self, uuid, follower):
        if self.get_user(follower):
            q = '''
            SELECT follower FROM account WHERE uuid = ?
            '''
            followers = self.read_db(q, (uuid, ))[0]['follower']
            if followers:
                follower = followers.split(', ').remove(follower)
                sql = '''
                UPDATE account SET follower=? WHERE uuid = ?
                '''
                follower = None if not follower else reduce(lambda f1, f2: f1 + ', ' + f2, follower)
                self.write_db(sql, (follower, uuid))
        else:
            raise InvalidUser(follower)

    def add_token(self, uuid, token):
         sql = '''
         UPDATE account SET token = ? WHERE uuid = ?
         
         '''
         self.write_db(sql,(token, uuid))
    def get_token(self, uuid):
        q = '''
         SELECT token FROM account WHERE uuid = ?
        '''
        return self.read_db(q,(uuid, ))

    def add_following(self, uuid, following):
        if self.get_user_by_uuid(uuid)[0]['name'] == following or self.is_following_existing(uuid, following):
            raise DuplicateUserException(following)
        if self.get_user(following):
            q = '''
                       SELECT following FROM account WHERE uuid = ?
             '''   
            followings = self.read_db(q, (uuid, ))
            if followings[0]['following']:
                following = followings[0]['following'] + ', '+following
                sql ='''
                UPDATE account SET following = ? WHERE uuid = ?
                '''
                self.write_db(sql,(following, uuid)) 
                query ='''
                SELECT uuid, name, follower, following FROM account WHERE uuid = ?
                '''
                return self.read_db(query,(uuid, ))
        else:
            raise InvalidUser(following)         

     def delete_following(self, uuid, following):
        if self.get_user(following):
            q = '''
            SELECT following FROM account WHERE uuid = ?
            '''
            followings = self.read_db(q, (uuid, ))[0]['following']
            if followings:
                following = followings.split(', ').remove(following)
                sql = '''
                UPDATE account SET follower=? WHERE uuid = ?
                '''
                following = None if not following else reduce(lambda f1, f2: f1 + ', ' + f2, following)
                self.write_db(sql, (following, uuid))
        else:
            raise InvalidUser(following)



