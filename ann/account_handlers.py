import json
from flask import request, Response
from hashlib import md5
from weibo_exception import InvalidUser
from db import AccountDB, UserAlreadyExists, DuplicateUserException

DB = "/Users/lafengnan/codes/Github/weibo/weibo.db"
acc = AccountDB(DB)

def AuthToken(f):
    def wrapper(uuid, *args, **kargs):
        if 'X-Auth-Token'in request.headers:
            token = request.headers['X-Auth-Token']
            if token == acc.get_token(uuid)[0]['token']:
                return f(uuid, *args, **kargs)
            else:
                return Response(json.dumps({'error':'Invalid Token'}),
                           status = 401,
                           content_type='application/json')
        else:
            return Response(json.dumps({"error": "missing token"}),
                            status=400,
                           content_type="application/json")
    return wrapper

def signup():
    if 'X-User' not in request.headers or \
       'X-Pass' not in request.headers:
        return Response(json.dumps({"error":"missing user_name or password"}),
                       status=400,
                       content_type='application/json')

    user_and_pass = [request.headers.get(h) for h in ["X-User", "X-Pass"]]
    body = None
    try:
        acc.add_user(*user_and_pass)
        r = acc.get_user(user_and_pass[0])
        body = json.dumps({user_and_pass[0]:{'uuid': r[0]['uuid'],
                                             'name':r[0]['name'],
                                             'follower': r[0]['follower'],
                                             'following':r[0]['following']}})
    except UserAlreadyExists as e:
        body = json.dumps({"error": str(e)})
    return Response(body, status=200, content_type='application/json')
   
def signin():
    if 'X-User' not in request.headers or \
       'X-Pass' not in request.headers:
        return Response(json.dumps({"error":"missing user_name or PW"}),
                        status=400,content_type='application/json')
    user_and_pass = [request.headers.get(h) for h in ['X-User','X-Pass']]
    body = None
    rc = acc.get_user(user_and_pass[0])
    if rc:
        if rc[0]['passwd'] == user_and_pass[1]:
            token = md5(user_and_pass[0]).hexdigest()
            uuid = rc[0]['uuid']
            body ={'uuid':uuid,'token':token}
            acc.add_token(uuid, token)
            return Response(json.dumps(body), status=200,content_type
                           ='application/json')
        else:
            return Response(json.dumps({'error':'wrong password'}),
                    status=403, content_type='application/json')
    else:
        return Response(json.dumps({'error':'invalid user_name'}),
                       status = 404, content_type='application/json')
@AuthToken
def add_follower(uuid):
    data = json.loads(request.data)
    try:
        r = acc.add_follower(uuid, data['follower'])
        body = {'uuid':r[0]['uuid'],
                'name': r[0]['name'],
                'follower': r[0]['follower'].split(", "),
                'following': r[0]['following']
               }
        print body
        return Response(json.dumps(body), status = 200, content_type ='application/json')
    except InvalidUser as e:
        print str(e)
        return Response(json.dumps({'error': str(e)}),
                       status=404,
                       content_type="application/json")
    except DuplicateUserException as e:
        print str(e)
        return Response(json.dumps({'error': str(e)}),
                       status=403,
                       content_type="application/json")

@AuthToken
def delete_follower(uuid, follower):
    try:
        acc.delete_follower(uuid,follower)
        return Response(status = 204)
    except InvalidUser as e:
        return Response(json.dumps({'error':str(e)}),status = 404, content_type="application/json")

@AuthToken
def add_following(uuid):
    data = json.loads(request.data)
    try:
        r = acc.add_following(uuid,data['following'])
        body ={'uuid':r[0]['uuid'],
               'name':r[0]['name'],
               'follower':r[0]['follower'],
               'following':r[0]['following'].split(", ")  
        }
        return Response(json.dumps(body),status = 200, content_type ='application/json')
    except InvalidUser as e:
        print str(e)
        return Response(json.dumps({'error':str(e)}),
                        status = 404,
                        content_type = 'application/json')    
    except DuplicateUserException as e:
        print str(e)
        return Response(json.dumps({'error':str(e)}),
                        status = 403,
                        content_type = 'application/json')

@AuthToken
def detele_following(uuid, following):
    try:
        acc.delete_following(uuid, following):
        return Response(status=204)
    except InvalidUser as e:
        return Reponse(json.dumps({'error':str(e)}),
            status=404,
            content_type='/application/json')                                