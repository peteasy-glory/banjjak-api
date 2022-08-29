# -*- coding: utf-8 -*-
from inspect import getframeinfo, currentframe

from hptopLib.TAPIIDBase import TAPIIDBase
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *


class TVacation(TAPIIDBase):

    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_PERSONAL_VACATION_GET % (partner_id,), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body = []
            if value is not None:
                for d in data:
                    tmp = {}
                    tmp['worker'] = d[0]
                    vacation = []
                    sub = d[1].split(',')
                    for rs in sub:
                        r = rs.split("|")
                        vacation.append({"idx":r[0],"type":r[1], "date_st":r[2], "date_fi":r[3], "update_date":r[4]})
                    tmp["vacation"] = vacation
                    body.append(tmp)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            err_str = ""
            body = {}
            if args[0] == 'POST':
                for w in args[1]["worker"]:
                    value, rows, columns = self.db.resultDBQuery(PROC_SETTING_PERSONAL_VACATION_POST % (args[1]["partner_id"]
                                                                , w["name"], args[1]["type"], args[1]["st_date"], args[1]["fi_date"]),
                                                                 QUERY_DB)
                    if value is not None:
                        body = self.queryDataToDic(value, rows, columns)
                        if body["err"] != 0:
                            err_str += w["name"]+",insert_error|"
                if len(err_str) > 0:
                    body["err_msg"] = err_str
                return 0, "success", body
            elif args[0] == 'DELETE':
                value, rows, columns = self.db.resultDBQuery(
                    PROC_SETTING_PERSONAL_VACATION_DELETE % (args[1]["partner_id"]
                                                           , w["name"], args[1]["type"], args[1]["st_date"],
                                                           args[1]["fi_date"]),
                    QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None