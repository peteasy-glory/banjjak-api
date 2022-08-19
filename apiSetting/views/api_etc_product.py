# -*- coding: utf-8 -*-
from inspect import getframeinfo, currentframe

from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPISettingBase import TAPISettingBase


class TProduct(TAPISettingBase):
    """
    제품 가져오기
    """

    def __init__(self):
        pass

    def __del__(self):
        pass

    def errorInfo(self, err):
        msg = self.frameInfo(getframeinfo(currentframe()), err)
        return HttpResponse(self.json.dicToJson(self.message.error(msg)))

    def getInfo(self, partner_id):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_ETC_PRODUCT_GET % (partner_id), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body = []
            if value is not None:
                for d in data:
                    tmp = {}
                    tmp["type"] = d[5]
                    tmp["name"] = d[6]
                    tmp["price"] = d[8]

                    body.append(tmp)
            return 0, "success", body
        except Exception as e:
            msg = self.frameInfo(getframeinfo(currentframe()), e.args[0])
            return -1, msg, None

    def put(self, request):
        try:
           pass
        except Exception as e:
            return self.errorInfo( e.args[0])


