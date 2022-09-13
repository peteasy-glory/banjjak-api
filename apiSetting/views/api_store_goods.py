# -*- coding: utf-8 -*-
from apiSetting.views.base.api_product import TProduct
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SETTING_BEAUTY_STORE_GOODS_DELETE, PROC_SETTING_BEAUTY_STORE_GOODS_POST


class TGoods(TProduct):
    def getInfo(self, partner_id, *args):
        pass

    def modifyInfo(self, *args):
        try:
            if args[0] == 'POST':
                if len(args[1]["goods"]) > 0:
                    value, rows, columns = self.db.resultDBQuery(
                        PROC_SETTING_BEAUTY_STORE_GOODS_DELETE % (args[1]["partner_id"], args[1]["product_kind"]),
                        QUERY_DB)
                    for good in args[1]["goods"]:
                        #try:
                        value, rows, columns = self.db.resultDBQuery(
                                        PROC_SETTING_BEAUTY_STORE_GOODS_POST % (args[1]["partner_id"],
                                                                                  args[1]["product_kind"],
                                                                                  good["name"], good["price"]), QUERY_DB)
                        #except Exception as err:
                        #    print(err)
                body = {}
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", {}
        except Exception as err:
            return -1, self.errorInfo(err), None