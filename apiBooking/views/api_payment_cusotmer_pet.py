# -*- coding: utf-8 -*-
import traceback
import json
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
                    if "product" in body:
                        body["product_parsing"] = self.productToDic(body["product"])
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
                            tmp = {"payment_idx":d[0], "pet_seq":d[1], "cutomer_id":d[3], "product":d[36], "booking_date":d[76], "local_price":d[13], "local_price_cash":d[14]}
                        else:
                            tmp = {"payment_idx": d[0], "pet_seq": d[1], "cutomer_id": d[3], "memo": d[58],  "booking_date": d[76]}
                        if "product" in tmp:
                            tmp["product_parsing"] = self.productToDic(tmp["product"])
                        body.append(tmp)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        pass

class TCustomerPetInfoHotel(TAPIBookingBase):
    def getInfo(self, payment_idx, *args):
        try:
            if len(args) < 1:
                value, rows, columns = self.db.resultDBQuery(
                    PROC_BEAUTY_BOOKING_CUSTOMER_PET_INFO_HOTEL_GET % (payment_idx,), QUERY_DB)
                body = {}
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                    if "coupon_data" in body:
                        body["coupon_parsing"] = json.loads(body["coupon_data"])
                    if "etc_product_data" in body:
                        body["etc_parsing"] = json.loads(body["etc_product_data"])
            else:
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_BEFORE_PAYMENT_INFO_HOTEL_GET % (payment_idx, args[0]["is_hotel"], args[0]["get_count"]), QUERY_DB)
                data = []
                body = []
                if rows < 2:
                    data.append(value)
                else:
                    data = value
                if value is not None:
                    for d in data:
                        if args[0]["is_hotel"]:
                            tmp = {"order_num":d[1], "pet_seq":d[5], "cutomer_id":d[2], "checkin_date":d[47], "checkout_date":d[49], "total_price":d[19]}
                        else:
                            tmp = {"order_num": d[1], "pet_seq": d[5], "cutomer_id": d[2], "memo": d[31],  "checkin_date":d[47], "checkout_date":d[49]}
                        if "coupon_data" in tmp:
                            tmp["coupon_parsing"] = json.loads(tmp["coupon_data"])
                        if "etc_product_data" in tmp:
                            tmp["etc_parsing"] = json.loads(tmp["etc_product_data"])
                        body.append(tmp)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        pass
