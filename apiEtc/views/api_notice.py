# -*- coding: utf-8 -*-
import traceback

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_ETC_NOTICE_GET
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase


class TNotice(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        try:
            body = []
            value, rows, columns = self.db.resultDBQuery(PROC_ETC_NOTICE_GET % (),QUERY_DB)

            if value is not None:
                data = []
                if rows < 2:
                    data.append(value)
                else:
                    data = value
                for d in data:
                    tmp = {"idx":d[0], "id":d[1], "title":d[2], "image":d[7], "req_date":d[8],"mod_date":"" if d[9] is None else d[9]}
                    body.append(tmp)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        try:
            pass
        except Exception as e:
            return -1, traceback.format_exc(), None
