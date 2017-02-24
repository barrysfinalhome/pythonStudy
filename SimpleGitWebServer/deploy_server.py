# -*- coding: utf8 -*-
from werkzeug.routing import PathConverter
from flask import Flask, jsonify, request, Response;
from flask_sockets import Sockets
import gevent
from git import Git

app = Flask(__name__)
sockets = Sockets(app)

PROJECT_DIR = '/home/app/project/project_name'
REMOTE_NAME = 'ssh'
WS = None

def send(message):
    if WS:
        WS.send(message)

class EverythingConverter(PathConverter):
    regex = '.*?'

app.url_map.converters['everything'] = EverythingConverter

@app.route('/')
def index():
    content = open('index.html').read()
    return Response(content, mimetype="text/html")

@app.route('/branch/<everything:branch_name>')
def branch(branch_name):
    # branch_name = 'remotes/ssh/' + branch_name
    g = Git(PROJECT_DIR)
    send('重新获取远程分支中.....')
    g.fetch(REMOTE_NAME)
    send('获取成功')
    branch_names = g.branch('-a').split('\n')
    branch_names = [_.strip() for _ in branch_names]
    if branch_name not in branch_names:
        return '你的这个branch啊，鹅母鸡鸭'
    try:
        send('重置分支')
        g.reset('--hard')
        send('切换分支中')
        g.checkout(branch_name)
        send('切换分支完成')
    except Exception as e:
        return str(e)
    return branch_name

@app.route('/branches')
def branches():
    g = Git(PROJECT_DIR)
    send('重新获取远程分支中.....')
    g.fetch(REMOTE_NAME)
    send('获取成功')
    branch_names = g.branch('-a').split('\n')
    return jsonify(branch_names)

@sockets.route('/console')
def console_socket(ws):
    global WS
    WS = ws
    while True:
        gevent.sleep(10)
    #     try:
    #         send(message)
    #     except Exception as e:
    #         send('11111')
    #         gevent.sleep(3)

if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer
    from geventwebsocket.handler import WebSocketHandler
    http_server = WSGIServer(('0.0.0.0', 54321), app, handler_class=WebSocketHandler)
    http_server.serve_forever()

