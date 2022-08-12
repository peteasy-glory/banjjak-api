# -*- coding: utf-8 -*-
from abc import abstractmethod
from inspect import getframeinfo, currentframe
from django.http import HttpResponse

from hptopLib.TAPIBase import TAPIBase


class TAPIBookingBase(TAPIBase):
    """
    HTTP 전송 공통 클래스.
    """

    def get(self, request, payment_idx):
        try:
            if payment_idx is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            dic = request.data
            if len(dic) < 1:
                err, msg, body = self.getInfo(payment_idx)
            else:
                err, msg, body = self.getInfo(payment_idx, dic)
            if err == 0:
                ret = self.message.successOk()
                ret["body"] = body
                return HttpResponse(self.json.dicToJson(ret))
            else:
                return HttpResponse(self.json.dicToJson(self.message.error(msg)))
        except Exception as e:
            return self.errorInfo(e)

    def post(self, request):
        return self.modify(request)

    def put(self, request):
        return self.modify(request)


    def modify(self, request):
        try:
            dict = request.data
            if dict is None:
                return HttpResponse(self.json.dicToJson(self.message.errorNonePostData()))

            err, msg, body = self.modifyInfo(dict)
            if err == 0:
                ret = self.message.successOk()
                ret["body"] = body
                return HttpResponse(self.json.dicToJson(ret))
            elif err == 408:
                return HttpResponse(self.json.dicToJson(self.message.errorNoEnoughPostData()))
            else:
                return HttpResponse(self.json.dicToJson(self.message.error(msg)))
        except Exception as e:
            return self.errorInfo(e)

    @abstractmethod
    def getInfo(self, payment_idx, *args):
        pass

    @abstractmethod
    def modifyInfo(self, *args):
        pass


    # def frameInfo(self, f, err):
    #     return "[PATH: %s, LINE: %s, FUNC: %s, ERR: %s" % (f.filename, f.lineno, f.function, err)

