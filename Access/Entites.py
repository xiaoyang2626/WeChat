import logging;
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='Entites.log',
                    filemode='a')
from bson.objectid import ObjectId
import json
import time
class Lover(object):
    def __init__(self,name=None,lover=None,ScoreDetail=[],objid=None):
        self.__id=objid
        self.__name=name
        self.__lover=lover
        self.__ScoreDetail=ScoreDetail
    @property
    def objid(self):
        return self.__id
    @objid.setter
    def objid(self,value):
        self.__id=value
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,value):
        self.__name=value
    @property
    def lover(self):
        return self.__lover
    @lover.setter
    def lover(self,value):
        self.__lover=value
    @property
    def ScoreDetail(self):
        return self.__ScoreDetail
    @ScoreDetail.setter
    def ScoreDetail(self,value):
        self.__ScoreDetail=value
    def data(self):
        if self.__id==None:
            result=({'name':self.__name,'lover':self.__lover,'ScoreDetail':self.__ScoreDetail})
            return result
        else:
            result=({'_id':ObjectId(self.__id),'name':self.__name,'lover':self.__lover,'ScoreDetail':self.__ScoreDetail})
            return result