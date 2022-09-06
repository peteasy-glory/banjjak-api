# -*- coding: utf-8 -*-
from apiSetting.views.base.api_product import TProduct
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SETTING_BEAUTY_PART_DOG_MODIFY, PROC_SETTING_BEAUTY_PART_DOG_DELETE


class TDog(TProduct):
    def getInfo(self, partner_id, *args):
       pass

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[0] == 'POST' or args[0] == 'PUT':
                qryUpdate, qryInsert = self.argsToInsertUpdate(args)
                value, rows, columns = self.db.resultDBQuery(PROC_SETTING_BEAUTY_PART_DOG_MODIFY % (args[1]["partner_id"]
                                                            ,qryUpdate, qryInsert),QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            elif args[0] == 'DELETE':
                qryDelete = self.argsToDelete(args)
                value, rows, columns = self.db.resultDBQuery(PROC_SETTING_BEAUTY_PART_DOG_DELETE % (qryDelete,),QUERY_DB)
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

        update ="UPDATE tb_product_dog_worktime " \
                "SET worktime1_disp_yn = '%s', worktime2_disp_yn = '%s', worktime3_disp_yn = '%s', " \
                    "worktime4_disp_yn = '%s', worktime5_disp_yn = '%s', worktime6_disp_yn = '%s', " \
                    "worktime7_disp_yn = '%s', worktime8_disp_yn = '%s', worktime9_disp_yn = '%s', " \
                    "worktime10 = '%s', worktime10_title = '%s', worktime10_disp_yn = '%s', " \
                    "worktime11 = '%s', worktime11_title = '%s', worktime11_disp_yn = '%s', " \
                    "worktime12 = '%s', worktime12_title = '%s', worktime12_disp_yn = '%s', " \
                    "worktime13 = '%s', worktime13_title = '%s ', worktime13_disp_yn = '%s', " \
                    "worktime14 = '%s', worktime14_title = '%s ', worktime14_disp_yn = '%s', " \
                    "update_dt = NOW() " \
                "WHERE artist_id = '%s'" % (dispArr[0],dispArr[1],dispArr[2],dispArr[3],dispArr[4],dispArr[5],dispArr[6],dispArr[7],dispArr[8]
                                                              ,timeArr[0], addTitle[0], dispArr[9]
                                                              ,timeArr[1], addTitle[1], dispArr[10]
                                                              ,timeArr[2], addTitle[2], dispArr[11]
                                                              ,timeArr[3], addTitle[3], dispArr[12]
                                                              ,timeArr[4], addTitle[4], dispArr[13],args[1]["partner_id"])

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
        return update, insert

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