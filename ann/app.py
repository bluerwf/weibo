#! /usr/bin/env python
# coding=utf-8

from flask import Flask, Response, request
import json
import account_handlers
import message_handlers
from wsgi import Weibo

app = Weibo(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    #return {'hello': 'world'}
    return _hello()

@app.route('/hello/<id>', methods=['GET'])
def hello_id(id):
    return Response(json.dumps({"id":id}),
                   status=200,
                   content_type="application/json")

#@app.route('/filelist', methods=['GET'])
#def get_files():
#    return  _get_files()

@app.route('/weibo/signup', methods=['POST'])
def signup():
    return account_handlers.signup()

@app.route('/weibo/signin',methods=['POST'])
def signin():
    return account_handlers.signin()

@app.route('/weibo/user/<uuid>',methods=['DELETE'])
def delete_account(uuid):
    return account_handlers.delete_account(uuid)

@app.route('/weibo/<uuid>/follower',methods=['POST'])
def add_follower(uuid):
    return account_handlers.add_follower(uuid)

@app.route('/weibo/<uuid>/follower/<name>',methods=['DELETE'])
def delete_follower(uuid,name):
    return account_handlers.delete_follower(uuid,name)

@app.route('/weibo/<uuid>/following',methods=['POST'])
def add_following(uuid):
    return account_handlers.add_following(uuid)

@app.route('/weibo/<uuid>/following/<name>',methods=['DELETE'])
def delete_following(uuid, name):
    return account_handlers.delete_following(uuid, name)

@app.route('/weibo/user/<uuid>/info',methods=['GET'])
def get_user_info(uuid):
    return account_handlers.get_user_info(uuid)

@app.route('/weibo/users',methods=['GET'])
def get_user_list():
    return account_handlers.get_user_list()

@app.route('/weibo/timeline/<uuid>',methods=['PUT'])
def send_message(uuid):
    return message_handlers.send_message(uuid)

@app.route('/ping', methods=['PUT'])
def ping():
    return _ping()

def _ping():
    data = json.loads(request.data)
    return Response(json.dumps(data),
                   status=200,
                    content_type="application/json")
def _hello():
    body = {'msg': 'hello world'}
    return Response(json.dumps(body),
                   status=200,
                   content_type="application/json")
def _get_files():
    if 'X-Path' not in request.headers or \
       'X-Suffix' not in request.headers:
        return Response(json.dumps({'error':"x-Path or X-Suffix missing!"}),
                        status=400,
                       content_type='application/json')
    path = request.headers['X-Path']
    suffix = request.headers['X-Suffix']
    f = File(path, suffix)
    flist = f.filelist()
    response = Response(json.dumps({path:flist}),
                       status=200,
                       content_type="application/json")
    return response

if __name__ == '__main__':
    app.run()

