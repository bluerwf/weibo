import uuid
from hashlib import md5
import db

class Account:
    def __init__(self, username, pw, *arg, **karg):
        self.username = username 
        self.pw = pw
        self.uuid = None
        self.following = []
        self.follower = []
        self.db = db.Database()

    def signup(self):
        """
        The account is stored in a RDBMS table:
        CREATE TABLE account (
        uuid text PRIMARY KEY,
        usernmae varchar(20),
        passwd text
        )
        """
        self.uuid = uuid.uuid4(self.username)
        self.db.write_db(self.uuid)
    def _get_uuid(self):
        """
        SELECT uuid from account WHERE username = '%s' % self.username
        """
        return self.db.read_db(self.username)

    def _get_token(self):
        """
        token = md5(username).hexdigest()
        """
        return md5(self.name).hexdigest()

    def login(self):
        """
        SELECT username, decrypted(passwd) as passwd From
        account WHERE username = '%s' % self.username
        """
        user_and_passwd = self.db.read_db(self.username, self.pw)
        if not user_and_passwd:
            raise Exception("User: %s not exists!" % self.username)
        else:
            if user_and_passwd[1] != self.pw:
                raise Exception("User: %s login with wrong password" % self.username)
            else:
                self.uuid = self._get_uuid()
                token = self._get_token()
                return self.uuid, token


