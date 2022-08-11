# -*- coding: utf-8 -*-

from inspect import getframeinfo, currentframe

from hptopLib.TAPISettingBase import TAPISettingBase
from apiShare.constVar import QUERY_DB
from apiShare.funcLib import zeroToBool
from apiShare.sqlQuery import *


class TPartTime(TAPISettingBase):

    def getInfo(self, partner_id):
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
                           "is_leave": zeroToBool(d[9]), "is_show": True if d[10] == 2 else False,
                           "update_date":str(d[6]), "res_time_cnt": d[5]}
                    sub = d[3].split(",")
                    res_time_off = []
                    for s in sub:
                        res_time_off.append({"time": s})
                    tmp["res_time_off"] = res_time_off
                    body.append(tmp)
            return 0, "success", body
        except Exception as e:
            msg = self.frameInfo(getframeinfo(currentframe()), e.args[0])
            return -1, msg, None

