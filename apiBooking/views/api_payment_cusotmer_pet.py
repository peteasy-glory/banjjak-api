# -*- coding: utf-8 -*-

from inspect import getframeinfo, currentframe
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBookingBase import TAPIBookingBase


class TCustomerPetInfo(TAPIBookingBase):




    def getInfo(self, payment_idx, *args):
        try:
            if len(args) < 1:
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_CUSTOMER_PET_INFO_GET % (payment_idx,), QUERY_DB)
                body = {}
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
            else:
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_BEFORE_PAYMENT_INFO_GET % (payment_idx, args[0]["is_beauty"], args[0]["get_count"]), QUERY_DB)
                data = []
                body = []
                if rows < 2:
                    data.append(value)
                else:
                    data = value
                if value is not None:
                    for d in data:
                        if args[0]["is_beauty"]:
                            tmp = {"payment_idx":d[0], "pet_seq":d[1], "cutomer_id":d[3], "product":d[36], "booking_date":d[71]}
                        else:
                            tmp = {"payment_idx": d[0], "pet_seq": d[1], "cutomer_id": d[3], "memo": d[58],  "booking_date": d[71]}
                        body.append(tmp)
            return 0, "success", body
        except Exception as err:
            msg = self.frameInfo(getframeinfo(currentframe()), err)
            return -1, msg, None

    def modifyInfo(self, *args):
        pass
