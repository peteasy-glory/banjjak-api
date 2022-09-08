# -*- coding: utf-8 -*-
from apiSetting.views.base.api_product import TProduct
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SETTING_BEAUTY_PART_DOG_MODIFY, PROC_SETTING_BEAUTY_PART_DOG_DELETE, \
    PROC_SETTING_BEAUTY_PART_DOG_GET, PROC_SETTING_BEAUTY_PART_TIME_DOG_PUT


class TPartTime(TProduct):
    def getInfo(self, partner_id, *args):
        pass

    def modifyInfo(self, *args):
        try:
            body = {}
            if  args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_SETTING_BEAUTY_PART_TIME_DOG_PUT % (args[1]["partner_id"],
                                                            args[1]["work_time1"],args[1]["work_time2"],args[1]["work_time3"],
                                                            args[1]["work_time4"],args[1]["work_time5"],args[1]["work_time6"],
                                                            args[1]["work_time7"],args[1]["work_time8"],args[1]["work_time9"],
                                                            args[1]["work_time10"],args[1]["work_time11"],args[1]["work_time12"],
                                                            args[1]["work_time13"],args[1]["work_time14"],),QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None


class TDog(TProduct):
    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_BEAUTY_PART_DOG_GET % (partner_id,), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body = []
            if value is not None:
                for d in data:
                    tmp = {
                        "idx": d[0],
                        "part":[
                               {"tag":"목욕", "time":d[2], "is_show":d[21], "ord":1},
                               {"tag": "부분미용", "time": d[3], "is_show":d[22], "ord":2},
                               {"tag": "부분+목욕", "time": d[4], "is_show":d[23], "ord":3},
                               {"tag": "위생", "time": d[5], "is_show":d[24], "ord":4},
                               {"tag": "위생+목욕", "time": d[6], "is_show":d[25], "ord":5},
                               {"tag": "전체미용", "time": d[7], "is_show":d[26], "ord":6},
                               {"tag": "스포팅", "time": d[8], "is_show":d[27], "ord":7},
                               {"tag": "가위컷", "time": d[9], "is_show":d[28], "ord":8},
                               {"tag": "썸머컷", "time": d[10], "is_show":d[29], "ord":9},
                               {"tag": d[16], "time": d[11], "is_show":d[30], "ord":10},
                               {"tag": d[17], "time": d[12], "is_show":d[31], "ord":11},
                               {"tag": d[18], "time": d[13], "is_show":d[32], "ord":12},
                               {"tag": d[19], "time": d[14], "is_show":d[33], "ord":13},
                               {"tag": d[20], "time": d[15], "is_show":d[34], "ord":14}
                             ],
                        "reg_date":d[35],
                        "update_date":d[36]
                    }
                    body.append(tmp)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

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