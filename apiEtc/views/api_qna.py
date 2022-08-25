# -*- coding: utf-8 -*-
import traceback

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_ETC_ONE_ON_ONE_INQUIRY_GET, PROC_ETC_ONE_ON_ONE_INQUIRY_POST
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase


class TQna(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        try:
            body = []
            value, rows, columns = self.db.resultDBQuery(PROC_ETC_ONE_ON_ONE_INQUIRY_GET % (partner_id,),QUERY_DB)

            if value is not None:
                data = []
                if rows < 2:
                    data.append(value)
                else:
                    data = value
                for d in data:
                    tmp = {"req_idx":d[0], "req_id":d[1], "req_email":d[3], "req_main_type":d[5], "req_sub_type":d[6],
                           "req_title":d[4], "req_body":d[7], "req_date":d[8], "ans_idx":d[9], "ans_body":d[10], "ans_date":d[11]}
                    body.append(tmp)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        try:
            value = None
            row = None
            columns = None
            if args[0] == 'POST':
                value, rows, columns = self.db.resultDBQuery(PROC_ETC_ONE_ON_ONE_INQUIRY_POST % (args[1]["partner_id"],
                                                          args[1]["email"], args[1]["main_type"], args[1]["sub_type"],
                                                          args[1]["title"],args[1]["contents"]), QUERY_DB)
            else:
                return -1, "undefined method", {}
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as e:
            return -1, traceback.format_exc(), None
