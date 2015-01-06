class UserAlreadyExists(Exception):
    def __init__(self,user):
        self.user = user
    def __str__(self):
        return "User: {user} already exists.".format(user=self.user)

class InvalidUser(Exception):
    def __init__(self,user):
        self.user = user
    def __str__(self):
        return "User:{user} do not exist".format(user=self.user) 

class DuplicateUserException(Exception):
    def __init__(self,user):
        self.user = user
    def __str__(self):
        return "Can not operate on User:{user}".format(user=self.user) 


        

