# -*- coding: utf-8 -*-
from inspect import getframeinfo, currentframe

from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase
from hptopLib.TAPIBookingBase import TAPIBookingBase


class TBooking(TAPIBase):

    def errorInfo(self, err):
        msg = self.frameInfo(getframeinfo(currentframe()), err)
        return HttpResponse(self.json.dicToJson(self.message.error(msg)))

    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            body = []
            if request.GET.get('st_date') is not None and request.GET.get('fi_date') is not None:
                st_date = request.GET.get('st_date')
                fi_date = request.GET.get('fi_date')
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PEROID_GET % (partner_id, st_date, fi_date), QUERY_DB)
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
            return self.errorInfo(e.args[0])


class TBookingJoin(TAPIBase):
    def errorInfo(self, err):
       msg = self.frameInfo(getframeinfo(currentframe()), err)
       return HttpResponse(self.json.dicToJson(self.message.error(msg)))

    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PREDATA_STATIC_GET % (partner_id,), QUERY_DB)
            ret = self.message.successOk()
            if value is None:
                ret["body"] = {}
                return HttpResponse(self.json.dicToJson(ret))
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            value2, rows2, columns2 = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PREDATA_COMMON_GET % (partner_id,), QUERY_DB)
            data2 = []
            if rows2 < 2:
                data2.append(value2)
            else:
                data2 = value2
            value3, rows3, columns3 = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PREDATA_WORKTIME_GET % (partner_id,), QUERY_DB)
            data3 = []
            if rows2 < 2:
                data3.append(value3)
            else:
                data3 = value3
            ret["body"] = self.setPreData(data, data2, data3)
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return self.errorInfo(e.args[0])


    def setPreData(self, static, common, worktime):
        base_type = ("목욕","부분미용","부분+목욕","전체미용","스포팅","가위컷","썸머컷")
        body = []
        for s in static:
            tmp = {"size": s[2]}
            tmp["svc"] = []
            for i in range(9):
                if worktime[0][21+i] == 'y':
                    if len(s[i+6]) > 0:
                        sub_svc = {"type":base_type[i], "time":worktime[0][2+i]}
                        sub_price = s[i+6].split(",")
                        sub_kg = s[35].split(",")
                        p_k = []
                        for j in range(len(sub_kg)):
                            p_k.append({"kg":sub_kg[j], "price":sub_price[j]})
                        sub_svc["unit"] = p_k
                        tmp["svc"].append(sub_svc)
            body.append(tmp)
        return body
















