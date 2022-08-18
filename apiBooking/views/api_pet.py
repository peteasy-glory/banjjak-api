# -*- coding: utf-8 -*-
import string
import traceback

from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_BEAUTY_BOOKING_PET_TYPE_GET, PROC_BEAUTY_BOOKING_PET_INFO_GET, \
    PROC_BEAUTY_BOOKING_PET_INFO_PUT
from hptopLib.TAPIBase import TAPIBase
from hptopLib.TAPIBookingBase import TAPIBookingBase


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
            else:
                return HttpResponse(self.json.dicToJson(self.message.errorParametaRequst()))
        except Exception as e:
            msg = self.errorInfo(e)
            return HttpResponse(self.json.dicToJson(self.message.error(msg)))


class TPetInfo(TAPIBookingBase):
    def modifyInfo(self, *args):
        try:
            qry = PROC_BEAUTY_BOOKING_PET_INFO_PUT % (
                  args[0]["idx"],
                  args[0]["name"],args[0]["type"], args[0]["pet_type"],
                  args[0]["year"], args[0]["month"], args[0]["day"],
                  args[0]["gender"],
                  args[0]["neutral"],
                  args[0]["weight"], args[0]["beauty_exp"], args[0]["vaccination"], args[0]["luxation"],
                  args[0]["bite"],
                  args[0]["dermatosis"], args[0]["heart_trouble"], args[0]["marking"], args[0]["mounting"],
                  args[0]["etc"])
            if args[1] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(qry, QUERY_DB)
                return 0, "success", self.queryDataToDic(value, rows, columns)
        except Exception as err:
            return -1, traceback.format_exc(), None

    def getInfo(self, idx, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PET_INFO_GET % (idx,), QUERY_DB)
            body =self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None