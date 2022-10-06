# -*- coding: utf-8 -*-
import traceback

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_RESERVE_SHOP_GET, PROC_RESERVE_SHOP_PUT
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase


class TShop(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        try:
            body = []
            value, rows, columns = self.db.resultDBQuery(PROC_RESERVE_SHOP_GET % (partner_id,),QUERY_DB)

            if value is not None:
                data = []
                if rows < 2:
                    data.append(value)
                else:
                    data = value
                for d in data:
                    tmp = {"idx":d[0], "artist_id":d[1], "reserve_price":d[2], "deadline":d[3], "bank_name":d[4],
                           "account_num":d[5], "is_manual":d[6], "is_use":d[7], "is_delete":d[8], "update_time":d[9]}
                    body.append(tmp)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        try:
            value = None
            row = None
            columns = None
            if args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(
                    PROC_RESERVE_SHOP_PUT % (
                        args[1]["artist_id"],
                        args[1]["reserve_price"],
                        args[1]["deadline"],
                        args[1]["bank_name"],
                        args[1]["account_num"]), QUERY_DB)
            else:
                return -1, "undefined method", {}
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as e:
            return -1, traceback.format_exc(), None
