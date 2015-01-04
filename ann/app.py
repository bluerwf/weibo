#! /usr/bin/env python
# coding=utf-8

from flask import Flask, Response, request
import json
import account_handlers

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
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
