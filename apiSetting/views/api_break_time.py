# -*- coding: utf-8 -*-

from inspect import getframeinfo, currentframe

from hptopLib.TAPIIDBase import TAPIIDBase
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *


class TBreakTime(TAPIIDBase):


    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_BREAK_TIME_GET % (partner_id,), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body = []
            if value is not None:
                for d in data:
                    tmp = {"idx": d[0], "res_time_cnt": d[3],"res_time_off_ytn": d[4],
                           "reg_date": str(d[5]),"update_date":str(d[6])}
                    sub = d[2].split(",")
                    res_time_off = []
                    for s in sub:
                        res_time_off.append({"time":s})
                    tmp["res_time_off"] = res_time_off
                    body.append(tmp)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[0] == 'POST' or args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_SETTING_BREAK_TIME_MODIFY % (args[1]["partner_id"]
                                                            , args[1]["break_time"]),QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None