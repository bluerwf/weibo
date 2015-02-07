import json
from flask import request, Response
from hashlib import md5
from weibo_exception import InvalidUser, Invaliduuid
from db import UserAlreadyExists, DuplicateUserException
from utility import convert_str_to_list
import ann

def AuthToken(f):
    def wrapper(uuid, *args, **kargs):
        if 'X-Auth-Token'in request.headers:
            token = request.headers['X-Auth-Token']
            if token == ann.app.acc.get_token(uuid)[0]['token']:
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
        ann.app.acc.add_user(*user_and_pass)
        r = ann.app.acc.get_user(user_and_pass[0])
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
    rc = ann.app.acc.get_user(user_and_pass[0])
    if rc:
        if rc[0]['passwd'] == user_and_pass[1]:
            token = md5(user_and_pass[0]).hexdigest()
            uuid = rc[0]['uuid']
            body ={'uuid':uuid,'token':token}
            ann.app.acc.add_token(uuid, token)
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
        r = ann.app.acc.add_follower(uuid, data['follower'])
        body = {'uuid':r[0]['uuid'],
                'name': r[0]['name'],
                'follower': convert_str_to_list(r[0]['follower'],', '),
                'following': convert_str_to_list(r[0]['following'],', ')
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
        ann.app.acc.delete_follower(uuid,follower)
        return Response(status = 204)
    except InvalidUser as e:
        return Response(json.dumps({'error':str(e)}),status = 404, content_type="application/json")

@AuthToken
def add_following(uuid):
    data = json.loads(request.data)
    try:
        r = ann.app.acc.add_following(uuid,data['following'])
        body ={'uuid':r[0]['uuid'],
               'name':r[0]['name'],
               'follower':convert_str_to_list(r[0]['follower'],', '),
               'following':convert_str_to_list(r[0]['following'],', ')
        }
        return Response(json.dumps(body),status = 200, content_type ='application/json')
    except InvalidUser as e:
        return Response(json.dumps({'error':str(e)}),
                        status = 404,
                        content_type = 'application/json')
    except DuplicateUserException as e:
        return Response(json.dumps({'error':str(e)}),
                        status = 403,
                        content_type = 'application/json')

@AuthToken
def delete_following(uuid, following):
    try:
        ann.app.acc.delete_following(uuid, following)
        return Response(status=204)
    except InvalidUser as e:
        return Response(json.dumps({'error':str(e)}),
            status=404,
            content_type='/application/json')

@AuthToken
def delete_account(uuid):
    try:
        ann.app.acc.delete_account(uuid)
        return Response(status=204)
    except Invaliduuid as e:
        return Response(json.dumps({'error':str(e)}),
                       status=404,
                       content_type='/application/json')

def get_user_info(uuid):
    r = ann.app.acc.get_user_info(uuid)
    if r:
        follower = r[0]['follower']
        following = r[0]['following']

        print "debug: {}".format(following)

        body = {'uuid':r[0]['uuid'],
                'name':r[0]['name'],
                'follower':convert_str_to_list(follower, ', '),
                'following':convert_str_to_list(following, ', ')
               }
        return Response(json.dumps(body),status =200,content_type
                   ='application/json')
    else:
        return Response(json.dumps({'error':'Invalid uuid{%s}'%uuid}),
                       status=404,
                       content_type='application/json')

def get_user_list():
    users={}
    """
    {
    'uuid': {
    'name': 'ann',
    'follower': ["chris"]
    'following': []
    }
    }"""
    uuids = ann.app.acc.get_all_uuid()
    for r in uuids:
        uuid = r['uuid']
        user = ann.app.acc.get_user_info(uuid)[0]
        users[uuid] = {"name": user['name'],
                       "follower": convert_str_to_list(user['follower'], ', '),
                       "following": convert_str_to_list(user['following'], ', ')
                      }

    return Response(json.dumps(users),
                   status=200,
                   content_type="application/json")
