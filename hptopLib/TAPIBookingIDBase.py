# -*- coding: utf-8 -*-

from abc import abstractmethod
from django.http import HttpResponse
from hptopLib.TAPIBase import TAPIBase

class TAPIBookingIDBase(TAPIBase):
    """
    HTTP 전송 공통 클래스.
    """

    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            dic = request.data
            if len(dic) < 1:
                err, msg, body = self.getInfo(partner_id)
            else:
                err, msg, body = self.getInfo(partner_id, dic)
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
            return HttpResponse(self.json.dicToJson(self.message.error(self.errorInfo(e))))

    @abstractmethod
    def getInfo(self, partner_id, *args):
        pass

    @abstractmethod
    def modifyInfo(self, *args):
        pass
