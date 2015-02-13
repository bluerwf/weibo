import json
import ann
from time import time
from flask import request, Response
import account_handlers
import utility
#from account_handlers import AuthToken
MAX_MSG_LEN = 140

@account_handlers.AuthToken
def send_message(uuid):
    if 'X-Auth-Token' not in request.headers or \
       'Content-Type' not in request.headers or \
        request.headers['Content-Type'] != 'application/json':
        return Response(json.dumps({"error":'missing token or content-tpye'}),status =400, content_type='application/json')
    data = json.loads(request.data)
    if data['uuid'] != uuid or not data:
        return Response(json.dumps({'error':'uuid unmatched or empty data '}),
                       status=400, content_type='application/json')
    elif len(data['message']) > MAX_MSG_LEN:
        return Response(json.dumps({'error': "message length should less than {}".format(MAX_MSG_LEN)}),
                       status=403, content_type='application/json')
    else:
        body = data
        tag = utility.convert_list_to_str(data['tag'], ', ')
        body['msg_id'] = ann.app.msg.add_message(str(data['message']), tag, time(), uuid)
        return Response(json.dumps(body), status=200,
                       content_type='application/json')








