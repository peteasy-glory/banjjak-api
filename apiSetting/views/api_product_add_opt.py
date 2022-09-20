# -*- coding: utf-8 -*-
from apiSetting.views.base.api_product import TProduct
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SETTING_BEAUTY_ADD_OPT_DOG_MODIFY, PROC_SETTING_BEAUTY_ADD_OPT_DOG_GET, \
    PROC_SETTING_BEAUTY_PART_DOG_GET, PROC_SETTING_BEAUTY_ADD_OPT_KIND_GET


class TKind(TProduct):
    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_BEAUTY_ADD_OPT_KIND_GET % (partner_id,
                                                                                                args[0]["first_type"]), QUERY_DB)
            body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

class TDog(TProduct):
    def getInfo(self, partner_id, *args):
        try:
            body = {}
            body2 = {}
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_BEAUTY_ADD_OPT_DOG_GET % (partner_id,
                                                                                                args[0]["first_type"],
                                                                                                args[0]["second_type"],
                                                                                                args[0]["direct_title"]), QUERY_DB)
            value2, rows2, columns2 = self.db.resultDBQuery(PROC_SETTING_BEAUTY_PART_DOG_GET % (partner_id,), QUERY_DB)

            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
                body2 = self.queryDataToDic(value2, rows2, columns2)
                data = []
                if rows < 2:
                    data.append(body)
                else:
                    data = body
                for d in data:
                    d["bath"] = self.dictValToChange(d,"목욕","bath_price","is_consult_bath")
                    d["part"] = self.dictValToChange(d,"부분미용","part_price","is_consult_part")
                    d["bath_part"] = self.dictValToChange(d,"부분+목욕","bath_part_price","is_consult_bath_part")
                    d["sanitation"] = self.dictValToChange(d,"위생","sanitation_price","is_consult_sanitation")
                    d["sanitation_bath"] = self.dictValToChange(d,"위생+목욕","sanitation_bath_price","is_consult_sanitation_bath")
                    d["all"] = self.dictValToChange(d,"전체미용","all_price","is_consult_all")
                    d["spoting"] = self.dictValToChange(d,"스포팅","spoting_price","is_consult_spoting")
                    d["scissors"] = self.dictValToChange(d,"가위컷","scissors_price","is_consult_scissors")
                    d["summercut"] = self.dictValToChange(d,"썸머컷","summercut_price","is_consult_summercut")
                    d["beauty1"] = self.dictValToChange(d,self.nullToStr(body2["worktime10_title"]),"beauty1_price","is_consult_beauty1")
                    d["beauty2"] = self.dictValToChange(d,self.nullToStr(body2["worktime11_title"]),"beauty2_price","is_consult_beauty2")
                    d["beauty3"] = self.dictValToChange(d,self.nullToStr(body2["worktime12_title"]),"beauty3_price","is_consult_beauty3")
                    d["beauty4"] = self.dictValToChange(d,self.nullToStr(body2["worktime13_title"]),"beauty4_price","is_consult_beauty4")
                    d["beauty5"] = self.dictValToChange(d,self.nullToStr(body2["worktime14_title"]),"beauty5_price","is_consult_beauty5")

            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[0] == 'POST' or args[0] == 'PUT':
                qryUpdate, qryInsert = self.argsToInsertUpdate(args)
                value, rows, columns = self.db.resultDBQuery(PROC_SETTING_BEAUTY_ADD_OPT_DOG_MODIFY % (args[1]["partner_id"]
                                                            ,args[1]["first_type"],args[1]["second_type"],args[1]["direct_title"]
                                                            ,qryUpdate, qryInsert),QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            elif args[0] == 'DELETE':
                qryDelete = self.argsToDelete(args)
                value, rows, columns = self.db.resultDBQuery(PROC_SETTING_BEAUTY_ADD_OPT_DOG_MODIFY % (qryDelete,),QUERY_DB)
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
        update = "UPDATE tb_product_dog_static "
        insert = "INSERT INTO tb_product_dog_static "
        tail =      "WHERE customer_id          = '%s' " \
                    "	 AND first_type = '%s' " \
                    "   AND (second_type = '%s' OR second_type = '%s') " \
                    "   AND if( second_type != '직접입력',(direct_title = '' OR direct_title IS NULL),direct_title = '%s') " \
                    % (args[1]["partner_id"], args[1]["first_type"], args[1]["second_type"], args[1]["direct_title"], args[1]["direct_title"])
        middle =        "SET " \
                        "customer_id                 = '%s', " \
                        "first_type                 = %s, " \
                        "second_type                = %s, " \
                        "direct_title               = %s, " \
                        "in_shop_product            = %s, " \
                        "out_shop_product           = %s, " \
                        "kgs                        = %s, " \
                        "bath_price                 = %s, " \
                        "part_price                 = %s, " \
                        "bath_part_price            = %s, " \
                        "sanitation_price           = %s, " \
                        "sanitation_bath_price      = %s, " \
                        "all_price                  = %s, " \
                        "spoting_price              = %s, " \
                        "scissors_price             = %s, " \
                        "summercut_price            = %s, " \
                        "beauty1_price             = %s, " \
                        "beauty2_price             = %s, " \
                        "beauty3_price             = %s, " \
                        "beauty4_price             = %s, " \
                        "beauty5_price             = %s, " \
                        "is_consult_bath            = %s, " \
                        "is_consult_part            = %s, " \
                        "is_consult_bath_part       = %s, " \
                        "is_consult_sanitation      = %s, " \
                        "is_consult_sanitation_bath = %s, " \
                        "is_consult_all             = %s, " \
                        "is_consult_spoting         = %s, " \
                        "is_consult_scissors        = %s, " \
                        "is_consult_summercut       = %s, " \
                        "is_consult_beauty1         = %s, " \
                        "is_consult_beauty2         = %s, " \
                        "is_consult_beauty3         = %s, " \
                        "is_consult_beauty4         = %s, " \
                        "is_consult_beauty5         = %s, " \
                        "is_over_kgs                = %s, " \
                        "what_over_kgs              = %s, " \
                        "over_kgs_price             = %s, " \
                        "add_comment                = %s, " \
                        "update_time                = NOW() " % (args[1]["partner_id"],
                        self.isNull(args[1]["first_type"]), self.isNull(args[1]["second_type"]), self.isNull(args[1]["direct_title"]), self.isNull(args[1]["in_shop_product"]), self.isNull(args[1]["out_shop_product"]),
                        self.isNull(args[1]["kgs"]), self.isNull(args[1]["bath_price"]), self.isNull(args[1]["part_pric"]), self.isNull(args[1]["bath_part_price"]), self.isNull(args[1]["sanitation_price"]),
                        self.isNull(args[1]["sanitation_bath_price"]), self.isNull(args[1]["all_price"]), self.isNull(args[1]["spoting_price"]), self.isNull(args[1]["scissors_price"]), self.isNull(args[1]["summercut_price"]),
                        self.isNull(args[1]["beauty1_price"]), self.isNull(args[1]["beauty2_price"]), self.isNull(args[1]["beauty3_price"]), self.isNull(args[1]["beauty4_price"]), self.isNull(args[1]["beauty5_price"]),
                        self.isNull(args[1]["is_consult_bath"]), self.isNull(args[1]["is_consult_part"]), self.isNull(args[1]["is_consult_bath_part"]), self.isNull(args[1]["is_consult_sanitation"]), self.isNull(args[1]["is_consult_sanitation_bath"]),
                        self.isNull(args[1]["is_consult_all"]), self.isNull(args[1]["is_consult_spoting"]), self.isNull(args[1]["is_consult_scissors"]), self.isNull(args[1]["is_consult_summercut"]), self.isNull(args[1]["is_consult_beauty1"]),
                        self.isNull(args[1]["is_consult_beauty2"]), self.isNull(args[1]["is_consult_beauty3"]), self.isNull(args[1]["is_consult_beauty4"]), self.isNull(args[1]["is_consult_beauty5"]), self.isNull(args[1]["is_over_kgs"]),
                        self.isNull(args[1]["what_over_kgs"]), self.isNull(args[1]["over_kgs_price"]), self.isNull(args[1]["add_comment"]))

        return update+middle+tail, insert+middle

    def argsToDelete(self, args):
        dispArr = args[1]["display"].split("|")
        timeArr = args[1]["time"].split("|")
        addTitle = args[1]["add_title"].split("|")

        update ="UPDATE tb_product_dog_worktime " \
                "SET worktime10 = %s, worktime10_title = %s, worktime10_disp_yn = %s, " \
                    "worktime11 = %s, worktime11_title = %s, worktime11_disp_yn = %s, " \
                    "worktime12 = %s, worktime12_title = %s, worktime12_disp_yn = %s, " \
                    "worktime13 = %s, worktime13_title = %s, worktime13_disp_yn = %s, " \
                    "worktime14 = %s, worktime14_title = %s, worktime14_disp_yn = %s, " \
                    "update_dt = NOW() " \
                "WHERE artist_id = '%s'" % (self.isNull(timeArr[0]), self.isNull(addTitle[0]), self.isNull(dispArr[0])
                                            ,self.isNull(timeArr[1]), self.isNull(addTitle[1]), self.isNull(dispArr[1])
                                            ,self.isNull(timeArr[2]), self.isNull(addTitle[2]), self.isNull(dispArr[2])
                                            ,self.isNull(timeArr[3]), self.isNull(addTitle[3]), self.isNull(dispArr[3])
                                            ,self.isNull(timeArr[4]), self.isNull(addTitle[4]), self.isNull(dispArr[4]),args[1]["partner_id"])
        return update

    def nullToStr(self, val):
        if val is None or val == "null":
            return ""
        return val
    def isNull(self, val):
        if val == 'null'.lower():
            return 'NULL'
        else:
            return "'"+val+"'"