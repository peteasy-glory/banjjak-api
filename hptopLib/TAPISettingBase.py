# -*- coding: utf-8 -*-
from abc import abstractmethod
from inspect import getframeinfo, currentframe
from django.http import HttpResponse

from hptopLib.TAPIBase import TAPIBase


class TAPISettingBase(TAPIBase):
    """
    설정 기본 클래스.
    """

    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            err, msg, body = self.getInfo(partner_id)
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
    def getInfo(self, partner_id):
        pass

