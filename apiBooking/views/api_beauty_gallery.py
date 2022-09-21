# -*- coding: utf-8 -*-

import traceback
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_BEAUTY_BOOKING_BEAUTY_GALLERY_POST, PROC_BEAUTY_BOOKING_BEAUTY_GALLERY_GET, \
    PROC_BEAUTY_BOOKING_BEAUTY_GALLERY_DELETE
from hptopLib.TAPIBookingBase import TAPIBookingBase
from hptopLib.TDate import TDate
from hptopLib.TS3 import TS3


class TGallery(TAPIBookingBase):

    def getInfo(self, pet_idx, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_BEAUTY_GALLERY_GET % (pet_idx,args[0]["artist_id"]),
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
            if args[1] == 'POST':
                date = TDate()
                fName = "pet_gallery_"+date.customDateTime(format_date="%Y%m%d%H%M%S%f")+"."+args[0]["mime"]
                s3 = TS3()
                err, msg = s3.frontUpload(args[0]["partner_id"], file_name=fName, origin_file=args[0]["image"])
                if err == -1:
                    return -1, "Fail image uplad", body
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_BEAUTY_GALLERY_POST % (args[0]["payment_log_seq"],
                                                                                                        args[0]["partner_id"],
                                                                                                        args[0]["pet_seq"],
                                                                                                        args[0]["prnt_title"],msg), QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            elif args[1] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_BEAUTY_GALLERY_DELETE % (args[0]["idx"],), QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as e:
            return -1, traceback.format_exc(), None