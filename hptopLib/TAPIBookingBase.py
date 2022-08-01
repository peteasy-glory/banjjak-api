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
            frame_info = getframeinfo(currentframe())
            msg = "[PATH: %s, LINE: %s, FUNC: %s, ERR: %s" % (frame_info.filename, frame_info.lineno, frame_info.function, e.args[0])
            return HttpResponse(self.json.dicToJson(self.message.error(msg)))

    @abstractmethod
    def getInfo(self, payment_idx, *kwargs):
        pass