# -*- coding: utf-8 -*-
from abc import abstractmethod
from inspect import getframeinfo, currentframe
from django.http import HttpResponse

from hptopLib.TAPIBookingBase import TAPIBookingBase


class TAPICustomerBase(TAPIBookingBase):
    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))

            if request.GET.get('type') is not None:
                if request.GET.get('type') in ('beauty', 'hotel', 'kinder', 'people','animal'):
                    if request.GET.get('type') in ('people','animal'):
                        err, msg, body = self.getInfo(partner_id, request.GET.get('type'))
                    elif request.GET.get('pet') is not None:
                        err, msg, body = self.getInfo(partner_id, request.GET.get('type'), request.GET.get('pet'))
                    elif request.GET.get('ord_type') is not None:
                        err, msg, body = self.getInfo(partner_id, request.GET.get('type'), request.GET.get('ord_type'))
                    else:
                        HttpResponse(self.json.dicToJson(self.message.errorParametaRequst()))
                    if err == 0:
                        ret = self.message.successOk()
                        ret["body"] = body
                        return HttpResponse(self.json.dicToJson(ret))
                    else:
                        return HttpResponse(self.json.dicToJson(self.message.error(msg)))
            return HttpResponse(self.json.dicToJson(self.message.errorParametaRequst()))
        except Exception as e:
            return self.errorInfo(e)



