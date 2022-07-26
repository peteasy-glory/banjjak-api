# -*- coding: utf-8 -*-
from datetime import datetime

from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase
from hptopLib.TSha256 import TSha256


class THome(TAPIBase):
    """

    홈 메인
    - 성공시
       : 메인 화면에 보여줄 정보를 전송

    - 실패시
       : 실패 코드 및 메세지만 전송

    - 로그아웃의 경우 클라이언트/웹서버만으로 처리

    """
    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            yy = datetime.today().strftime("%Y")
            mm = datetime.today().strftime("%m")
            dd = datetime.today().strftime("%d")
            data, rows, columns = self.db.resultDBQuery(PROC_TOP_INFO_GET % (partner_id, yy,mm, dd), QUERY_DB)
  #          ret = self.message.successOk()
            body = {}
            if data is not None:
                body["shop_name"] = data[0]
                body["consulting_count"] = data[1]
                body["schedule_count"] = data[2]
                body["new_review_count"] = data[3]
                body["total_count"] = data[4]
            data, rows, columns = self.db.resultDBQuery(PROC_SPETIAL_MALL_GET % (), QUERY_DB)
            body["banner"] = []
            if data is not None:
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
            data, rows, columns = self.db.resultDBQuery(PROC_NOTICE_MGR_GET % (0, "", ""), QUERY_DB)
            body["notice"] = []
            if data is not None:
                for d in data:
                    tmp = {}
                    tmp["idx"] = d[0]
                    tmp["title"] = d[2]
                    tmp["order"] = d[4]
                    tmp["link"] = d[5]
                    tmp["image"] = d[6]
                    tmp["is_use_period"] = True if d[7] == 1 else False
                    tmp["reg_date"] = d[8].strftime("%Y-%m-%d %H:%M:%S") if d[8] is not None else ""
                    body["notice"].append(tmp)
            data, rows, columns = self.db.resultDBQuery(PROC_CONSULT_MGR_GET % (partner_id), QUERY_DB)
            body["consulting"] = []
            if data is not None:
                for d in data:
                    tmp = {}
                    tmp["approval"] = d[0] #0:첫이용상담신청, 1:미용, 2:첫이용상담수락, 3:첫이용상담거절
                    tmp["date"] = d[1]
                    tmp["user"] = d[3]
                    tmp["user_name"] = d[4]
                    tmp["phone"] = d[5]
                    tmp["pet_id"] = d[6]
                    tmp["pet_name"] = d[7]
                    tmp["pet_type"] = d[8]
                    body["consulting"].append(tmp)
            data, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_GET % (partner_id, yy, mm), QUERY_DB)
            body["beauty"] = []
            if data is not None:
                for d in data:
                    tmp = {}
                    d_format = "%Y-%m-%d %H:%M:%S"
                    booking_st = "%s-%s-%s %s:%s" % (d[23],str(d[24]).zfill(2),str(d[25]).zfill(2),str(d[26]).zfill(2),str(d[27]).zfill(2))
                    booking_fi = "%s-%s-%s %s:%s" % (d[23],str(d[24]).zfill(2),str(d[25]).zfill(2),str(d[31]).zfill(2),str(d[32]).zfill(2))
                    p_split = d[36].split('|')
                    customer = {"customer_id":d[3], "phone":d[39]}
                    pet = {"pet_seq":d[1], "animal":d[74], "type":d[75],"name":d[73] } #71~ 펫
                    product = {
                        "payment_idx":d[0],
                        "worker": d[18],
                        "is_no_show": d[51],
                        "is_cancel":d[50],
                        "category": p_split[3],
                        "pay_status": d[19],  # POS:매장접수 ///// [앱예약] R0:카드결제전, BR:계좌이체결제전, R1:결제완료, OR:매장결제
                        "post_payment" : {"card":d[13], "cash":d[14], "reserve_point":d[9]},
                        "pre_payment": {"total_price": d[7], "spend_point": d[8]},
                        "date": {"regist" : str(d[62]) # self.datetimeToStr(d[62], d_format)
                                , "booking_st":booking_st
                                , "booking_fi": booking_fi},
                        "memo": d[58]
                    }
                    tmp["customer"] = customer
                    tmp["pet"] = pet
                    tmp["product"] = product
                    body["beauty"].append(tmp)

            data, rows, columns = self.db.resultDBQuery(PROC_HOTEL_BOOKING_GET % (partner_id, yy, mm), QUERY_DB)
            body["hotel"] = []
            if data is not None:
                for d in data:
                    tmp = {}
                    d_format = "%Y-%m-%d %H:%M:%S"
                    check_in = "%s %s" % (d[47],d[48])
                    check_out = "%s %s" % (d[49],d[50])

                    customer = {"customer_id":d[2], "phone":d[3]}
                    pet = {"pet_seq":d[66], "animal":d[69], "type":d[70],"name":d[68] } #66~ 펫
                    product = {
                        "idx":d[1],
                        "partner_id": d[6],
                        "is_no_show": d[29],
                        "receipt_type": d[20],    # 접수방법(1-android,2-iOS,3-매장(POS)0-선택없음)
                        "pay_type": d[21],        # 결제방법(1-PG, 2-계좌이체, 0-선택없음)
                        "pay_status": d[22],    # 결제상태(1-진행중, 2-입금대기, 3-결제완료, 8-보류, 9-실패)
                        "payment" : {"point":d[16], "card":d[17], "cash":d[18], },
                        "date": {"regist" : str(d[34]) #self.datetimeToStr(d[34], d_format)
                                , "check_in": check_in
                                , "check_out": check_out},
                        "memo": d[31]
                    }
                    tmp["customer"] = customer
                    tmp["pet"] = pet
                    tmp["product"] = product
                    body["hotel"].append(tmp)

            data, rows, columns = self.db.resultDBQuery(PROC_KINDERGADEN_BOOKING_GET % (partner_id, yy, mm), QUERY_DB)
            body["kindergarden"] = []
            if data is not None:
                for d in data:
                    tmp = {}
                    d_format = "%Y-%m-%d %H:%M:%S"
                    check_in = "%s %s" % (d[48],d[49])
                    check_out = "%s %s" % (d[50],d[51])

                    customer = {"customer_id":d[2], "phone":d[3]}
                    pet = {"pet_seq":d[69], "animal":d[72], "type":d[73],"name":d[71] } #69~ 펫
                    product = {
                        "idx":d[1],
                        "partner_id": d[6],
                        "is_no_show": d[29],
                        "receipt_type": d[20],    # 접수방법(1-android,2-iOS,3-매장(POS)0-선택없음)
                        "pay_type": d[21],        # 결제방법(1-PG, 2-계좌이체, 0-선택없음)
                        "pay_status": d[22],    # 결제상태(1-진행중, 2-입금대기, 3-결제완료, 8-보류, 9-실패)
                        "payment" : {"point":d[16], "card":d[17], "cash":d[18], },
                        "date": {"regist" : str(d[34]) # self.datetimeToStr(d[34], d_format)
                                , "check_in": check_in
                                , "check_out": check_out},
                        "memo": d[31]
                    }
                    tmp["customer"] = customer
                    tmp["pet"] = pet
                    tmp["product"] = product
                    body["kindergarden"].append(tmp)
            ret = self.message.successOk()

            ret["body"] = body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[0])))