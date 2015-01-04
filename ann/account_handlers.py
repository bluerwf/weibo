import json
from flask import request, Response
from hashlib import md5

from db import AccountDB, UserAlreadyExists

DB = "/Users/lafengnan/codes/Github/weibo/weibo.db"

def signup():
    if 'X-User' not in request.headers or \
       'X-Pass' not in request.headers:
        return Response(json.dumps({"error":"missing user_name or password"}),
                       status=400,
                       content_type='application/json')

    acc = AccountDB(DB)
    user_and_pass = [request.headers.get(h) for h in ["X-User", "X-Pass"]]
    body = None
    try:
        acc.add_user(*user_and_pass)
        r = acc.get_user(user_and_pass[0])
        print r[0]
        body = json.dumps({user_and_pass[0]:{'uuid': r[0]['uuid'],
                                             'name':r[0]['name']}})
    except UserAlreadyExists as e:
        body = json.dumps({"error": str(e)})
    return Response(body, status=200, content_type='application/json')
   
def signin():
    if 'X-User' not in request.headers or \
       'X-Pass' not in request.headers:
        return Response(json.dumps({"error":"missing user_name or PW"}),
                        status=400,content_type='application/json')
    acc = AccountDB(DB)
    user_and_pass = [request.headers.get(h) for h in ['X-User','X-Pass']]
    body = None
    rc = acc.get_user(user_and_pass[0])
    if rc:
        if rc[0]['passwd'] == user_and_pass[1]:
            token = md5(user_and_pass[0]).hexdigest()
            uuid = rc[0]['uuid']
            body ={'uuid':uuid,'token':token}
            return Response(json.dumps(body), status=200,content_type
                           ='application/json')
        else:
            return Response(json.dumps({'error':'wrong password'}),
                    status=200, content_type='application/json')
    else:
        return Response(json.dumps({'error':'invalid user_name'}),
                       status = 404, content_type='application/json')

