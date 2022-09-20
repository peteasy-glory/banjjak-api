# -*- coding: utf-8 -*-
from apiSetting.views.base.api_product import TProduct
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SETTING_BEAUTY_ADD_OPT_ETC_DOG_MODIFY, PROC_SETTING_BEAUTY_ADD_OPT_ETC_DOG_DELETE, \
    PROC_SETTING_BEAUTY_COMMON_OPTION_DELETE, PROC_SETTING_BEAUTY_COMMON_OPTION_POST


class TDog(TProduct):
    def getInfo(self, partner_id, *args):
        pass
        # try:
        #     body = {}
        #     body2 = {}
        #     value, rows, columns = self.db.resultDBQuery(PROC_SETTING_BEAUTY_ADD_OPT_ETC_DOG_MODIFY % (partner_id,
        #                                                                                         args[0]["first_type"],
        #                                                                                         args[0]["second_type"]), QUERY_DB)
        #
        #     if value is not None:
        #         body = self.queryDataToDic(value, rows, columns)
        #         body2 = self.queryDataToDic(value2, rows2, columns2)
        #         data = []
        #         if rows < 2:
        #             data.append(body)
        #         else:
        #             data = body
        #         for d in data:
        #             d["bath"] = self.dictValToChange(d,"목욕","bath_price","is_consult_bath")
        #             d["part"] = self.dictValToChange(d,"부분미용","part_price","is_consult_part")
        #             d["bath_part"] = self.dictValToChange(d,"부분+목욕","bath_part_price","is_consult_bath_part")
        #             d["sanitation"] = self.dictValToChange(d,"위생","sanitation_price","is_consult_sanitation")
        #             d["sanitation_bath"] = self.dictValToChange(d,"위생+목욕","sanitation_bath_price","is_consult_sanitation_bath")
        #             d["all"] = self.dictValToChange(d,"전체미용","all_price","is_consult_all")
        #             d["spoting"] = self.dictValToChange(d,"스포팅","spoting_price","is_consult_spoting")
        #             d["scissors"] = self.dictValToChange(d,"가위컷","scissors_price","is_consult_scissors")
        #             d["summercut"] = self.dictValToChange(d,"썸머컷","summercut_price","is_consult_summercut")
        #             d["beauty1"] = self.dictValToChange(d,self.nullToStr(body2["worktime10_title"]),"beauty1_price","is_consult_beauty1")
        #             d["beauty2"] = self.dictValToChange(d,self.nullToStr(body2["worktime11_title"]),"beauty2_price","is_consult_beauty2")
        #             d["beauty3"] = self.dictValToChange(d,self.nullToStr(body2["worktime12_title"]),"beauty3_price","is_consult_beauty3")
        #             d["beauty4"] = self.dictValToChange(d,self.nullToStr(body2["worktime13_title"]),"beauty4_price","is_consult_beauty4")
        #             d["beauty5"] = self.dictValToChange(d,self.nullToStr(body2["worktime14_title"]),"beauty5_price","is_consult_beauty5")
        #
        #     return 0, "success", body
        # except Exception as err:
        #     return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[0] == 'POST' or args[0] == 'PUT':
                
                value, rows, columns = self.db.resultDBQuery(
                                    PROC_SETTING_BEAUTY_COMMON_OPTION_DELETE % (args[1]["partner_id"],), QUERY_DB)
                if len(args[1]["addition_bath_hair"]) > 0:
                    tmp_arr = args[1]["addition_bath_hair"].split(",")
                    for word in tmp_arr:
                        try:
                            tmp = word.split(":")
                            value, rows, columns = self.db.resultDBQuery(
                                            PROC_SETTING_BEAUTY_COMMON_OPTION_POST % (args[1]["partner_id"], tmp[0], tmp[1]), QUERY_DB)
                        except Exception as e:
                            return -1, "Error insert common_option["+e.args[0]+"]", None
                qryUpdate, qryInsert = self.argsToInsertUpdate(args)
                # print(qryUpdate)
                # print("===================================")
                # print(qryInsert)
                value, rows, columns = self.db.resultDBQuery(PROC_SETTING_BEAUTY_ADD_OPT_ETC_DOG_MODIFY % (args[1]["partner_id"]
                                                            ,args[1]["first_type"],args[1]["second_type"]
                                                            ,qryUpdate, qryInsert),QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            elif args[0] == 'DELETE':
                value, rows, columns = self.db.resultDBQuery(PROC_SETTING_BEAUTY_ADD_OPT_ETC_DOG_DELETE % (args[1]["partner_id"],
                                                                                                           args[1]["first_type"]),QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def dictValToChange(self, d, tag,old_val1, old_val2):
        new_val = {"tag":tag, "price":d[old_val1], "is_consult": d[old_val2]}
        del(d[old_val1])
        del(d[old_val2])
        return new_val

    def argsToInsertUpdate(self, args):
        update = "UPDATE tb_product_dog_common SET  "
        insert = "INSERT INTO tb_product_dog_common SET customer_id = '%s', first_type = '%s', second_type = '%s'," \
                                                                % (args[1]["partner_id"],args[1]["first_type"],args[1]["second_type"])
        tail =      "WHERE customer_id          = '%s' " \
                    "	 AND first_type = '%s' " % (args[1]["partner_id"], args[1]["first_type"])
        middle =        "in_shop_product            = %s, " \
                        "out_shop_product           = %s, " \
                        "basic_face_price                        = %s, " \
                        "broccoli_price                 = %s, " \
                        "highba_price                 = %s, " \
                        "bear_price            = %s, " \
                        "hair_clot_price           = %s, " \
                        "ferocity_price      = %s, " \
                        "tick_price                  = %s, " \
                        "short_hair_price              = %s, " \
                        "long_hair_price             = %s, " \
                        "double_hair_price            = %s, " \
                        "addition_face_product             = %s, " \
                        "addition_work_product             = %s, " \
                        "addition_option_product             = %s, " \
                        "spa_option_product             = %s, " \
                        "dyeing_option_product             = %s, " \
                        "etc_option_product            = %s, " \
                        "beauty_length_1            = %s, " \
                        "beauty_length_1_price       = %s, " \
                        "beauty_length_2      = %s, " \
                        "beauty_length_2_price = %s, " \
                        "beauty_length_3             = %s, " \
                        "beauty_length_3_price         = %s, " \
                        "beauty_length_4        = %s, " \
                        "beauty_length_4_price       = %s, " \
                        "beauty_length_5         = %s, " \
                        "beauty_length_5_price         = %s, " \
                        "hair_length_product         = %s, " \
                        "add_comment         = %s, " \
                        "update_time         = NOW() " % (self.isNull(args[1]["in_shop_product"]), self.isNull(args[1]["out_shop_product"]),
                        self.isNull(args[1]["basic_face_price"]), self.isNull(args[1]["broccoli_price"]),
                        self.isNull(args[1]["highba_price"]), self.isNull(args[1]["bear_price"]), self.isNull(args[1]["hair_clot_price"]), self.isNull(args[1]["ferocity_price"]), self.isNull(args[1]["tick_price"]),
                        self.isNull(args[1]["short_hair_price"]), self.isNull(args[1]["long_hair_price"]), self.isNull(args[1]["double_hair_price"]), self.isNull(args[1]["addition_face_product"]), self.isNull(args[1]["addition_work_product"]),
                        self.isNull(args[1]["addition_option_product"]), self.isNull(args[1]["spa_option_product"]), self.isNull(args[1]["dyeing_option_product"]), self.isNull(args[1]["etc_option_product"]),
                        self.isNull(args[1]["beauty_length_1"]),
                        self.isNull(args[1]["beauty_length_1_price"]), self.isNull(args[1]["beauty_length_2"]), self.isNull(args[1]["beauty_length_2_price"]), self.isNull(args[1]["beauty_length_3"]), self.isNull(args[1]["beauty_length_3_price"]),
                        self.isNull(args[1]["beauty_length_4"]), self.isNull(args[1]["beauty_length_4_price"]), self.isNull(args[1]["beauty_length_5"]), self.isNull(args[1]["beauty_length_5_price"]), self.isNull(args[1]["hair_length_product"]),
                        self.isNull(args[1]["add_comment"]))

        return update+middle+tail, insert+middle

    def nullToStr(self, val):
        if val is None or val == "null":
            return ""
        return val
    def isNull(self, val):
        if val == 'null'.lower():
            return 'NULL'
        else:
            return "'"+val+"'"