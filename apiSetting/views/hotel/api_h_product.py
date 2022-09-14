# -*- coding: utf-8 -*-
from apiSetting.views.base.api_product import TProduct
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SETTING_HOTEL_PRODUCT_GET


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

    def imageSplit(self, image):
        img_arr = image.split(",")
        ret_data = []
        for i in img_arr:
            tmp = {"idx":int(i) if i != "" else 0}
            ret_data.append(tmp)
        return ret_data

    def modifyInfo(self, *args):
        pass
        # try:
        #     body = {}
        #     if  args[0] == 'PUT':
        #         value, rows, columns = self.db.resultDBQuery(PROC_SETTING_BEAUTY_PART_TIME_DOG_PUT % (args[1]["partner_id"],
        #                                                     args[1]["work_time1"],args[1]["work_time2"],args[1]["work_time3"],
        #                                                     args[1]["work_time4"],args[1]["work_time5"],args[1]["work_time6"],
        #                                                     args[1]["work_time7"],args[1]["work_time8"],args[1]["work_time9"],
        #                                                     args[1]["work_time10"],args[1]["work_time11"],args[1]["work_time12"],
        #                                                     args[1]["work_time13"],args[1]["work_time14"],),QUERY_DB)
        #         if value is not None:
        #             body = self.queryDataToDic(value, rows, columns)
        #         return 0, "success", body
        #     return - 1, "undefined method", body
        # except Exception as err:
        #     return -1, self.errorInfo(err), None