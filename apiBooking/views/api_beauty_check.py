import traceback

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_BEAUTY_BOOKING_CHECKPHONE_GET,PROC_BEAUTY_BOOKING_REPEATRESERVCHK_GET
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase


class TCheckPhone(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        try:
            if len(args) < 1:
                return -1, "get Data를 확인해 주세요.", None
            else:
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_CHECKPHONE_GET % (partner_id,
                                                                                                    args[0]["phone_num"]), QUERY_DB)
                body = {}
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None


    def modifyInfo(self, *args):
        pass


class TCheckRepeatReserve(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        try:
            if len(args) < 1:
                return -1, "get Data를 확인해 주세요.", None
            else:
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_REPEATRESERVCHK_GET % (partner_id,
                                                                                                    args[0]["worker"],
                                                                                                    args[0]["start_time"],
                                                                                                    args[0]["end_time"]), QUERY_DB)
                body = {}
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None


    def modifyInfo(self, *args):
        pass
