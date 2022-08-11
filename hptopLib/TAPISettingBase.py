# -*- coding: utf-8 -*-
from abc import abstractmethod
from inspect import getframeinfo, currentframe
from django.http import HttpResponse

from hptopLib.TAPIBase import TAPIBase
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *


class TAPISettingBase(TAPIBase):
    """
    설정 기본 클래스.
    """

    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            err, msg, body = self.getInfo(partner_id)
            if err == 0:
                ret = self.message.successOk()
                ret["body"] = body
                return HttpResponse(self.json.dicToJson(ret))
            else:
                return HttpResponse(self.json.dicToJson(self.message.error(msg)))
        except Exception as e:
            return self.errorInfo(e)

    @abstractmethod
    def getInfo(self, partner_id):
        pass

    def errorInfo(self, err):
        msg = self.frameInfo(getframeinfo(currentframe()), err)
        return HttpResponse(self.json.dicToJson(self.message.error(msg)))


    def getBodyProduct(self, partner_id):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_VAT_GET % (partner_id), QUERY_DB)
            #          ret = self.message.successOk()
            body = {}
            if value is not None:
                body["is_vat"] = value[0]

            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_WORKTIME_GET % (partner_id), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body["worktime"] = {}
            if value is not None:
                for d in data:
                    tmp = body["worktime"]
                    tmp["idx"] = d[0]
                    tmp["bath"] = d[2]
                    tmp["part"] = d[3]
                    tmp["bath_part"] = d[4]
                    tmp["sanitation"] = d[5]
                    tmp["bath"] = d[6]
                    tmp["sanitation_bath"] = d[7]
                    tmp["all"] = d[8]
                    tmp["spoting"] = d[9]
                    tmp["scissors"] = d[10]
                    tmp["summercut"] = d[11]
                    tmp["time_1"] = d[12]
                    tmp["time_2"] = d[13]
                    tmp["time_3"] = d[14]
                    tmp["time_4"] = d[15]
                    tmp["time_5"] = d[16]
                    tmp["title_1"] = d[17]
                    tmp["title_2"] = d[18]
                    tmp["title_3"] = d[19]
                    tmp["title_4"] = d[20]
                    tmp["title_5"] = d[21]
                    tmp["disp_1"] = d[22]
                    tmp["disp_2"] = d[23]
                    tmp["disp_3"] = d[24]
                    tmp["disp_4"] = d[25]
                    tmp["disp_5"] = d[26]
                    tmp["disp_6"] = d[27]
                    tmp["disp_7"] = d[28]
                    tmp["disp_8"] = d[29]
                    tmp["disp_9"] = d[30]
                    tmp["disp_10"] = d[31]
                    tmp["disp_11"] = d[32]
                    tmp["disp_12"] = d[33]
                    tmp["disp_13"] = d[34]
                    tmp["disp_14"] = d[35]
                    # body["worktime"].append(tmp)


            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_DOG_PRODUCT_GET % (partner_id), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body["dog"] = []
            if value is not None:
                for d in data:
                    tmp = {}
                    tmp["second_type"] = d[2]
                    tmp["direct_title"] = d[3]
                    tmp["in_shop"] = d[4]
                    tmp["out_shop"] = d[5]
                    # kgs = d[35].split(',')
                    # tmp["kgs"] = []
                    # for i, k in kgs:
                    #     print(d[6].split(',')[i])
                    #     # kg["bath_price"] = d[6].split(',')[i]
                    #     # tmp["kgs"].append(kg)
                    body["dog"].append(tmp)


            return 0, body
        except Exception as e:
            return -1, e.args[0]