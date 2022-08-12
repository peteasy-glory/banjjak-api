# -*- coding: utf-8 -*-
import traceback

from django.http import HttpResponse
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase
from hptopLib.TAPIBookingBase import TAPIBookingBase


class TBooking(TAPIBase):

    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            body = []
            if request.GET.get('st_date') is not None and request.GET.get('fi_date') is not None:
                st_date = request.GET.get('st_date')
                fi_date = request.GET.get('fi_date')
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PEROID_GET % (partner_id, st_date, fi_date), QUERY_DB)
                data = []
                if rows < 2:
                    data.append(value)
                else:
                    data = value
                if value is not None:
                    for d in data:
                        body.append(self.setBeautyData(d))
            else:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            ret = self.message.successOk()
            ret["body"] = body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return self.errorInfo(e)


class TBookingJoin(TAPIBase):

    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            if request.GET.get('animal') is not None:
                if request.GET.get('animal') == "dog":
                    ret = self.setDogData(partner_id=partner_id)
                elif request.GET.get('animal') == "cat":
                    ret = self.setCatData(partner_id=partner_id)
                else:
                    return HttpResponse(self.json.dicToJson(self.message.errorParametaRequst()))
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            msg = self.errorInfo(e)
            return HttpResponse(self.json.dicToJson(self.message.error(msg)))

    def setDogData(self, partner_id):
        value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PREDATA_STATIC_GET % (partner_id,), QUERY_DB)
        ret = self.message.successOk()
        if value is None:
            ret["body"] = {}
            return ret
        data = []
        if rows < 2:
            data.append(value)
        else:
            data = value
        value2, rows2, columns2 = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PREDATA_COMMON_GET % (partner_id,),
                                                        QUERY_DB)
        data2 = []
        if rows2 < 2:
            data2.append(value2)
        else:
            data2 = value2
        value3, rows3, columns3 = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PREDATA_WORKTIME_GET % (partner_id,),
                                                        QUERY_DB)
        data3 = []
        if rows2 < 2:
            data3.append(value3)
        else:
            data3 = value3
        ret["body"] = self.setPreData(static=data, common=data2, worktime=data3, partner_id=partner_id)
        return ret

    def setCatData(self, partner_id):
        value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PREDATA_CAT_GET % (partner_id,), QUERY_DB)
        ret = self.message.successOk()
        if value is None:
            ret["body"] = {}
            return ret
        data = []
        if rows < 2:
            data.append(value)
        else:
            data = value
        body = {"in_shop": data[0][3], "out_shop": data[0][4], "is_use_weight": data[0][17],
               "beauty": [{"type":"단모_미용", "price": data[0][5]},{"type":"장모_미용", "price": data[0][6]}],
                "bath": [{"type": "단모", "price": data[0][9]},{"type":"장모", "price": data[0][10]}],
                "add_svc": [{"type":"발톱", "price": data[0][11]}],
                "add_opt": [{"type":"털엉킴", "price": data[0][13]},{"type":"사나움", "price": data[0][14]},{"type":"진드기", "price": data[0][15]}],
                "comment": data[0][18]
               }
        add = data[0][12].split(",")
        for a in add:
            s = a.split(":")
            body["add_svc"].append({"type":s[0], "price":s[1]})
        add = data[0][16].split(",")
        for a in add:
            s = a.split(":")
            body["add_opt"].append({"type":s[0], "price":s[1]})
        return  body


    def setPreData(self, static, common, worktime, partner_id):
        base_type = ["목욕", "부분미용", "부분+목욕", "위생", "위생+목욕", "전체미용", "스포팅", "가위컷", "썸머컷"]
        lenth_type = ["4mm","4mm","13mm","9mm","4mm"]
        face_type = ["기본얼굴컷", "브로콜리컷", "하이바컷", "곰돌이컷"]
        leg_type = ["발톱", "장화"]
        add_opt = ["털엉킴", "사나움", "진드기"]

        body = {"in_shop": common[0][4], "out_shop": common[0][5],
               "face": [], "leg": [], "spa": [], "dyeing": [], "etc": [], "add_opt": [], "comment": common[0][39],
                "hair_feature": [{"type": "단모_목욕", "price": common[0][20]},
                                 {"type": "장모_목욕", "price": common[0][21]},
                                 {"type": "이중모_목욕", "price": common[0][22]}],
                "hair_length": [],
                "base_svc": []
               }

        value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PREDATA_COMMON_OPTION_GET % (partner_id,), QUERY_DB)
        data = []
        if rows < 2:
            data.append(value)
        else:
            data = value
        for d in data:
            body["hair_feature"].append({"type": d[3], "price": str(d[4])})

        for i in range(len(face_type)):
            body["face"].append({"type": face_type[i], "price": common[0][6 + i]})
        sub_face = common[0][38].split(",")
        for face in sub_face:
            unit = face.split(":")
            body["face"].append({"type": unit[0], "price": unit[1]})
        for i in range(len(leg_type)):
            body["leg"].append({"type": leg_type[i], "price": common[0][23 + i]})
        body["leg"].append({"type": "방울", "price": common[0][37]})
        sub_leg = common[0][26].split(",")
        for leg in sub_leg:
            unit = leg.split(":")
            body["leg"].append({"type": unit[0], "price": unit[1]})
        sub_spa = common[0][27].split(",")
        for spa in sub_spa:
            unit = spa.split(":")
            body["spa"].append({"type": unit[0], "price": unit[1]})
        sub_dyeing = common[0][28].split(",")
        for dyeing in sub_dyeing:
            unit = dyeing.split(":")
            body["dyeing"].append({"type": unit[0], "price": unit[1]})
        sub_etc = common[0][29].split(",")
        for etc in sub_etc:
            unit = etc.split(":")
            body["etc"].append({"type": unit[0], "price": unit[1]})
        for i in range(len(add_opt)):
            body["add_opt"].append({"type": add_opt[i], "price": common[0][30 + i]})
        sub_add_opt = common[0][33].split(",")
        for add in sub_add_opt:
            unit = add.split(":")
            body["add_opt"].append({"type": unit[0], "price": unit[1]})
        for i in range(len(lenth_type)):
            body["hair_length"].append({"type": lenth_type[i], "price":common[0][i+10]})
        sub_hair = common[0][34].split(",")
        for h in sub_hair:
            unit = h.split(":")
            body["hair_length"].append({"type": unit[0]+"mm", "price": unit[1]})

        for s in static:
            tmp = {"size": s[2], "in_shop": s[4], "out_shop": s[5],
                   "surcharge": {"is_have": s[36], "kg": s[38], "price": s[39]},
                   "comment": s[40],
                   "svc": []}
            for i in range(14):
                if i < 9:
                    sub_svc = {"type": base_type[i], "time": worktime[0][2+i], "is_show":worktime[0][21+i]}
                else:
                    sub_svc = {"type": worktime[0][i+7], "time": worktime[0][2+i], "is_show":worktime[0][21+i]}

                p_k = []
                if s[i+6] is not None and len(s[i+6]) > 0:
                    sub_price = s[i+6].split(",")
                    sub_kg = s[35].split(",")
                    sub_consult = s[i+20].split(",")
                    for j in range(len(sub_kg)):
                        p_k.append({"kg":sub_kg[j], "price":sub_price[j], "is_consulting":sub_consult[j]})
                sub_svc["unit"] = p_k
                tmp["svc"].append(sub_svc)
            body["base_svc"].append(tmp)
        return body
















