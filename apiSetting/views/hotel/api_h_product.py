# -*- coding: utf-8 -*-
from apiSetting.views.base.api_product import TProduct
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SETTING_HOTEL_PRODUCT_GET, PROC_SETTING_HOTEL_GET, \
    PROC_SETTING_HOTEL_PRODUCT_POST, PROC_SETTING_HOTEL_PRODUCT_PUT, PROC_SETTING_PHOTO_GET, \
    PROC_SETTING_HOTEL_PRODUCT_DELETE


class TRoom(TProduct):
    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_HOTEL_PRODUCT_GET % (partner_id,), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body = {"dog":[], "cat":[]}
            if value is not None:
                tmp_body = self.queryDataToDic(data, rows, columns)
                for tmp in tmp_body:
                    type = tmp["room_pet_type"]
                    tmp["fee_list"] = self.priceCommaSplit(tmp["weight"], tmp["normal_price"], tmp["peak_price"])
                    tmp["img_list"] = self.imageSplit(tmp["image"])
                    del tmp["weight"]
                    del tmp["normal_price"]
                    del tmp["peak_price"]
                    del tmp["image"]
                    del tmp["room_pet_type"]
                    del tmp["artist_id"]
                    del tmp["is_delete"]
                    del tmp["delete_msg"]
                    del tmp["delete_dt"]

                    if type == "dog":
                        body["dog"].append(tmp)
                    else:
                        body["cat"].append(tmp)
                err_coupon, body["coupon"] = self.getCoupon(partner_id)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def priceCommaSplit(self, weight, price, add_price):
        kg_arr = weight.split(",")
        price_arr = price.split(",")
        add_price_arr = add_price.split(",")
        ret_data = []
        i = 0
        for k in kg_arr:
            tmp = {"kg":k, "normal_price":0, "peak_price":0}
            if len(price_arr) > i:
                tmp["normal_price"] =  int(price_arr[i]) if price_arr[i] != "" else 0
            if len(add_price_arr) > i:
                tmp["peak_price"] = int(add_price_arr[i]) if add_price_arr[i] != "" else 0
            ret_data.append(tmp)
            i += 1
        return  ret_data

    def getCoupon(self, partner_id):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_HOTEL_GET % (partner_id,'H'), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body = []
            if value is not None:
                tmp_body = self.queryDataToDic(data, rows, columns)
                for tmp in tmp_body:
                    del tmp["customer_id"]
                    del tmp["product_type"]
                    del tmp["del_yn"]
                    body.append(tmp)
            return 0, body
        except Exception as err:
            return -1, []
    def imageSplit(self, image):
        img_arr = image.split(",")
        ret_data = []
        for i in img_arr:
            tmp = {"idx":0,"path":""}
            tmp["idx"] = int(i) if i != "" else 0
            tmp["path"] = self.getPhoto(int(i)) if i != "" else ""
            ret_data.append(tmp)
        return ret_data
    def getPhoto(self, idx):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_PHOTO_GET % (idx,), QUERY_DB)
            if value is not None:
                return value[2]
            else:
                return ""
        except Exception as err:
            return err.args[0]


    def modifyInfo(self, *args):
        try:
            body = {}
            if args[0] == 'POST' or args[0] == 'PUT' or args[0] == 'DELETE':
                if args[0] == 'POST':
                    value, rows, columns = self.db.resultDBQuery(PROC_SETTING_HOTEL_PRODUCT_POST % (args[1]["h_seq"],
                                                                args[1]["partner_id"],args[1]["room_pet_type"],args[1]["room_name"],
                                                                args[1]["room_cnt"],args[1]["weight"],args[1]["normal_price"],
                                                                args[1]["peak_price"],args[1]["is_neutral"],args[1]["is_neutral_pay"],
                                                                args[1]["neutral_price"],args[1]["extra_price"],args[1]["is_peak"],
                                                                args[1]["is_image"],args[1]["comment"],args[1]["image"]),QUERY_DB)
                elif args[0] == 'PUT':
                    value, rows, columns = self.db.resultDBQuery(PROC_SETTING_HOTEL_PRODUCT_PUT % (args[1]["hp_seq"], args[1]["room_name"],
                                                                args[1]["room_cnt"], args[1]["weight"],args[1]["normal_price"],args[1]["peak_price"],
                                                                args[1]["sort"],args[1]["is_neutral"],args[1]["is_neutral_pay"],args[1]["neutral_price"],
                                                                args[1]["extra_price"],args[1]["is_peak"],args[1]["is_image"], args[1]["comment"],
                                                                args[1]["image"]),QUERY_DB)
                else:
                    value, rows, columns = self.db.resultDBQuery( PROC_SETTING_HOTEL_PRODUCT_DELETE % (args[1]["hp_seq"], args[1]["del_msg"]), QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                    return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err.args[0]), None