# -*- coding: utf-8 -*-

from hptopLib.TAPIIDBase import TAPIIDBase
from apiShare.constVar import QUERY_DB
from apiShare.funcLib import zeroToBool
from apiShare.sqlQuery import *


class TOpenClose(TAPIIDBase):

    def getInfo(self, partner_id, *args):
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
                           "is_work_on_holiday": zeroToBool(d[3]), "update_date": str(d[4])}
                    body.append(tmp)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            pass
        except Exception as err:
            return -1, self.errorInfo(err), None