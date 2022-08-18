# -*- coding: utf-8 -*-

from django.http import HttpResponse

from hptopLib.TAPIBookingBase import TAPIBookingBase


class TAPIBooking(TAPIBookingBase):

    def getInfo(self, payment_idx, *args):
        pass

    def modifyInfo(self, *args):
        pass

    def get(self, request):
        try:
            dict = request.data
            if dict is None:
                return HttpResponse(self.json.dicToJson(self.message.errorNonePostData()))
            err, msg, body = self.getInfo(dict)
            if err == 0:
                ret = self.message.successOk()
                ret["body"] = body
                return HttpResponse(self.json.dicToJson(ret))
            else:
                return HttpResponse(self.json.dicToJson(self.message.error(msg)))
        except Exception as e:
            return self.errorInfo(e)




