# -*- coding: utf-8 -*-
import traceback

from django.http import HttpResponse
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase
from hptopLib.TAPIBookingBase import TAPIBookingBase

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


class TPickUp(TAPIBookingBase):
    def getInfo(self, payment_idx, *args):
        try:
            pass
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[1] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PICKUP_HOTEL_PUT % (args[0]["order_num"]
                                                            , args[0]["is_pickup"], args[0]["zipcode"]
                                                            , args[0]["addr1"], args[0]["addr2"]
                                                            , args[0]["addr4"]), QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None

class TPayment(TAPIBookingBase):
    def getInfo(self, payment_idx, *args):
        try:
            pass
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[1] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PAYMENT_HOTEL_PUT % (args[0]["order_num"]
                                                            , args[0]["hp_seq"], args[0]["room_name"]
                                                            , args[0]["weight"], args[0]["room_price"]
                                                            , args[0]["neutral_price"], args[0]["extra_price"]
                                                            , args[0]["pickup_price"], args[0]["room_sort"]
                                                            , args[0]["coupon_data"], args[0]["etc_product_data"]), QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None














