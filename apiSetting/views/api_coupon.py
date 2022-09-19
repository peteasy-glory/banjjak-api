# -*- coding: utf-8 -*-
from apiSetting.views.base.api_product import TProduct
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SETTING_COUPON_GET, PROC_SETTING_COUPON_POST, PROC_SETTING_COUPON_PUT, \
    PROC_SETTING_PERIOD_COUPON_GET, PROC_SETTING_PERIOD_COUPON_POST, PROC_SETTING_PERIOD_COUPON_PUT, \
    PROC_SETTING_PERIOD_COUPON_DELETE


class TCoupon(TProduct):
    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_COUPON_GET % (partner_id,args[0]["service_type"]), QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[0] == 'POST' or args[0] == 'PUT':
                if args[0] == 'POST':
                    value, rows, columns = self.db.resultDBQuery(PROC_SETTING_COUPON_POST % (args[1]["partner_id"],args[1]["service_type"],args[1]["coupon_type"],
                                                                                             args[1]["name"],args[1]["given"],args[1]["price"]),QUERY_DB)
                else:
                    value, rows, columns = self.db.resultDBQuery(PROC_SETTING_COUPON_PUT % (args[1]["idx"],args[1]["name"],args[1]["given"],
                                                                                            args[1]["price"]),QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                    return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None


class TPeriodCoupon(TProduct):
    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_PERIOD_COUPON_GET % (partner_id,), QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)

            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[0] == 'POST' or args[0] == 'PUT' or args[0] == 'DELETE':
                if args[0] == 'POST':
                    value, rows, columns = self.db.resultDBQuery(PROC_SETTING_PERIOD_COUPON_POST % (args[1]["partner_id"],args[1]["name"],args[1]["count"],
                                                                                             args[1]["price"],args[1]["sale_price"]),QUERY_DB)
                elif args[0] == 'PUT':
                    value, rows, columns = self.db.resultDBQuery(PROC_SETTING_PERIOD_COUPON_PUT % (args[1]["idx"],args[1]["name"],args[1]["count"],
                                                                                            args[1]["price"],args[1]["sale_price"]),QUERY_DB)
                else:
                    value, rows, columns = self.db.resultDBQuery(PROC_SETTING_PERIOD_COUPON_DELETE % (args[1]["idx"],args[1]["is_del"],args[1]["del_msg"]),QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                    return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None