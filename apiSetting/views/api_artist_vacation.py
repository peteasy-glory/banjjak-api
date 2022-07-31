# -*- coding: utf-8 -*-
from inspect import getframeinfo, currentframe


from hptopLib.TSettingBase import TSettingBase
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *


class TVacation(TSettingBase):

    def getInfo(self, partner_id):
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
                        vacation.append({"idx":r[0], "date_st":r[1], "date_fi":r[2], "update_date":r[3]})
                    tmp["vacation"] = vacation
                    body.append(tmp)
            return 0, "success", body
        except Exception as e:
            frame_info = getframeinfo(currentframe())
            msg = "[PATH: %s, LINE: %s, FUNC: %s, ERR: %s" % (frame_info.filename, frame_info.lineno, frame_info.function, e.args[0])
            return -1, msg, None
