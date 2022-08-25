# -*- coding: utf-8 -*-
import traceback

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_ETC_ONE_ON_ONE_INQUIRY_GET
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase


class TQna(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        try:
            body = {}
            value, rows, columns = self.db.resultDBQuery(PROC_ETC_ONE_ON_ONE_INQUIRY_GET % (partner_id,),QUERY_DB)

            if value is not None:
                data = []
                if rows < 2:
                    data.append(value)
                else:
                    data = value
                for d in data:
                    tmp = {"q_idx":d[0], "q_id":d[1]}
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        try:
            value = None
            row = None
            columns = None
            if args[0] == 'POST':
                value, rows, columns = self.db.resultDBQuery(PROC_SHOP_BLOG_POST % (args[1]["idx"], args[1]["reply"]), QUERY_DB)
            elif args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_SHOP_BLOG_PUT % (args[1]["idx"], args[1]["reply"]), QUERY_DB)
            elif args[0] == 'DELETE':
                value, rows, columns = self.db.resultDBQuery(PROC_SHOP_BLOG_DELETE % (args[1]["idx"],), QUERY_DB)
            else:
                return -1, "undefined method", {}
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as e:
            return -1, traceback.format_exc(), None
