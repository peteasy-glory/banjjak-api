# -*- coding: utf-8 -*-
import traceback
from django.http import HttpResponse
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SHOP_REVIEW_PUT, PROC_SHOP_REVIEW_GET, PROC_SHOP_REVIEW_DELETE
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase


class TReview(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SHOP_REVIEW_GET % (partner_id,),
                                                         QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
                if rows > 1:
                    for b in body:
                        arr = b["review_images"].split("|")
                        b["review_images"] = []
                        for a in arr:
                            tmp = {"path": a}
                            b["review_images"].append(tmp)
                elif rows == 1:
                    arr = body["review_images"].split("|")
                    body["review_images"] = []
                    for a in arr:
                        tmp = {"path": a}
                        body["review_images"].append(tmp)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        try:
            value = None
            row = None
            columns = None
            if args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_SHOP_REVIEW_PUT % (args[1]["idx"], args[1]["reply"]), QUERY_DB)
            elif args[0] == 'DELETE':
                value, rows, columns = self.db.resultDBQuery(PROC_SHOP_REVIEW_DELETE % (args[1]["idx"],), QUERY_DB)
            else:
                return -1, "undefined method", {}
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as e:
            return -1, traceback.format_exc(), None