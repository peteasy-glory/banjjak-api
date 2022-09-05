# -*- coding: utf-8 -*-

from inspect import getframeinfo, currentframe

from hptopLib.TAPIIDBase import TAPIIDBase
from apiShare.constVar import QUERY_DB
from apiShare.funcLib import zeroToBool
from apiShare.sqlQuery import *


class TPartTime(TAPIIDBase):
    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_TIME_LIMIT_GET % (partner_id,), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body = []
            if value is not None:
                for d in data:
                    tmp = {"idx": d[0], "name": d[2],"nick": d[7], "is_host": zeroToBool(d[8]),
                           "is_leave": d[9], "is_show": d[10],
                           "update_date":str(d[6]), "res_time_cnt": d[4]}
                    sub = d[3].split(",")
                    res_time_off = []
                    for s in sub:
                        res_time_off.append({"time": s})
                    tmp["res_time_off"] = res_time_off
                    body.append(tmp)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[0] == 'POST' or args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_SETTING_TIME_LIMIT_MODIFY % (args[1]["idx"]
                                                            , args[1]["partner_id"],args[1]["name"]
                                                            ,args[1]["times"] ),QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None


class TPartTimeSet(TAPIIDBase):
    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_TIME_CHOICE_TYPE_GET % (partner_id,), QUERY_DB)
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_SETTING_TIME_CHOICE_TYPE_PUT % (args[1]["partner_id"],
                                                                                                  args[1]["is_time_Type"]),QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None