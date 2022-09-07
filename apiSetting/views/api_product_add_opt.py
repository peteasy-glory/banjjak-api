# -*- coding: utf-8 -*-
from apiSetting.views.base.api_product import TProduct
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SETTING_BEAUTY_ADD_OPT_DOG_MODIFY


class TDog(TProduct):
    def getInfo(self, partner_id, *args):
       pass

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[0] == 'POST' or args[0] == 'PUT':
                qryUpdate, qryInsert = self.argsToInsertUpdate(args)
                value, rows, columns = self.db.resultDBQuery(PROC_SETTING_BEAUTY_ADD_OPT_DOG_MODIFY % (args[1]["partner_id"]
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

    def argsToInsertUpdate(self, args):
        dispArr = args[1]["display"].split("|")
        timeArr = args[1]["time"].split("|")
        addTitle = args[1]["add_title"].split("|")

        update = "UPDATE tb_product_dog_static "
        insert = "INSERT INTO tb_product_dog_static "
        tail =      "WHERE customer_id          = 'eaden@peteasy.kr' " \
                    "	 AND first_type = '개' " \
                    "   AND second_type = '직접입력' " \
                    "   AND direct_title = '추가 강아지 상품 1' "

        middle =        "SET " \
                        "first_type                 = '개', " \
                        "second_type                = '직접입력', " \
                        "direct_title               = '추가 강아지 상품 1', " \
                        "in_shop_product            = '1', " \
                        "out_shop_product           = '0', " \
                        "kgs                        = '1', " \
                        "bath_price                 = '1000', " \
                        "part_price                 = '1000', " \
                        "bath_part_price            = '1000', " \
                        "sanitation_price           = '1000', " \
                        "sanitation_bath_price      = '1000', " \
                        "all_price                  = '1000', " \
                        "spoting_price              = '1000', " \
                        "scissors_price             = '1000', " \
                        "summercut_price            = '1000', " \
                        "beauty1_price             = '1000', " \
                        "beauty2_price             = '1000', " \
                        "beauty3_price             = '', " \
                        "beauty4_price             = '', " \
                        "beauty5_price             = '', " \
                        "is_consult_bath            = '0', " \
                        "is_consult_part            = '0', " \
                        "is_consult_bath_part       = '0', " \
                        "is_consult_sanitation      = '0', " \
                        "is_consult_sanitation_bath = '0', " \
                        "is_consult_all             = '0', " \
                        "is_consult_spoting         = '0', " \
                        "is_consult_scissors        = '0', " \
                        "is_consult_summercut       = '0', " \
                        "is_consult_beauty1         = '0', " \
                        "is_consult_beauty2         = '0', " \
                        "is_consult_beauty3         = '', " \
                        "is_consult_beauty4         = '', " \
                        "is_consult_beauty5         = '', " \
                        "is_over_kgs                = '1', " \
                        "what_over_kgs              = '9', " \
                        "over_kgs_price             = '90', " \
                        "add_comment                = '추가 요금 설정 설명', " \
                        "update_time                = NOW() "


        insert = "INSERT INTO tb_product_dog_worktime " \
                 "SET artist_id = '%s', worktime1_disp_yn = '%s', worktime2_disp_yn = '%s', " \
                 "worktime3_disp_yn = '%s', worktime4_disp_yn = '%s', worktime5_disp_yn = '%s', worktime6_disp_yn = '%s', " \
                 "worktime7_disp_yn = '%s', worktime8_disp_yn = '%s', worktime9_disp_yn = '%s', " \
                 "worktime10 = '%s', worktime10_title = '%s', worktime10_disp_yn = '%s'," \
                 "worktime11 = '%s', worktime11_title = '%s', worktime11_disp_yn = '%s'," \
                 "worktime12 = '%s', worktime12_title = '%s', worktime12_disp_yn = '%s'," \
                 "worktime13 = '%s', worktime13_title = '%s', worktime13_disp_yn = '%s'," \
                 "worktime14 = '%s', worktime14_title = '%s', worktime14_disp_yn = '%s', " \
                 "reg_dt = NOW()" % (args[1]["partner_id"], dispArr[0], dispArr[1]
                                     , dispArr[2], dispArr[3], dispArr[4], dispArr[5]
                                     , dispArr[6], dispArr[7], dispArr[8]
                                     , timeArr[0], addTitle[0], dispArr[9]
                                     , timeArr[1], addTitle[1], dispArr[10]
                                     , timeArr[2], addTitle[2], dispArr[11]
                                     , timeArr[3], addTitle[3], dispArr[12]
                                     , timeArr[4], addTitle[4], dispArr[13])
        return update+middle, insert+middle

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

    def isNull(self, val):
        if val == 'null'.lower():
            return 'NULL'
        else:
            return "'"+val+"'"