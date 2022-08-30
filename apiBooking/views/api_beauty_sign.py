import traceback
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_BEAUTY_BOOKING_BEAUTY_SIGN_GET, PROC_BEAUTY_BOOKING_BEAUTY_SIGN_POST
from hptopLib.TAPIIDBase import TAPIIDBase
from hptopLib.TDate import TDate
from hptopLib.TS3 import TS3


class TSign(TAPIIDBase):

    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_BEAUTY_SIGN_GET % (partner_id,args[0]["pet_idx"]),
                                                         QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[0] == 'POST':
                date = TDate()
                fName = "tmp_"+date.customDateTime(format_date="%Y%m%d%H%M%S%f")+"."+args[1]["mime"]
                s3 = TS3()
                err, msg = s3.frontUpload("sign/"+args[1]["partner_id"], file_name=fName, origin_file=args[1]["image"])
                if err == -1:
                    return -1, "Fail image uplad", body
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_BEAUTY_SIGN_POST % (args[1]["partner_id"],
                                                                                                    args[1]["customer_id"],
                                                                                                    args[1]["customer_name"],
                                                                                                    args[1]["pet_idx"],
                                                                                                    args[1]["phone"],
                                                                                                    args[1]["is_beauty_agree"],
                                                                                                    args[1]["is_private_agree"],
                                                                                                    args[1]["agree_type"],
                                                                                                    args[1]["auth_url"], msg), QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as e:
            return -1, traceback.format_exc(), None