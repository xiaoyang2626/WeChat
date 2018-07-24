import os
import time
import json
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='app.log',
                    filemode='a')
import Access.Entites

import xmltodict
import Access.weixin
from flask import Flask, request, render_template, redirect, url_for, escape, session, jsonify
from flask_socketio import SocketIO,send,emit,join_room,leave_room
from gevent import monkey,_socket3
from gevent.pywsgi import WSGIServer
monkey.patch_all()
app = Flask(__name__)
app.config['DEBUG'] = True
# app.config['SECRET_KEY']='secret!'
app.secret_key = os.urandom(12)
socketio=SocketIO(app)

@socketio.on('message')
def socketio_message(message):
    print('收到消息',message)
    send('holloworld')
@socketio.on('join')
def on_join(data):
    username=data['username']
    print(request.sid)
    join_room('uid')
    print('收到的信息',data['username'])
    send('Thank you')

@app.route('/', methods=['GET'])
def home():
    return render_template('helloword.html')
@app.route('/info/<number>',methods=['GET'])
def info(number):
    return render_template('info'+number+'.html')

@app.route('/hudong', methods=['GET'])
def hudong():
    return render_template('index.html')


@app.route('/wechat', methods=['POST'])
def GetMessage():
    # dictdata=json.loads(json.dumps(xmltodict.parse(request.data)))
    # # dictdata=json.loads(json.dumps(xmltodict.parse(request.form['body'])))
    # print(dictdata['xml']['ToUserName'])
    # print(dictdata['xml']['FromUserName'])
    # print(dictdata['xml']['CreateTime'])
    # print(dictdata['xml']['MsgType'])
    # print(dictdata['xml']['Content'])
    # print(dictdata['xml']['MsgId'])
    # result = {'xml': {'ToUserName': dictdata['xml']['FromUserName'], 'FromUserName': dictdata['xml']['ToUserName'], 'CreateTime': str(
    #     int(round(time.time() * 1000))), 'MsgType': 'text', 'Content': 'Hello World'}}
    # print(xmltodict.unparse(result))

    msg = Access.weixin.message(request.data)

    msg.receive()

    return msg.answer()


@app.route('/wechat', methods=['GET'])
def auth():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    wxsign = Access.weixin.sign()
    result = wxsign.authtoken(str(signature), str(
        timestamp), str(nonce), str(echostr))
    print('result' + str(result))

    # return render_template('weixinsign.html',signature=signature)
    return result


@app.route('/testwechat', methods=['GET'])
def testauth():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    wxsign = Access.weixin.sign()
    result = wxsign.authtoken(str(signature), str(
        timestamp), str(nonce), str(echostr))
    print('result' + str(result))

    # return render_template('weixinsign.html',signature=signature)
    return result


@app.route('/addlover', methods=['GET'])
def addloverpage():
    return render_template('addlover.html')


@app.route('/addlove', methods=['POST'])
def addlover():
    try:
        data=request.get_json()
        name=data['name']
        lover=data['lover']
        loveEntity = Access.Entites.Lover(name=name, lover=lover)
        loveAccess = Access.weixin.LoverAccess()
        result = loveAccess.AddLover([loveEntity])
    except Exception as ex:
        logging.error(ex)
        return jsonify({'type': 1011, 'message': 'Not found ' + str(ex)})
    else:
        if result['type'] == 200:
            return jsonify({'type': 200, 'message': 'success', 'content': result['message']})
        else:
            return jsonify({'type': result['type'], 'message': result['message']})


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8080), app)
    # socketio.run(app)
    print('yiqidong')
    http_server.serve_forever()
