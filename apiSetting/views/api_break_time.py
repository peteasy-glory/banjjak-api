# -*- coding: utf-8 -*-

from inspect import getframeinfo, currentframe

from hptopLib.TAPISettingBase import TAPISettingBase
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *


class TBreakTime(TAPISettingBase):


    def getInfo(self, partner_id):
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
        except Exception as e:
            frame_info = getframeinfo(currentframe())
            msg = "[PATH: %s, LINE: %s, FUNC: %s, ERR: %s" % (frame_info.filename, frame_info.lineno, frame_info.function, e.args[0])
            return -1, msg, None

