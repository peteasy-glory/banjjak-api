# -*- coding: utf-8 -*-
import traceback

from django.http import HttpResponse
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase

class TBooking(TAPIBase):

    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            body = []
            if request.GET.get('st_date') is not None and request.GET.get('fi_date') is not None:
                st_date = request.GET.get('st_date')
                fi_date = request.GET.get('fi_date')
                value, rows, columns = self.db.resultDBQuery(PROC_HOTEL_BOOKING_PEROID_GET_OPT % (partner_id, st_date, fi_date), QUERY_DB)
                data = []
                if rows < 2:
                    data.append(value)
                else:
                    data = value
                if value is not None:
                    for d in data:
                        body.append(self.setHotelData(d))
            else:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            ret = self.message.successOk()
            ret["body"] = body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(self.errorInfo(e))))















