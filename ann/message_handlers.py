import json
from flask import request, Response
import account_handlers
#from account_handlers import AuthToken
@account_handlers.AuthToken
def send_message(uuid):
    if 'X-Auth-Token' not in request.headers or \
       'Content-Type' not in request.headers or \
        request.headers['Content-Type'] != 'application/json':
        return Response(json.dumps({"error":'missing token or content-tpye'}),status =400, content_type='application/json')
    data=json.loads(request.data)
    if data[uuid]!=uuid or data== {}:
        return Response(json.dumps({'error':'uuid in not the same'}),
                       status =400, content_type='application/json')





