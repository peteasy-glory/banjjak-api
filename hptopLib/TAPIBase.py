# -*- coding: utf-8 -*-
from abc import abstractmethod
from datetime import datetime

from rest_framework.views import APIView

from hptopLib.TDB import TDB
from hptopLib.TJson import TJson
from hptopLib.TMessage import TMessage


class TAPIBase(APIView):
    """
    기본 클래스.
    자주 사용하는 DB, JSON, MESSAGE를 정의하여
    상속된 하위 클래스에서 사용한다.
    """

    db = TDB()
    json = TJson()
    message = TMessage()

    # @abstractmethod
    # def procQuery(self, **kwargs):
    #     pass

    def queryDataToDic(self, data, rows, colums):
        if rows < 2:
            body = {}
            i = 0
            for val in data:
                if val is None:
                    body[colums[i]] = ""
                else:
                    if type(val) is datetime:
                        body[colums[i]] = val.strftime("%Y%m%d%H%M%S")
                    else:
                        body[colums[i]] = val
                i += 1
        else:
            body = []
            for d in data:
                k = {}
                i = 0
                for key in colums:
                    if d[i] is None:
                        k[key] = ""
                    else:
                        if type(d[i]) is datetime:
                            k[key] = d[i].strftime("%Y%m%d%H%M%S")
                        else:
                            k[key] = d[i]
                    i += 1
                body.append(k)
        return body

    def queryDataToSimpleDic(self, data, rows, keys):
        if rows < 2:
            body = {}
            i = 0
            for val in data:
                if val is None:
                    body[keys[i]] = ""
                else:
                    if type(val) is datetime:
                        body[keys[i]] = val.strftime("%Y%m%d%H%M%S")
                    else:
                        body[keys[i]] = val
                i += 1
        else:
            body = []
            for d in data:
                k = {}
                i = 0
                for key in keys:
                    if d[i] is None:
                        k[key] = ""
                    else:
                        if type(d[i]) is datetime:
                            k[key] = d[i].strftime("%Y%m%d%H%M%S")
                        else:
                            k[key] = d[i]
                    i += 1
                body.append(k)
        return body

    def datetimeToStr(self, dateTime, format):
        return datetime(dateTime).striftime(format)
