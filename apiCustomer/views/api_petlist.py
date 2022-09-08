# -*- coding: utf-8 -*-

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_CUSTOMER_PET_LIST_GET, PROC_CUSTOMER_PET_DELETE, PROC_CUSTOMER_PET_INFO_GET
from hptopLib.TAPIIDBase import TAPIIDBase


class TPetList(TAPIIDBase):
    def getInfo(self, partner_id, *args):

        try:
            body = {}
            value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_PET_LIST_GET % (args[0]["cellphone"]), QUERY_DB)
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
                data = []
                if rows < 2:
                    data.append(body)
                else:
                    data = body

                for val in data:
                    if val["partner_id"] != "":
                        split = val["partner_id"].split(",")
                        arr = []
                        for s in split:
                            tmp = {"tag":s}
                            arr.append(tmp)
                        val["partner_id"] = arr
                    else:
                        val["partner_id"] = []
                    value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_PET_INFO_GET % (val["pet_seq"]),
                                                                 QUERY_DB)
                    detail = self.queryDataToDic(value, rows, columns)
                    val["detail"] = detail
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            if args[0] == 'DELETE':
                body = {}
                value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_PET_DELETE % (args[1]["partner_id"],args[1]["pet_idx"]), QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return -1, "undefined method", {}
        except Exception as e:
            return -1, self.errorInfo(e), None
