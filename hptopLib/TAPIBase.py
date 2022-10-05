# -*- coding: utf-8 -*-
import traceback
from abc import abstractmethod
from datetime import datetime

from rest_framework.views import APIView

from apiShare import funcLib
from hptopLib.TDB import TDB
from hptopLib.TJson import TJson
from hptopLib.TMessage import TMessage
from apiShare.sqlQuery import *
from apiShare.constVar import QUERY_DB
from apiShare.funcLib import *

class TAPIBase(APIView):
    """
    기본 클래스.
    자주 사용하는 DB, JSON, MESSAGE를 정의하여
    상속된 하위 클래스에서 사용한다.
    """

    db = TDB()
    json = TJson()
    message = TMessage()

    # @abstractmethod
    # def procQuery(self, **kwargs):
    #     pass

    def queryDataToDic(self, data, rows, colums, ord = False):
        if ord:
            colums.append("ord_num")
        if rows < 2:
            body = {}
            i = 0
            for val in data:
                if colums[i] == "ord_num":
                    val = 1
                else:
                    if val is None:
                        body[colums[i]] = ""
                    else:
                        if type(val) is datetime:
                            body[colums[i]] = val.strftime("%Y%m%d%H%M%S")
                        else:
                            body[colums[i]] = val
                i += 1
        else:
            ord_cnt = 1
            body = []
            for d in data:
                k = {}
                i = 0
                for key in colums:
                    if key == "ord_num":
                        k[key] = ord_cnt
                    else:
                        if d[i] is None:
                            k[key] = ""
                        else:
                            if type(d[i]) is datetime:
                                k[key] = d[i].strftime("%Y%m%d%H%M%S")
                            else:
                                k[key] = d[i]
                    i += 1
                body.append(k)
                ord_cnt += 1
        return body

    def queryDataToSimpleDic(self, data, rows, keys):
        if rows < 2:
            body = {}
            i = 0
            for val in data:
                if val is None:
                    body[keys[i]] = ""
                else:
                    if type(val) is datetime:
                        body[keys[i]] = val.strftime("%Y%m%d%H%M%S")
                    else:
                        body[keys[i]] = val
                i += 1
        else:
            body = []
            for d in data:
                k = {}
                i = 0
                for key in keys:
                    if d[i] is None:
                        k[key] = ""
                    else:
                        if type(d[i]) is datetime:
                            k[key] = d[i].strftime("%Y%m%d%H%M%S")
                        else:
                            k[key] = d[i]
                    i += 1
                body.append(k)
        return body

    def datetimeToStr(self, dateTime, format):
        return datetime(dateTime).striftime(format)

    def setBeautyData(self, d):
        booking_st = "%s-%s-%s %s:%s" % (
            d[10], str(d[11]).zfill(2), str(d[12]).zfill(2), str(d[13]).zfill(2), str(d[14]).zfill(2))
        booking_fi = "%s-%s-%s %s:%s" % (
            d[10], str(d[11]).zfill(2), str(d[12]).zfill(2), str(d[15]).zfill(2), str(d[16]).zfill(2))
        # if d[36] is not None:
        #     p_split = d[36].split('|')
        # else:
        #     p_split = ("","")
        #price = totalPrice(d[36])

        customer = {"customer_id": d[2], "phone": d[17]}
        pet = {"idx": d[1], "animal": d[31], "type": d[32], "name": d[30], "photo":d[33]}  # 71~ 펫
        product = {
            "payment_idx": d[0],
            "worker": d[19],
            "is_no_show": d[21],
            "is_cancel": d[22],
            "category": "" if d[23] is None else  d[23].split('|')[3],
            "category_sub": "" if d[23] is None else  d[23].split('|')[4],
            "pay_type": d[18],    # pos-card 매장접수(카드), pos-cash:매장접수(현금), offline-card:앱예약 매장결제(카드), offline-cash:앱예약 매장결제(현금), card:앱예약 카드결제, bank:앱예약 계좌이체
            "pay_status": d[20],  # POS:매장접수 ///// [앱예약] R0:카드결제전, BR:계좌이체결제전, R1:결제완료, OR:매장결제
            "product_detail": d[23],
            "product_detail_parsing": {} if d[23] is None else self.productToDic(d[23]),
            "is_vat": True if d[24] == 1 else False,
           "origin_price": 0,
            "store_payment": {"discount_type": d[9], "discount": d[8], "card": d[6], "cash": d[7],
                              "reserve_point": d[5]},
            "app_payment": {"total_price": d[3], "spend_point": d[4]},
            "date": {"regist": str(d[26])  # self.datetimeToStr(d[62], d_format)
                , "booking_st": booking_st
                , "booking_fi": booking_fi},
            "memo": d[25],
            "approve_idx": d[34],
            "is_approve": d[35],  # 승인여부(0: 대기, 1: 보류, 2: 승인, 3: 반려, 4:견주가 취소 )
            "is_confirm": zeroToBool(d[27]),   # 결제완료여부, 돈 받았는지 확인용(0-미완료,1-완료)
            "noshow_cnt": d[36], # noshow 카운트
            "worker_nick": d[37],  # 미용사 닉네임
            "is_reserve_pay": d[38],
            "reserve_pay_price": d[39],
            "reserve_pay_yn": d[40],
            "reserve_pay_deadline": d[41],
            "reserve_pay_confirm_time": d[42]

        }
        tmp = {}
        tmp["customer"] = customer
        tmp["pet"] = pet
        tmp["product"] = product
        return tmp

    def setHotelData(self, d):

        customer = {"customer_id": d[2], "phone": d[3], "tmp_seq": d[4]}
        pet = {"idx": d[20], "animal": d[22], "type": d[23], "type2": d[24], "name": d[21], "photo":d[25]}  # 71~ 펫
        product = {
            "order_num": d[1],
            "artist_id": d[5],
            "etc_memo": d[11],
            "is_no_show": d[10],
            "is_cancel": d[12],
            "payment": {"product_price": d[6], "card": d[7], "cash": d[8], "total_price": d[9]},
            "date": {"check_in": d[14], "check_out": d[15]},
            "room_idx": d[13],
            "room_name": d[16],
            "weight": d[17],
            "room_sort": d[19]

        }
        tmp = {}
        tmp["customer"] = customer
        tmp["pet"] = pet
        tmp["product"] = product
        return tmp

    def getBodyHome(self, partner_id):
        try:
            yy = datetime.today().strftime("%Y")
            mm = datetime.today().strftime("%m")
            dd = datetime.today().strftime("%d")
            data, rows, columns = self.db.resultDBQuery(PROC_TOP_INFO_GET % (partner_id, yy, mm, dd), QUERY_DB)
            body = {}
            if data is not None:
                body["partner"] = True
                body["partner_id"] = partner_id
                body["shop_name"] = data[0]
                body["front_image"] = data[1]
                body["nick"] = data[2]
                body["consulting_count"] = data[3]
                body["schedule_count"] = data[4]
                body["new_review_count"] = data[5]
                body["total_count"] = data[6]
            value, rows, columns = self.db.resultDBQuery(PROC_SPETIAL_MALL_GET % (), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body["banner"] = []
            if value is not None:
                for d in data:
                    tmp = {}
                    tmp["idx"] = d[0]
                    tmp["title"] = d[2]
                    tmp["order"] = d[4]
                    tmp["link"] = d[5]
                    tmp["image"] = d[6]
                    tmp["is_use_period"] = True if d[7] == 1 else False
                    tmp["start_dt"] = d[8].strftime("%Y-%m-%d %H:%M:%S") if d[8] is not None else ""
                    tmp["end_dt"] = d[9].strftime("%Y-%m-%d %H:%M:%S") if d[9] is not None else ""
                    body["banner"].append(tmp)
            value, rows, columns = self.db.resultDBQuery(PROC_NOTICE_MGR_GET % (0, "", ""), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body["notice"] = []
            if value is not None:
                for d in data:
                    tmp = {}
                    tmp["idx"] = d[0]
                    tmp["title"] = d[2]
                    tmp["contents"] = d[3]
                    tmp["type"] = d[4]      # 타입(0-공지, 1-업데이트, 2-일반)
                    tmp["is_show"] = d[5]      # 메인 노출여부(0-미노출, 1-노출)
                    tmp["image"] = d[6]
                    tmp["reg_date"] = d[8].strftime("%Y-%m-%d %H:%M:%S") if d[8] is not None else ""
                    body["notice"].append(tmp)

            value, rows, columns = self.db.resultDBQuery(PROC_CONSULT_MGR_GET % (partner_id,), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body["consulting"] = []
            if value is not None:
                for d in data:
                    tmp = {}
                    tmp['payment_log_seq'] = d[25]
                    tmp["approval"] = d[0]  # 0:첫이용상담신청, 1:미용, 2:첫이용상담수락, 3:첫이용상담거절
                    tmp["date"] = str(d[1])
                    tmp["user"] = d[3]
                    tmp["user_name"] = d[4]
                    tmp["phone"] = d[5]
                    tmp["pet_id"] = d[6]
                    tmp["pet_name"] = d[7]
                    tmp["pet_type"] = d[8]

                    tmp["birth"] = d[9]
                    tmp["gender"] = d[10]
                    tmp["neutral"] = zeroToBool(d[11])
                    tmp["weight"] = d[12]
                    tmp["photo"] = d[13]
                    tmp["beauty_exp"] = d[14]
                    tmp["vaccination"] = d[15]
                    tmp["bite"] = d[16]
                    tmp["heart_trouble"] = zeroToBool(d[17])
                    tmp["marking"] = zeroToBool(d[18])
                    tmp["mounting"] = zeroToBool(d[19])
                    tmp["luxation"] = d[20]
                    tmp["dermatosis"] = zeroToBool(d[21])
                    tmp["photocounseling"] = d[22]
                    tmp["memo"] = d[23]
                    tmp['disliked_part'] = d[24]

                    photo = []
                    try:
                        if d[22] is not None and len(d[22]) > 0:
                            code = tmp["photocounseling"].split(',')
                            for c in code:
                                value2, rows2, columns2 = self.db.resultDBQuery(PROC_CONSULT_PHOTO_GET % (c,),QUERY_DB)
                                if value2 is not None:
                                    p = {"photo": value2[3]}
                                    photo.append(p)
                    except Exception as e:
                        print(e.args[0])
                    tmp["consult_photo"]=photo
                    body["consulting"].append(tmp)

#==================================================================================================================================================

            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_GET_OPT % (partner_id, yy, mm), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body["beauty"] = []
            if value is not None:
                for d in data:
                    body["beauty"].append(self.setBeautyData(d))

            value, rows, columns = self.db.resultDBQuery(PROC_HOTEL_BOOKING_GET % (partner_id, yy, mm), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body["hotel"] = []
            if value is not None:
                for d in data:
                    tmp = {}
                    d_format = "%Y-%m-%d %H:%M:%S"
                    check_in = "%s %s" % (d[47], d[48])
                    check_out = "%s %s" % (d[49], d[50])

                    customer = {"customer_id": d[2], "phone": d[3]}
                    pet = {"pet_seq": d[66], "animal": d[69], "type": d[70], "name": d[68]}  # 66~ 펫
                    product = {
                        "idx": d[1],
                        "partner_id": d[6],
                        "is_no_show": d[29],
                        "receipt_type": d[20],  # 접수방법(1-android,2-iOS,3-매장(POS)0-선택없음)
                        "pay_type": d[21],  # 결제방법(1-PG, 2-계좌이체, 0-선택없음)
                        "pay_status": d[22],  # 결제상태(1-진행중, 2-입금대기, 3-결제완료, 8-보류, 9-실패)
                        "payment": {"point": d[16], "card": d[17], "cash": d[18], },
                        "date": {"regist": str(d[34])  # self.datetimeToStr(d[34], d_format)
                            , "check_in": check_in
                            , "check_out": check_out},
                        "memo": d[31]
                    }
                    tmp["customer"] = customer
                    tmp["pet"] = pet
                    tmp["product"] = product
                    body["hotel"].append(tmp)
            value, rows, columns = self.db.resultDBQuery(PROC_KINDERGADEN_BOOKING_GET % (partner_id, yy, mm), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body["kindergarden"] = []
            if value is not None:
                for d in data:
                    tmp = {}
                    d_format = "%Y-%m-%d %H:%M:%S"
                    check_in = "%s %s" % (d[48], d[49])
                    check_out = "%s %s" % (d[50], d[51])

                    customer = {"customer_id": d[2], "phone": d[3]}
                    pet = {"pet_seq": d[69], "animal": d[72], "type": d[73], "name": d[71]}  # 69~ 펫
                    product = {
                        "idx": d[1],
                        "partner_id": d[6],
                        "is_no_show": d[29],
                        "receipt_type": d[20],  # 접수방법(1-android,2-iOS,3-매장(POS)0-선택없음)
                        "pay_type": d[21],  # 결제방법(1-PG, 2-계좌이체, 0-선택없음)
                        "pay_status": d[22],  # 결제상태(1-진행중, 2-입금대기, 3-결제완료, 8-보류, 9-실패)
                        "payment": {"point": d[16], "card": d[17], "cash": d[18], },
                        "date": {"regist": str(d[34])  # self.datetimeToStr(d[34], d_format)
                            , "check_in": check_in
                            , "check_out": check_out},
                        "memo": d[31]
                    }
                    tmp["customer"] = customer
                    tmp["pet"] = pet
                    tmp["product"] = product
                    body["kindergarden"].append(tmp)

# ==================================================================================================================================================
            return 0, body
        except Exception as e:
            return -1, e.args[0]

    def getBodyHomePeriodStatus(self, partner_id, yy, mm):
        try:
            body = {}
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_GET_OPT % (partner_id, yy, mm), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body["beauty"] = []
            if value is not None:
                for d in data:
                    body["beauty"].append(self.setBeautyData(d))

            value, rows, columns = self.db.resultDBQuery(PROC_HOTEL_BOOKING_GET % (partner_id, yy, mm), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body["hotel"] = []
            if value is not None:
                for d in data:
                    tmp = {}
                    d_format = "%Y-%m-%d %H:%M:%S"
                    check_in = "%s %s" % (d[47], d[48])
                    check_out = "%s %s" % (d[49], d[50])

                    customer = {"customer_id": d[2], "phone": d[3]}
                    pet = {"pet_seq": d[66], "animal": d[69], "type": d[70], "name": d[68]}  # 66~ 펫
                    product = {
                        "idx": d[1],
                        "partner_id": d[6],
                        "is_no_show": d[29],
                        "receipt_type": d[20],  # 접수방법(1-android,2-iOS,3-매장(POS)0-선택없음)
                        "pay_type": d[21],  # 결제방법(1-PG, 2-계좌이체, 0-선택없음)
                        "pay_status": d[22],  # 결제상태(1-진행중, 2-입금대기, 3-결제완료, 8-보류, 9-실패)
                        "payment": {"point": d[16], "card": d[17], "cash": d[18], },
                        "date": {"regist": str(d[34])  # self.datetimeToStr(d[34], d_format)
                            , "check_in": check_in
                            , "check_out": check_out},
                        "memo": d[31]
                    }
                    tmp["customer"] = customer
                    tmp["pet"] = pet
                    tmp["product"] = product
                    body["hotel"].append(tmp)

            value, rows, columns = self.db.resultDBQuery(PROC_KINDERGADEN_BOOKING_GET % (partner_id, yy, mm), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body["kindergarden"] = []
            if value is not None:
                for d in data:
                    tmp = {}
                    d_format = "%Y-%m-%d %H:%M:%S"
                    check_in = "%s %s" % (d[48], d[49])
                    check_out = "%s %s" % (d[50], d[51])

                    customer = {"customer_id": d[2], "phone": d[3]}
                    pet = {"pet_seq": d[69], "animal": d[72], "type": d[73], "name": d[71]}  # 69~ 펫
                    product = {
                        "idx": d[1],
                        "partner_id": d[6],
                        "is_no_show": d[29],
                        "receipt_type": d[20],  # 접수방법(1-android,2-iOS,3-매장(POS)0-선택없음)
                        "pay_type": d[21],  # 결제방법(1-PG, 2-계좌이체, 0-선택없음)
                        "pay_status": d[22],  # 결제상태(1-진행중, 2-입금대기, 3-결제완료, 8-보류, 9-실패)
                        "payment": {"point": d[16], "card": d[17], "cash": d[18], },
                        "date": {"regist": str(d[34])  # self.datetimeToStr(d[34], d_format)
                            , "check_in": check_in
                            , "check_out": check_out},
                        "memo": d[31]
                    }
                    tmp["customer"] = customer
                    tmp["pet"] = pet
                    tmp["product"] = product
                    body["kindergarden"].append(tmp)
            return 0, body
        except Exception as e:
            return -1, e.args[0]

    def getBodyBooking(self, partner_id):
        try:
            yy = datetime.today().strftime("%Y")
            mm = datetime.today().strftime("%m")
            dd = datetime.today().strftime("%d")
            # data, rows, columns = self.db.resultDBQuery(PROC_TOP_INFO_GET % (partner_id, yy, mm, dd), QUERY_DB)
            # #          ret = self.message.successOk()
            # body = {}
            # if data is not None:
            #     body["shop_name"] = data[0]
            # return 0, body
            value, rows, columns = self.db.resultDBQuery(PROC_WORKER_TO_CEO_GET % (partner_id), QUERY_DB)
            data = []
            body = {"partner": False, "partner_id": partner_id, "beauty": []}

            if rows == 1:
                data.append(value)
            elif rows > 1:
                data = value
            if value is not None:
                for d in data:
                    body["beauty"].append(self.setBeautyData(d))
            return 0, body
        except Exception as e:
            return -1, e.args[0]


    def productToDic(self, product):
        if product == "" or product.find("|") < 0:
            return product
        p_split = product.split("|")
        if not p_split[1].strip() in ("개", "고양이"):
            return product
        if p_split[1].strip() == "개":
            return self.typeDog(product)
        else:
            return self.typeCat(product)

    def typeDog(self,product):
        try:
            p_split = product.split("|")
            products = {
                "name": p_split[0],
                "animal": p_split[1],
                "shop": p_split[2],
                "base": {
                    "size": p_split[3],
                    "beauty_kind": p_split[4],
                    "weight": {
                        "unit": subSplit(p_split[5], ":")[0],
                        "price": subSplit(p_split[5], ":")[1]
                    },
                    "hair_features": setArr(p_split[8]),
                    "hair_lenth": {
                        "unit": subSplit(p_split[7], ":")[0],
                        "price": subSplit(p_split[7], ":")[1]
                    }
                },
                "add": {
                    "face": {
                        "unit": subSplit(p_split[6], ":")[0],
                        "price": subSplit(p_split[6], ":")[1]
                    },
                    "leg": {

                        "nail": {
                            "unit": "네일",
                            "price": p_split[9]
                        },
                        "rain_boots": {
                            "unit": "장화",
                            "price": p_split[10],
                        },
                        "bell": {
                            "unit":"방울",
                            "price": p_split[11]
                        }
                    }
                }
            }
            pos = 14
            if len(p_split) > pos and p_split[pos].strip() != "":# and int(p_split[pos]) > 0:  # 스파 개수
                if p_split[pos].isdigit():
                    max = int(p_split[pos])
                    for i in range(0, max):
                        products["add"]["leg"]["type"+str(i+1)] = {}
                        products["add"]["leg"]["type"+str(i+1)]["unit"] = p_split[pos+1].split(":")[0]
                        products["add"]["leg"]["type"+str(i+1)]["price"] = p_split[pos+1].split(":")[1]
                        pos += 1
            pos += 1
            if len(p_split) > pos and p_split[pos].strip() != "":# and int(p_split[pos]) > 0:  # 스파 개수
                if p_split[pos].isdigit():
                    count, body = setOffSet(pos, int(p_split[pos]), p_split)
                    products["add"]["spa"] = body
                    pos += count
            pos += 1
            if len(p_split) > pos and p_split[pos].strip() != "":# and int(p_split[pos]) > 0:  # 염색 개수
                if p_split[pos].isdigit():
                    count, body = setOffSet(pos, int(p_split[pos]), p_split)
                    products["add"]["hair_color"] = body
                    pos += count
            pos += 1
            if len(p_split) > pos and p_split[pos].strip() != "":# and int(p_split[pos]) > 0:  # 기타
                if p_split[pos].isdigit():
                    count, body = setOffSet(pos, int(p_split[pos]), p_split)
                    products["add"]["etc"] = body
                    pos += count
            pos += 1
            if len(p_split) > pos and p_split[pos].strip() != "":# and int(p_split[pos]) > 0:  # 쿠폰상품
                if p_split[pos].isdigit():
                    count, body = setOffSet(pos, int(p_split[pos]), p_split)
                    products["coupon"] = body
                    pos += count
            pos += 1

            if len(p_split) > pos and p_split[pos].strip() != "":# and int(p_split[pos]) > 0:  # 제품
                if p_split[pos].isdigit():
                    count, body = setOffSet(pos, int(p_split[pos]), p_split)
                    products["goods"] = body
                    pos += count

            return products
        except Exception as e:
            print(e.args[0], "[%d : %s] => %s"%(pos,p_split[pos],product), )

    def typeCat(self, product):
        try:
            p_split = product.split("|")
            products = {
                "name": p_split[0],
                "animal": p_split[1],
                "shop": p_split[2],
                "category": p_split[3],
                "base": {
                    "weight": {
                        "unit": subSplit(p_split[4], ":")[0],
                        "price": subSplit(p_split[4], ":")[1]
                    },
                    "hair_beauty": p_split[5],
                    "bath_shot": p_split[7],
                    "bath_long": p_split[8]
                },
                "add": {
                    "nail": p_split[6]
                }
            }
            pos = 9
            if len(p_split) > pos and p_split[pos].strip() != "" and int(p_split[pos]) > 0:  # 기타
                count, body = setOffSet(pos, int(p_split[pos]), p_split)
                products["add"]["etc"] = body
                pos += count
            pos += 1
            if len(p_split) > pos and p_split[pos].strip() != "" and int(p_split[pos]) > 0:  # 쿠폰상품
                count, body = setOffSet(pos, int(p_split[pos]), p_split)
                products["coupon"] = body
                pos += count
            pos += 1
            if len(p_split) > pos and p_split[pos].strip() != "" and int(p_split[pos]) > 0:  # 제품
                count, body = setOffSet(pos, int(p_split[pos]), p_split)
                products["goods"] = body
                pos += count

            return products
        except Exception as e:
            print(e.args[0])

    def getArtistWorkInfo(self, partner_id):
        try:
            # 작업
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_ARTIST_WORKING_GET % (partner_id,), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body = []
            if value is not None:
                for d in data:
                    tmp = {}
                    artist = []
                    tmp["ord"] = d[0]
                    tmp["name"] = d[2]
                    tmp["nick"] = d[3]
                    tmp["is_host"] = True if d[4] == 1 else False
                    tmp["is_leave"] = True if d[5] == 1 else False
                    tmp["is_show"] = True if d[6] == 2 else False
                    sub = d[7].split(',')
                    for s in sub:
                        resub = s.split('|')
                        artist.append({"idx": resub[0], "week": resub[1], "time_st": resub[2], "time_fi": resub[3]})
                    tmp["work"] = artist
                    body.append(tmp)
            return 0, "success", body
        except Exception as e:
            return -1, e.args[1], None

    def getArtistWorkInfo1(self, partner_id, body):
        # 작업
        value, rows, columns = self.db.resultDBQuery(PROC_SETTING_ARTIST_WORKING_GET % (partner_id,), QUERY_DB)
        data = []
        if rows < 2:
            data.append(value)
        else:
            data = value
        body = []
        before_name = ""
        if value is not None:
            for d in data:
                if before_name == "" or before_name != d[2]:
                    if before_name != "" and before_name != d[2]:
                        tmp["work"] = artist
                        body.append(tmp)
                    tmp = {}
                    artist = []
                    tmp["name"] = d[2]
                    tmp["nick"] = d[3]
                    tmp["is_host"] = True if d[4] == 1 else False
                    tmp["is_leave"] = True if d[5] == 1 else False
                    tmp["is_show"] = True if d[6] == 2 else False
                    tmp["ord"] = d[10]
                    artist.append({"seq": d[0], "week": d[7], "time_st": d[8], "time_fi": d[9]})
                    before_name = d[2]
                else:
                    artist.append({"seq": d[0], "week": d[7], "time_st": d[8], "time_fi": d[9]})
                    before_name = d[2]
            tmp["work"] = artist
            body.append(tmp)
        # 휴가
        value, rows, columns = self.db.resultDBQuery(PROC_SETTING_PERSONAL_VACATION_GET % (partner_id,), QUERY_DB)
        data = []
        if rows < 2:
            data.append(value)
        else:
            data = value

        return body

    def frameInfo(self, f, err):
        return "[PATH: %s, LINE: %s, FUNC: %s, ERR: %s" % (f.filename, f.lineno, f.function, err)

    def errorInfo(self, err):
        return traceback.format_exc()

