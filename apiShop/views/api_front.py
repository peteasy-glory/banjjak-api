# -*- coding: utf-8 -*-
import traceback
from django.http import HttpResponse
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SHOP_FRONT_IMAGE_GET, PROC_SHOP_FRONT_IMAGE_POST, PROC_SHOP_FRONT_IMAGE_PUT, \
    PROC_SHOP_FRONT_IMAGE_DELETE
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase
from hptopLib.TDate import TDate
from hptopLib.TS3 import TS3


class TFront(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SHOP_FRONT_IMAGE_GET % (partner_id,),
                                                         QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        try:
            if args[0] == 'POST':
                date = TDate()
                fName = "artist_front_image_"+date.customDateTime(format_date="%Y%m%d%H%M%S%f")+"."+args[1]["mine"]
                s3 = TS3()
                err, msg = s3.frontUpload(args[1]["partner_id"], file_name=fName, origin_file=args[1]["image"])
                body = {}
                if err == -1:
                    return -1, "Fail image uplad", body
                value, rows, columns = self.db.resultDBQuery(PROC_SHOP_FRONT_IMAGE_POST % (args[1]["partner_id"], msg), QUERY_DB)
            elif args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_SHOP_FRONT_IMAGE_PUT % (args[1]["partner_id"],
                                                                                          args[1]["image"]), QUERY_DB)
            elif args[0] == 'DELETE':
                value, rows, columns = self.db.resultDBQuery(PROC_SHOP_FRONT_IMAGE_DELETE % (args[1]["partner_id"],
                                                                                          args[1]["image"]), QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as e:
            return -1, traceback.format_exc(), None