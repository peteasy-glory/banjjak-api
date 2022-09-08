
# -*- coding: utf-8 -*-
import traceback
from django.http import HttpResponse
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase


class TSend(TAPIBase):
    def post(self, request):
        try:
            dic = request.data

            if dic["cellphone"] is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))

            if dic["btn_link"] != '':
                data, rows, columns = self.db.resultDBQuery(PROC_ALLIM_WITHBTN_POST % (dic["cellphone"], dic["message"], dic["tem_code"], dic["btn_link"]),QUERY_DB)
            else:
                data, rows, columns = self.db.resultDBQuery(PROC_ALLIM_WITHOUTBTN_POST % (dic["cellphone"], dic["message"], dic["tem_code"]),QUERY_DB)

            ret = self.message.successOk()
            if data is None:
                return HttpResponse(self.json.dicToJson(self.message.errorDBInsert()))
            if data[0] < 0:
                return HttpResponse(self.json.dicToJson(self.message.errorDBUpdate()))

            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))
