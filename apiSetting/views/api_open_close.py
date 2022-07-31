# -*- coding: utf-8 -*-

from inspect import getframeinfo, currentframe
from hptopLib.TSettingBase import TSettingBase
from apiShare.constVar import QUERY_DB
from apiShare.funcLib import zeroToBool
from apiShare.sqlQuery import *


class TOpenClose(TSettingBase):

    def getInfo(self, partner_id):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_SHOP_OPEN_CLOSE_GET % (partner_id,), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body = []
            if value is not None:
                for d in data:
                    tmp = {"open_time": d[1], "close_time": d[2],
                           "is_work_of_holiday": zeroToBool(d[3]), "update_date": str(d[4])}
                    body.append(tmp)
            return 0, "success", body
        except Exception as e:
            frame_info = getframeinfo(currentframe())
            msg = "[PATH: %s, LINE: %s, FUNC: %s, ERR: %s" % (frame_info.filename, frame_info.lineno, frame_info.function, e.args[0])
            return -1, msg, None
