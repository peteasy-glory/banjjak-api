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
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PEROID_GET_OPT % (partner_id, st_date, fi_date), QUERY_DB)
                data = []
                if rows < 2:
                    data.append(value)
                else:
                    data = value
                if value is not None:
                    for d in data:
                        body.append(self.setBeautyData(d))
            else:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            ret = self.message.successOk()
            ret["body"] = body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(self.errorInfo(e))))

class TBookingCount(TAPIBase):

    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            body = []
            if request.GET.get('st_date') is not None and request.GET.get('fi_date') is not None:
                st_date = request.GET.get('st_date')
                fi_date = request.GET.get('fi_date')
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_COUNT_GET % (partner_id, st_date, fi_date), QUERY_DB)
                data = []
                if rows < 2:
                    data.append(value)
                else:
                    data = value
                if value is not None:
                    cnt = []
                    for d in data:
                        tmp = {"date": d[0], "count": d[1]}
                        cnt.append(tmp)
                    body.append(cnt)
                value, rows, columns = self.db.resultDBQuery(
                    PROC_BEAUTY_BOOKING_PAY_COUNT_GET % (partner_id, st_date, fi_date), QUERY_DB)
                data = []
                if rows < 2:
                    data.append(value)
                else:
                    data = value
                if value is not None:
                    for d in data:
                        tmp = {"card_price": d[0], "cash_price": d[1]}
                        body.append(tmp)
                value, rows, columns = self.db.resultDBQuery(
                    PROC_BEAUTY_BOOKING_PETTYPE_COUNT_GET % (partner_id, st_date, fi_date), QUERY_DB)
                data = []
                if rows < 2:
                    data.append(value)
                else:
                    data = value
                if value is not None:
                    for d in data:
                        tmp = {"dog_cnt": d[0], "cat_cnt": d[1]}
                        body.append(tmp)
            else:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            ret = self.message.successOk()
            ret["body"] = body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(self.errorInfo(e))))

class TBookingPetPay(TAPIBase):

    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            body = []
            if request.GET.get('st_date') is not None and request.GET.get('fi_date') is not None:
                st_date = request.GET.get('st_date')
                fi_date = request.GET.get('fi_date')
                value, rows, columns = self.db.resultDBQuery(
                    PROC_BEAUTY_BOOKING_PAY_COUNT_GET % (partner_id, st_date, fi_date), QUERY_DB)
                data = []
                if rows < 2:
                    data.append(value)
                else:
                    data = value
                if value is not None:
                    for d in data:
                        tmp = {"card_price": d[0], "cash_price": d[1]}
                        body.append(tmp)
                value, rows, columns = self.db.resultDBQuery(
                    PROC_BEAUTY_BOOKING_PETTYPE_COUNT_GET % (partner_id, st_date, fi_date), QUERY_DB)
                data = []
                if rows < 2:
                    data.append(value)
                else:
                    data = value
                if value is not None:
                    for d in data:
                        tmp = {"pet_type": d[0], "pet_cnt": d[1]}
                        body.append(tmp)
            else:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            ret = self.message.successOk()
            ret["body"] = body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(self.errorInfo(e))))














