# -*- coding: utf-8 -*-
from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase

class TCatProduct(TAPIBase):

    # 고양이 상품 등록/수정
    def put(self, request):
        try:
            dic = request.data

            if dic["customer_id"] is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))

            customer_id = dic["customer_id"].strip()
            data, rows1, columns1 = self.db.resultDBQuery(PROC_SETTING_BEAUTY_CAT_PUT % (customer_id, dic["in_shop_product"], dic["out_shop_product"], dic["short_price"], dic["long_price"], dic["increase_price"], dic["section"], dic["shower_price"], dic["shower_price_long"], dic["toenail_price"], dic["addition_option_product"], dic["hair_clot_price"], dic["ferocity_price"], dic["tick_price"],dic["addition_work_product"], dic["is_use_weight"], dic["add_comment"]), QUERY_DB)
            ret = self.message.successOk()
            if data is None:
                return HttpResponse(self.json.dicToJson(self.message.errorDBInsert()))
            if data[0] < 0:
                return HttpResponse(self.json.dicToJson(self.message.errorDBUpdate()))

            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))