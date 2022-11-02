import traceback

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_BEAUTY_BOOKING_CHECKPHONE_GET
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase


class TCheckPhone(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        try:
            if len(args) < 1:
                return -1, "Post Data를 확인해 주세요.", None
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




