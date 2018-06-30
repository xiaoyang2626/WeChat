#coding:utf-8
import re
import time
import json
import hashlib
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(clientip)s %(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='weixin.log',
                    filemode='a')
import pinyin
import xmltodict
from bson.objectid import ObjectId
import EntityAccess.Entites
# import Entites
from EntityAccess.mongo import Dao
# from mongo import Dao
# APPSecret='a243dcea5386e1842a0069e4bc0bd2ad'


class sign(object):
    #服务器信息验证接收信息[signature,timestamp,nonce,echostr]
    def authtoken(self, signature, timestamp, nonce, echostr):
        try:
            data = ['15900253421xiaoyangYHC', timestamp, nonce]
            data.sort()
            # sha1 = hashlib.sha1()
            # for item in data:
            #     sha1.update(item.encode('utf-8'))
            # hashcode = sha1.hexdigest()
            # if hashcode == signature:
            #     return echostr
            # else:
            #     return ''
            data2 = ''.join(data)
            sha1 = hashlib.sha1()
            sha1.update(data2.encode('utf-8'))
            hashcode = sha1.hexdigest()
            if hashcode == signature:
                return echostr
            else:
                return ''
        except Exception as ex:
            logging.error(str(ex))


class message(object):
    '消息处理'

    def __init__(self, xml):
        self.__dicdata = json.loads(json.dumps(xmltodict.parse(xml)))
        self.__ToUserName = self.__dicdata['xml']['ToUserName']
        self.__FromUserName = self.__dicdata['xml']['FromUserName']
        self.__CreateTime = self.__dicdata['xml']['CreateTime']
        self.__MsgType = self.__dicdata['xml']['MsgType']
        self.__MsgId = self.__dicdata['xml']['MsgId']

    def receive(self):
        if self.__MsgType == 'text':
            self.__Content = self.__dicdata['xml']['Content']
        elif self.__MsgType == 'voice':
            self.__Recognition = self.__dicdata['xml']['Recognition']

    def getDicdata(self):
        return self.__dicdata

    def answer(self):
        try:
            if self.__MsgType == 'text':
                print('text:' + self.__Content)
                if re.search('廖英强', self.__Content):
                    resultxml = {'xml': {
                        'ToUserName': self.__FromUserName,
                        'FromUserName': self.__ToUserName,
                        'CreateTime': str(int(round(time.time() * 1000))),
                        'MsgType': 'news',
                        'ArticleCount': 1,
                        'Articles': {
                            'item': {
                                'Title': '廖英强解盘',
                                'Description': '廖英强解盘',
                                'PicUrl': 'http://www.zhangwocj.com/static/images/video_sort_01.png',
                                'Url': 'http://www.zhangwocj.com/video1?uid=599172f178a8051cd2b111a4&key=111&live_id=598c213aa2fea4f51978e0de&title=%E5%BB%96%E8%8B%B1%E5%BC%BA%E8%80%81%E5%B8%88%E6%AF%8F%E6%97%A5%E8%A7%A3%E7%9B%98'
                            }
                        }
                    }}
                    return xmltodict.unparse(resultxml)

        except Exception as ex:
            logging.error(str(ex))

        try:
            if self.__MsgType == 'voice':
                print('voice:' + self.__Recognition)
                if re.search('liaoyingqiang', pinyin.get(self.__Recognition, format="strip", delimiter='')):
                    result = {'xml': {
                        'ToUserName': self.__FromUserName,
                        'FromUserName': self.__ToUserName,
                        'CreateTime': str(int(round(time.time() * 1000))),
                        'MsgType': 'news',
                        'ArticleCount': 1,
                        'Articles': {
                            'item': {
                                'Title': '廖英强解盘',
                                'Description': '廖英强解盘',
                                'PicUrl': 'http://www.zhangwocj.com/static/images/video_sort_01.png',
                                'Url': 'http://www.zhangwocj.com/video1?uid=599172f178a8051cd2b111a4&key=111&live_id=598c213aa2fea4f51978e0de&title=%E5%BB%96%E8%8B%B1%E5%BC%BA%E8%80%81%E5%B8%88%E6%AF%8F%E6%97%A5%E8%A7%A3%E7%9B%98'
                            }
                        }
                    }}

                    return xmltodict.unparse(result)
        except Exception as ex:
            logging.error(str(ex))

        return 'success'


class LoverAccess(object):
    def __init__(self):
        self.__LoverDao = Dao('lover')

    def ExitLover(self, name=None, lid=None):
        if name != None:
            try:
                result = self.__LoverDao.select({'name': name}).data()
                self.__LoverDao.close()
            except Exception as ex:
                logging.error(ex)
                self.__LoverDao.close()
                return {'type': 7001, 'message': str(ex)}
            else:
                if len(result) != 0:
                    return {'type': 200, 'message': result[0]}
                else:
                    return {'type': 7002, 'message': 'not found this name'}
        elif lid != None:
            try:
                result = self.__LoverDao.select({'_id': ObjectId(lid)}).data()
                self.__LoverDao.close()
            except Exception as ex:
                logging.error(ex)
                self.__LoverDao.close()
                return {'type': 7001, 'message': str(ex)}
            else:
                if len(result) != 0:
                    return {'type': 200, 'message': result[0]}
                else:
                    return {'type': 7003, 'message': 'not found this lid'}
        else:
            return {'type': 7004, 'message': 'name and lid not is null'}

    def AddLover(self, ListLoverEntity):
        try:
            data = []
            for dic in ListLoverEntity:
                r = dic.data()
                data.append(r)
            result = self.__LoverDao.insert(data)
        except Exception as ex:
            logging.error(ex)
            self.__LoverDao.close()
            return {'type': 7005, 'message': '添加失败'}
        else:
            self.__LoverDao.close()
            print(result)
            if type(result) == type(data):
                for index, el in enumerate(result):
                    result[index] = str(el)
                self.__LoverDao.close()
                return {'type': 200, 'message': result}

    def insertScore(self, datetime, event, score, lovername, pic=''):
        diclover = ExitLover(name=lovername)
        if diclover['type'] == 200:
            lover = diclover['message']
            le = EntityAccess.Entites.Lover()
            le.objid = lover['_id']
            le.name = lover['name']
            le.lover = lover['lover']
            temptime = time.localtime(datetime)
            tempdic = {'year': temptime.tm_year, 'score': score, 'pic': pic,
                       'month': temptime.tm_mon, 'day': temptime.tm_mday, 'event': event}
            templist = lover['ScoreDetail']
            templist.append(tempdic)
            le.scoredetail = templist
            self.__LoverDao = Dao('lover')
            dicup = updateLover([le])
            if dicup['type'] == 200:
                return {'type': 200, 'message': dicup['message']}
            else:
                return {'type': 7006, 'message': dicup['message']}
        else:
            return {'type': 7007, 'message': diclover['message']}

    def updateLover(self, ListLoverEntity):
        try:
            result = []
            for dic in ListVideoEntity:
                if self.__LoverDao.update({'_id': ObjectId(dic.objid)}, dic.updata()) == 1:
                    result.append(dic.objid)
        except Exception as ex:
            logging.error(ex)
            self.__LoverDao.close()
            return {'type': 7010, 'message': 'update fail'}
        else:
            self.__LoverDao.close()
            if result == []:
                return {'type': 7011, 'message': 'Not found this Lover'}
            else:
                return {'type': 200, 'message': result}
