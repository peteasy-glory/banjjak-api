# -*- coding: utf-8 -*-
from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_BEAUTY_BOOKING_PET_TYPE_GET
from hptopLib.TAPIBase import TAPIBase


class TPetType(TAPIBase):
    def get(self, request):
        try:
            if request.GET.get('animal') is not None:
                if request.GET.get('animal') != "dog" and request.GET.get('animal') != "cat":
                    return HttpResponse(self.json.dicToJson(self.message.errorParametaRequst()))
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PET_TYPE_GET % (request.GET.get('animal'),), QUERY_DB)
                ret = self.message.successOk()
                if value is None:
                    ret["body"] = {}
                    return HttpResponse(self.json.dicToJson(ret))
            ret["body"] = self.queryDataToDic(value, rows, columns)
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            msg = self.errorInfo(e)
            return HttpResponse(self.json.dicToJson(self.message.error(msg)))