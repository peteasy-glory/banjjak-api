# -*- coding: utf-8 -*-
from abc import abstractmethod
from datetime import datetime

from rest_framework.views import APIView

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

    def queryDataToDic(self, data, rows, colums):
        if rows < 2:
            body = {}
            i = 0
            for val in data:
                if val is None:
                    body[colums[i]] = ""
                else:
                    if type(val) is datetime:
                        body[colums[i]] = val.strftime("%Y%m%d%H%M%S")
                    else:
                        body[colums[i]] = val
                i += 1
        else:
            body = []
            for d in data:
                k = {}
                i = 0
                for key in colums:
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
            d[23], str(d[24]).zfill(2), str(d[25]).zfill(2), str(d[26]).zfill(2), str(d[27]).zfill(2))
        booking_fi = "%s-%s-%s %s:%s" % (
            d[23], str(d[24]).zfill(2), str(d[25]).zfill(2), str(d[31]).zfill(2), str(d[32]).zfill(2))
        p_split = d[36].split('|')
        price = totalPrice(d[36])

        customer = {"customer_id": d[3], "phone": d[39]}
        pet = {"idx": d[1], "animal": d[74], "type": d[75], "name": d[73], "photo":d[77]}  # 71~ 펫
        product = {
            "payment_idx": d[0],
            "worker": d[18],
            "is_no_show": d[51],
            "is_cancel": d[50],
            "category": p_split[3],
            "category_sub": p_split[4],
            "pay_type": d[40],
            # pos-card 매장접수(카드), pos-cash:매장접수(현금), offline-card:앱예약 매장결제(카드), offline-cash:앱예약 매장결제(현금), card:앱예약 카드결제, bank:앱예약 계좌이체
            "pay_status": d[19],  # POS:매장접수 ///// [앱예약] R0:카드결제전, BR:계좌이체결제전, R1:결제완료, OR:매장결제
            "product_detail": d[36],
            "is_vat": True if d[59] == 1 else False,
            "origin_price": price,
            "store_payment": {"discount_type": d[15], "discount": d[16], "card": d[13], "cash": d[14],
                              "reserve_point": d[9]},
            "app_payment": {"total_price": d[7], "spend_point": d[8]},
            "date": {"regist": str(d[62])  # self.datetimeToStr(d[62], d_format)
                , "booking_st": booking_st
                , "booking_fi": booking_fi},
            "memo": d[58],
            "is_approve": d[76]  # 승인여부(0: 대기, 1: 보류, 2: 승인, 3: 반려, 4:견주가 취소 )
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
            #          ret = self.message.successOk()
            body = {}
            if data is not None:
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
            value, rows, columns = self.db.resultDBQuery(PROC_CONSULT_MGR_GET % (partner_id), QUERY_DB)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            body["consulting"] = []
            if value is not None:
                for d in data:
                    tmp = {}
                    tmp["approval"] = d[0]  # 0:첫이용상담신청, 1:미용, 2:첫이용상담수락, 3:첫이용상담거절
                    tmp["date"] = d[1]
                    tmp["user"] = d[3]
                    tmp["user_name"] = d[4]
                    tmp["phone"] = d[5]
                    tmp["pet_id"] = d[6]
                    tmp["pet_name"] = d[7]
                    tmp["pet_type"] = d[8]
                    body["consulting"].append(tmp)

            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_GET % (partner_id, yy, mm), QUERY_DB)
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

    def getBodyHomePeriodStatus(self, partner_id, yy, mm):
        try:
            body = {}
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_GET % (partner_id, yy, mm), QUERY_DB)
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
            data, rows, columns = self.db.resultDBQuery(PROC_TOP_INFO_GET % (partner_id, yy, mm, dd), QUERY_DB)
            #          ret = self.message.successOk()
            body = {}
            if data is not None:
                body["shop_name"] = data[0]
            return 0, body
        except Exception as e:
            return -1, e.args[0]

    def getArtistList(self, partner_id):
        try:
            data, rows, columns = self.db.resultDBQuery(PROC_SETTING_ARTIST_GET % (partner_id), QUERY_DB)
            #          ret = self.message.successOk()
            body = {}
            body["artist"] = []
            if data is not None:
                for d in data:
                    tmp = {}
                    tmp["name"] = d[0]
                    tmp["nickname"] = d[1]
                    tmp["is_main"] = d[2]
                    tmp["is_out"] = d[3]
                    tmp["is_view"] = d[4]
                    tmp["week_list"] = []

                    seq_list = d[8].split(',')
                    week_list = d[5].split(',')
                    start_list = d[6].split(',')
                    end_list = d[7].split(',')

                    for i, d_1 in enumerate(seq_list):
                        tmp_1 = {}
                        tmp_1["seq"] = seq_list[i]
                        tmp_1["week"] = week_list[i]
                        tmp_1["time_start"] = start_list[i]
                        tmp_1["time_end"] = end_list[i]

                        tmp["week_list"].append(tmp_1)


                    body["artist"].append(tmp)


            return 0, body
        except Exception as e:
            return -1, e.args[0]