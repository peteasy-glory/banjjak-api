# -*- coding: utf-8 -*-
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SETTING_COUPON_GET
from hptopLib.TAPIIDBase import TAPIIDBase


class TProduct(TAPIIDBase):
    def getInfo(self, partner_id, *args):
        pass

    def modifyInfo(self, *args):
        pass

    def priceCommaSplit(self, weight, price, add_price=None):
        kg_arr = weight.split(",")
        price_arr = price.split(",")
        add_price_arr = []
        if add_price is not None:
            add_price_arr = add_price.split(",")
        ret_data = []
        i = 0
        for k in kg_arr:
            if add_price is not None:
                tmp = {"kg": k, "normal_price": 0, "peak_price": 0}
            else:
                tmp = {"kg": k, "normal_price": 0}
            if len(price_arr) > i:
                tmp["normal_price"] = int(price_arr[i]) if price_arr[i] != "" else 0
            if len(add_price_arr) > i:
                tmp["peak_price"] = int(add_price_arr[i]) if add_price_arr[i] != "" else 0
            ret_data.append(tmp)
            i += 1
        return ret_data

    def getCoupon(self, partner_id, service):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_COUPON_GET % (partner_id,service), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body = []
            if value is not None:
                tmp_body = self.queryDataToDic(data, rows, columns)
                for tmp in tmp_body:
                    del tmp["customer_id"]
                    del tmp["product_type"]
                    del tmp["del_yn"]
                    body.append(tmp)
            return 0, body
        except Exception as err:
            return -1, []




