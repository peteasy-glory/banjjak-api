# -*- coding: utf-8 -*-

from hptopLib.TAPIIDBase import TAPIIDBase
from apiShare.constVar import QUERY_DB
from apiShare.funcLib import zeroToBool
from apiShare.sqlQuery import *


class TReqularHoliday(TAPIIDBase):



    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_REGULAR_HOLIDAY_GET % (partner_id,), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body = []
            if value is not None:
                for d in data:
                    tmp = {"is_work_sun": zeroToBool(d[1]),
                           "is_work_mon": zeroToBool(d[2]),
                           "is_work_tue": zeroToBool(d[3]),
                           "is_work_wed": zeroToBool(d[4]),
                           "is_work_thu": zeroToBool(d[5]),
                           "is_work_fri": zeroToBool(d[6]),
                           "is_work_sat": zeroToBool(d[7]),
                           "week_type": d[8],
                           "update_date": str(d[9])}
                    body.append(tmp)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            pass
        except Exception as err:
            return -1, self.errorInfo(err), None