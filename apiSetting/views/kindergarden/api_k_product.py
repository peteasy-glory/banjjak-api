# -*- coding: utf-8 -*-
from apiSetting.views.base.api_product import TProduct
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SETTING_KINDERGARDEN_PRODUCT_GET, PROC_SETTING_KINDERGARDEN_PRODUCT_POST, \
    PROC_SETTING_KINDERGARDEN_PRODUCT_PUT, PROC_SETTING_KINDERGARDEN_PRODUCT_DELETE


class TRoom(TProduct):
    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_KINDERGARDEN_PRODUCT_GET % (partner_id,), QUERY_DB)

            body = {"base":[], "coupon":[]}
            if value is not None:
                tmp_body = self.queryDataToDic(value, rows, columns)
                data = []
                if rows < 2:
                    data.append(tmp_body)
                else:
                    data = tmp_body
                for tmp in data:
                    tmp["fee_list"] = self.priceCommaSplit(tmp["weight"], tmp["normal_price"])
                    del tmp["weight"]
                    del tmp["normal_price"]
                    del tmp["artist_id"]
                    del tmp["is_delete"]
                    del tmp["delete_msg"]
                    del tmp["delete_dt"]
                    body["base"].append(tmp)
                err_coupon, body["coupon"] = self.getCoupon(partner_id, service="K")
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[0] == 'POST' or args[0] == 'PUT' or args[0] == 'DELETE':
                if args[0] == 'POST':
                    value, rows, columns = self.db.resultDBQuery(PROC_SETTING_KINDERGARDEN_PRODUCT_POST % (args[1]["kindergarden_idx"],
                                                                args[1]["partner_id"],args[1]["room_name"],args[1]["weight"],
                                                                args[1]["normal_price"],args[1]["sort"],args[1]["comment"]),QUERY_DB)
                elif args[0] == 'PUT':
                    value, rows, columns = self.db.resultDBQuery(PROC_SETTING_KINDERGARDEN_PRODUCT_PUT % (args[1]["idx"], args[1]["room_name"],
                                                                args[1]["weight"], args[1]["normal_price"],args[1]["sort"],args[1]["comment"],
                                                                args[1]["is_delete"]),QUERY_DB)
                else:
                    value, rows, columns = self.db.resultDBQuery( PROC_SETTING_KINDERGARDEN_PRODUCT_DELETE % (args[1]["idx"], args[1]["del_msg"]), QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                    return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err.args[0]), None


