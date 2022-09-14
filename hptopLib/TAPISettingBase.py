# -*- coding: utf-8 -*-
from abc import abstractmethod
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
            return HttpResponse(self.json.dicToJson(self.message.error(self.errorInfo(e))))

    @abstractmethod
    def getInfo(self, partner_id):
        pass

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
                    tmp["bath"] = {}
                    sub = tmp["bath"]
                    sub["time"] = d[2]
                    sub["is_use"] = d[22]

                    tmp["part"] = {}
                    sub = tmp["part"]
                    sub["time"] = d[3]
                    sub["is_use"] = d[23]

                    tmp["bath_part"] = {}
                    sub = tmp["bath_part"]
                    sub["time"] = d[4]
                    sub["is_use"] = d[24]

                    tmp["sanitation"] = {}
                    sub = tmp["sanitation"]
                    sub["time"] = d[5]
                    sub["is_use"] = d[25]

                    tmp["sanitation_bath"] = {}
                    sub = tmp["sanitation_bath"]
                    sub["time"] = d[6]
                    sub["is_use"] = d[26]

                    tmp["all"] = {}
                    sub = tmp["all"]
                    sub["time"] = d[7]
                    sub["is_use"] = d[27]

                    tmp["spoting"] = {}
                    sub = tmp["spoting"]
                    sub["time"] = d[8]
                    sub["is_use"] = d[28]

                    tmp["scissors"] = {}
                    sub = tmp["scissors"]
                    sub["time"] = d[9]
                    sub["is_use"] = d[29]

                    tmp["summercut"] = {}
                    sub = tmp["summercut"]
                    sub["time"] = d[10]
                    sub["is_use"] = d[30]

                    if d[11] is not None:
                        tmp[d[16]] = {}
                        sub = tmp[d[16]]
                        sub["time"] = d[11]
                        sub["is_use"] = d[31]

                    if d[12] is not None:
                        tmp[d[17]] = {}
                        sub = tmp[d[17]]
                        sub["time"] = d[12]
                        sub["is_use"] = d[32]

                    if d[13] is not None:
                        tmp[d[18]] = {}
                        sub = tmp[d[18]]
                        sub["time"] = d[13]
                        sub["is_use"] = d[33]

                    if d[14] is not None:
                        tmp[d[19]] = {}
                        sub = tmp[d[19]]
                        sub["time"] = d[14]
                        sub["is_use"] = d[34]

                    if d[15] is not None:
                        tmp[d[20]] = {}
                        sub = tmp[d[20]]
                        sub["time"] = d[15]
                        sub["is_use"] = d[35]

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
                    if d[2] != '기타공통':
                        tmp = {}
                        tmp["second_type"] = d[2]
                        tmp["direct_title"] = d[3]
                        tmp["in_shop"] = d[4]
                        tmp["out_shop"] = d[5]
                        tmp["comment"] = d[40]
                        tmp["is_over_kgs"] = d[36]
                        tmp["over_kg"] = d[38]
                        tmp["over_price"] = d[39]
                        kgs = d[35].split(',')
                        tmp["service"] = []
                        for i, k in enumerate(kgs):
                            kg = {}
                            kg["kg"] = k
                            if d[6] is not None and d[6] != "" and i < len(d[6].split(',')) and d[20] is not None:
                                kg["bath_price"] = {}
                                sub = kg["bath_price"]
                                sub["price"] = (d[6].split(',')[i] if d[6].split(',')[i] is not None else 0)
                                sub["consult"] = (d[20].split(',')[i] if d[20].split(',')[i] is not None else 0)

                            if d[7] is not None and d[7] != "" and i < len(d[7].split(',')) and d[21] is not None:
                                kg["part_price"] = {}
                                sub = kg["part_price"]
                                sub["price"] = (d[7].split(',')[i] if d[7].split(',')[i] is not None else 0)
                                sub["consult"] = (d[21].split(',')[i] if d[21].split(',')[i] is not None else 0)

                            if d[8] is not None and d[8] != "" and i < len(d[8].split(',')) and d[22] is not None:
                                kg["bath_part_price"] = {}
                                sub = kg["bath_part_price"]
                                sub["price"] = (d[8].split(',')[i] if d[8].split(',')[i] is not None else 0)
                                sub["consult"] = (d[22].split(',')[i] if d[22].split(',')[i] is not None else 0)

                            if d[9] is not None and d[9] != "" and i < len(d[9].split(',')) and d[23] is not None:
                                kg["sanitation_price"] = {}
                                sub = kg["sanitation_price"]
                                sub["price"] = (d[9].split(',')[i] if d[9].split(',')[i] is not None else 0)
                                sub["consult"] = (d[23].split(',')[i] if d[23].split(',')[i] is not None else 0)

                            if d[10] is not None and d[10] != "" and i < len(d[10].split(',')) and d[24] is not None:
                                kg["sanitation_bath_price"] = {}
                                sub = kg["sanitation_bath_price"]
                                sub["price"] = (d[10].split(',')[i] if d[10].split(',')[i] is not None else 0)
                                sub["consult"] = (d[24].split(',')[i] if d[24].split(',')[i] is not None else 0)

                            if d[11] is not None and d[11] != "" and i < len(d[11].split(',')) and d[25] is not None:
                                kg["all_price"] = {}
                                sub = kg["all_price"]
                                sub["price"] = (d[11].split(',')[i] if d[11].split(',')[i] is not None else 0)
                                sub["consult"] = (d[25].split(',')[i] if d[25].split(',')[i] is not None else 0)

                            if d[12] is not None and d[12] != "" and i < len(d[12].split(',')) and d[26] is not None:
                                kg["spoting_price"] = {}
                                sub = kg["spoting_price"]
                                sub["price"] = (d[12].split(',')[i] if d[12].split(',')[i] is not None else 0)
                                sub["consult"] = (d[26].split(',')[i] if d[26].split(',')[i] is not None else 0)

                            if d[13] is not None and d[13] != "" and i < len(d[13].split(',')) and d[27] is not None:
                                kg["scissors_price"] = {}
                                sub = kg["scissors_price"]
                                sub["price"] = (d[13].split(',')[i] if d[13].split(',')[i] is not None else 0)
                                sub["consult"] = (d[27].split(',')[i] if d[27].split(',')[i] is not None else 0)

                            if d[14] is not None and d[14] != "" and i < len(d[14].split(',')) and d[28] is not None:
                                kg["summercut_price"] = {}
                                sub = kg["summercut_price"]
                                sub["price"] = (d[14].split(',')[i] if d[14].split(',')[i] is not None else 0)
                                sub["consult"] = (d[28].split(',')[i] if d[28].split(',')[i] is not None else 0)

                            if d[15] is not None and d[15] != "" and i < len(d[15].split(',')) and d[29] is not None:
                                kg["beauty1_price"] = {}
                                sub = kg["beauty1_price"]
                                sub["price"] = (d[15].split(',')[i] if d[15].split(',')[i] is not None else 0)
                                sub["consult"] = (d[29].split(',')[i] if d[29].split(',')[i] is not None else 0)

                            if d[16] is not None and d[16] != "" and i < len(d[16].split(',')) and d[30] is not None:
                                kg["beauty2_price"] = {}
                                sub = kg["beauty2_price"]
                                sub["price"] = (d[16].split(',')[i] if d[16].split(',')[i] is not None else 0)
                                sub["consult"] = (d[30].split(',')[i] if d[30].split(',')[i] is not None else 0)

                            if d[17] is not None and d[17] != "" and i < len(d[17].split(',')) and d[31] is not None:
                                kg["beauty3_price"] = {}
                                sub = kg["beauty3_price"]
                                sub["price"] = (d[17].split(',')[i] if d[17].split(',')[i] is not None else 0)
                                sub["consult"] = (d[31].split(',')[i] if d[31].split(',')[i] is not None else 0)

                            if d[18] is not None and d[18] != "" and i < len(d[18].split(',')) and d[32] is not None:
                                kg["beauty4_price"] = {}
                                sub = kg["beauty4_price"]
                                sub["price"] = (d[18].split(',')[i] if d[18].split(',')[i] is not None else 0)
                                sub["consult"] = (d[32].split(',')[i] if d[32].split(',')[i] is not None else 0)

                            if d[19] is not None and d[19] != "" and i < len(d[19].split(',')) and d[33] is not None:
                                kg["beauty5_price"] = {}
                                sub = kg["beauty5_price"]
                                sub["price"] = (d[19].split(',')[i] if d[19].split(',')[i] is not None else 0)
                                sub["consult"] = (d[33].split(',')[i] if d[33].split(',')[i] is not None else 0)
                            tmp["service"].append(kg)
                        body["dog"].append(tmp)
                    else:
                        body["etc_comment"] = d[40]

            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_CAT_PRODUCT_GET % (partner_id), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body["cat"] = {}
            if value is not None:
                for d in data:
                    tmp = body["cat"]
                    tmp["in_shop"] = d[3]
                    tmp["out_shop"] = d[4]
                    tmp["shower_price"] = d[9]
                    tmp["shower_price_long"] = d[10]
                    tmp["toenail_price"] = d[11]
                    tmp["hair_clot_price"] = d[13]
                    tmp["ferocity_price"] = d[14]
                    tmp["comment"] = d[18]
                    tmp["section"] = d[8]
                    tmp["increase_price"] = d[7]

                    if d[12] is not None and d[12] != '':
                        tmp['option'] = {}
                        addition = d[12].split(',')
                        for o in addition:
                            sub = tmp['option']
                            sub[o.split(':')[0]] = o.split(':')[1]

                    if d[16] is not None and d[16] != '':
                        tmp['shop_option'] = {}
                        addition = d[16].split(',')
                        for o in addition:
                            sub = tmp['shop_option']
                            sub[o.split(':')[0]] = o.split(':')[1]

                    tmp["is_use_weight"] = d[17]
                    if d[17] == "1":
                        kgs = d[8].split(',')
                        tmp["service"] = []
                        for i, k in enumerate(kgs):
                            kg = {}
                            kg["kg"] = k
                            kg["short_price"] = int(d[5]) + (int(d[7]) * i)
                            kg["long_price"] = int(d[6]) + (int(d[7]) * i)
                            tmp["service"].append(kg)
                    else:
                        tmp["short_price"] = d[5]
                        tmp["long_price"] = d[6]

            return 0, body
        except Exception as e:
            return -1, e.args[0]

    def getOptionProduct(self, partner_id):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_VAT_GET % (partner_id), QUERY_DB)
            #          ret = self.message.successOk()
            body = {}
            if value is not None:
                body["is_vat"] = value[0]

            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_OPTION_PRODUCT_GET % (partner_id), QUERY_DB)
            body["option"] = {}
            if value is not None:
                tmp = body["option"]
                tmp["idx"] = value[0]
                tmp["in_shop"] = value[4]
                tmp["out_shop"] = value[5]

                tmp["face"] = {}
                sub = tmp["face"]
                sub["basic"] = value[6]
                sub["broccoli"] = value[7]
                sub["highba"] = value[8]
                sub["bear"] = value[9]
                if value[38] is not None and value[38] != "":
                    face_etc = value[38].split(',')
                    for i, f in enumerate(face_etc):
                        sub[f.split(':')[0]] = f.split(':')[1]

                tmp["hair_len"] = {}
                sub = tmp["hair_len"]
                if value[10] is not None and value[10] != "":
                    sub[value[10]] = value[11]
                if value[12] is not None and value[12] != "":
                    sub[value[12]] = value[13]
                if value[14] is not None and value[14] != "":
                    sub[value[14]] = value[15]
                if value[16] is not None and value[16] != "":
                    sub[value[16]] = value[17]
                if value[18] is not None and value[18] != "":
                    sub[value[18]] = value[19]

                tmp["plus"] = {}
                sub = tmp["plus"]
                if value[20] is not None and value[20] != "":
                    sub['short_bath'] = value[20]
                if value[21] is not None and value[21] != "":
                    sub['long_bath'] = value[21]
                if value[22] is not None and value[22] != "":
                    sub['double_bath'] = value[22]

                tmp["place_plus"] = {}
                sub = tmp["place_plus"]
                if value[30] is not None and value[30] != "":
                    sub['hair_clot'] = value[30]
                if value[31] is not None and value[31] != "":
                    sub['ferocity'] = value[31]
                if value[32] is not None and value[32] != "":
                    sub['tick'] = value[32]

                tmp["etc"] = {}
                sub = tmp["etc"]
                sub["leg"] = {}
                small = sub["leg"]
                if value[23] is not None and value[23] != "":
                    small['toenail'] = value[23]
                if value[24] is not None and value[24] != "":
                    small['boots'] = value[24]
                if value[37] is not None and value[37] != "":
                    small['bell'] = value[37]
                if value[26] is not None and value[26] != "":
                    leg_etc = value[26].split(',')
                    for i, l in enumerate(leg_etc):
                        small[l.split(':')[0]] = l.split(':')[1]

                sub["spa"] = {}
                small = sub["spa"]
                if value[27] is not None and value[27] != "":
                    spa = value[27].split(',')
                    for i, s in enumerate(spa):
                        small[s.split(':')[0]] = s.split(':')[1]

                sub["dyeing"] = {}
                small = sub["dyeing"]
                if value[28] is not None and value[28] != "":
                    dyeing = value[28].split(',')
                    for i, d in enumerate(dyeing):
                        small[d.split(':')[0]] = d.split(':')[1]

                sub["etc_etc"] = {}
                small = sub["etc_etc"]
                if value[29] is not None and value[29] != "":
                    etc_etc = value[29].split(',')
                    for i, e in enumerate(etc_etc):
                        small[e.split(':')[0]] = e.split(':')[1]

            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_PLUS_OPTION_PRODUCT_GET % (partner_id), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value

            if value is not None:
                for d in data:
                    sub = tmp["plus"]
                    sub[d[3]] = d[4]

            return 0, body
        except Exception as e:
            return -1, e.args[0]
