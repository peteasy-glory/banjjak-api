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
            self.errorInfo(e)
    # def get(self, request, partner_id):
    #     try:
    #         if partner_id is None:
    #             return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
    #         dic = request.data
    #         if len(dic) < 1:
    #             err, msg, body = self.getInfo(partner_id)
    #         else:
    #             err, msg, body = self.getInfo(partner_id, dic)
    #         if err == 0:
    #             ret = self.message.successOk()
    #             ret["body"] = body
    #             return HttpResponse(self.json.dicToJson(ret))
    #         else:
    #             return HttpResponse(self.json.dicToJson(self.message.error(msg)))
    #     except Exception as e:
    #         self.errorInfo(e)


    def put(self, request):
        try:
            dic = request.data
            if dic is None:
                return HttpResponse(self.json.dicToJson(self.message.errorNonePostData()))
            err, msg, body = self.putInfo(dic)
            if err == 0:
                ret = self.message.successOk()
                ret["body"] = body
                return HttpResponse(self.json.dicToJson(ret))
            else:
                return HttpResponse(self.json.dicToJson(self.message.error(msg)))
        except Exception as e:
            self.errorInfo(e)


    @abstractmethod
    def getInfo(self, payment_idx, *args):
        pass

    @abstractmethod
    def putInfo(self, *args):
        pass


    def errorInfo(self, err):
        msg = self.frameInfo(getframeinfo(currentframe()), err)
        return HttpResponse(self.json.dicToJson(self.message.error(msg)))

    def frameInfo(self, f, err):
        return "[PATH: %s, LINE: %s, FUNC: %s, ERR: %s" % (f.filename, f.lineno, f.function, err)