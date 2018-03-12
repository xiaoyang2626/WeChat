import os
import time
import json
import logging;
logging.basicConfig(level=logging.DEBUG,
                    format='%(clientip)s %(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='app.log',
                    filemode='a')

import EntityAccess.weixin

import xmltodict
from flask import Flask, request, render_template, redirect, url_for, escape, session, jsonify
from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = os.urandom(12)


@app.route('/', methods=['GET'])
def home():
    return render_template('helloword.html')


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
    
    msg=EntityAccess.weixin.message(request.data)
    print(msg.getDicdata())
    msg.receive()
    return msg.answer()
@app.route('/wechat', methods=['GET'])
def auth():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    wxsign = EntityAccess.weixin.sign()
    result = wxsign.authtoken(str(signature), str(timestamp), str(nonce), str(echostr))
    print('result'+str(result))

    # return render_template('weixinsign.html',signature=signature)
    return result

if __name__ == '__main__':
    http_server=WSGIServer(('0.0.0.0', 8080), app)
    print('yiqidong')
    http_server.serve_forever()
