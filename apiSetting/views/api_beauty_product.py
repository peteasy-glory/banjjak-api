# -*- coding: utf-8 -*-
from inspect import getframeinfo, currentframe

from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPISettingBase import TAPISettingBase


class TProduct(TAPISettingBase):
    """
    미용 상품 첫페이지 불러오기
    """

    def errorInfo(self, err):
        msg = self.frameInfo(getframeinfo(currentframe()), err)
        return HttpResponse(self.json.dicToJson(self.message.error(msg)))

    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            else:
                err, body = self.getBodyProduct(partner_id)
            if err < 0:
                return HttpResponse(self.json.dicToJson(self.message.errorDBSelect()))
            ret = self.message.successOk()
            ret["body"] = body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[0])))

    def put(self, request):
        try:
            dic = request.data

            if dic["artist_id"] is None or dic["pay_type"] is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))

            artist_id = dic["artist_id"].strip()
            data, rows, columns = self.db.resultDBQuery(PROC_SETTING_PAY_TYPE_PUT % (artist_id, dic["pay_type"]),QUERY_DB)
            ret = self.message.successOk()
            if data is None:
                return HttpResponse(self.json.dicToJson(self.message.errorDBInsert()))
            if data[0] < 0:
                return HttpResponse(self.json.dicToJson(self.message.errorDBUpdate()))

            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return self.errorInfo( e.args[0])


