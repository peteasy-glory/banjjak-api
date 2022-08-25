# -*- coding: utf-8 -*-

from django.http import HttpResponse
from apiShare.constVar import QUERY_DB
from apiShare.funcLib import zeroToBool
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase


class THome(TAPIBase):
    """

    홈 메인
    - 성공시
       : 메인 화면에 보여줄 정보를 전송

    - 실패시
       : 실패 코드 및 메세지만 전송
    """
    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            if request.GET.get('y') is not None and request.GET.get('m') is not None:
                err, body = self.getBodyHomePeriodStatus(partner_id, request.GET.get('y'), request.GET.get('m'))
            else:
                err, body = self.getBodyHome(partner_id)
            if err < 0:
                return HttpResponse(self.json.dicToJson(self.message.errorDBSelect()))
            ret = self.message.successOk()
            ret["body"] = body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[0])))


class TCellSearch(TAPIBase):
    """

     홈 전화번호 조회
     - 성공시
        : 조회된 회원및 가족 구성원 연락처 전송

     - 실패시
        : 실패 코드 및 메세지만 전송
     """

    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            if request.GET.get('phone') is not None and request.GET.get('name') is not None:
                return HttpResponse(self.json.dicToJson(self.message.multiplSsearchFail()))
            if request.GET.get('phone') is not None:
                value, rows, columns = self.db.resultDBQuery(PROC_SEARCH_PHONE_GET % (partner_id.strip(), request.GET.get('phone')), QUERY_DB)
            elif request.GET.get('name') is not None:
                value, rows, columns = self.db.resultDBQuery(PROC_SEARCH_PET_NAME_GET % (partner_id.strip(), request.GET.get('name')), QUERY_DB)
            else:
                return HttpResponse(self.json.dicToJson(self.message.searchFail()))
            ret = self.message.successOk()
            ret["body"] = self.queryDataToDic(value, rows, columns)
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[0])))

class TConsulting(TAPIBase):
    """

     홈 이용 상담 관리 조회
     - 성공시
        : 이용 상담 조회

     - 실패시
        : 실패 코드 및 메세지만 전송
     """

    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            value, rows, columns = self.db.resultDBQuery(PROC_CONSULT_MGR_GET % (partner_id.strip()), QUERY_DB)
            ret = self.message.successOk()
            body = []
            if value is None:
                ret["body"] = body
                return HttpResponse(self.json.dicToJson(ret))
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
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

                    tmp["birth"] = d[9]
                    tmp["gender"] = d[10]
                    tmp["neutral"] = zeroToBool(d[11])
                    tmp["weight"] = d[12]
                    tmp["photo"] = d[13]
                    tmp["beauty_exp"] = d[14]
                    tmp["vaccination"] = d[15]
                    tmp["bite"] = zeroToBool(d[16])
                    tmp["heart_trouble"] = zeroToBool(d[17])
                    tmp["marking"] = zeroToBool(d[18])
                    tmp["mounting"] = zeroToBool(d[19])
                    tmp["luxation"] = d[20]
                    tmp["dermatosis"] = zeroToBool(d[21])
                    tmp["photocounseling"] = d[22]
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
                    body.append(tmp)
            ret["body"] = body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[0])))

class TConsultBookingWaiting(TAPIBase):
    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            value, rows, columns = self.db.resultDBQuery(PROC_CONSULT_BOOKING_WAITING_COUNT_GET % (partner_id.strip()), QUERY_DB)
            ret = self.message.successOk()
            ret["body"] = self.queryDataToDic(value, rows, columns)
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[0])))

class TNavigation(TAPIBase):
    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            value, rows, columns = self.db.resultDBQuery(PROC_NAVIGATION_INFO_GET % (partner_id.strip()), QUERY_DB)
            ret = self.message.successOk()
            ret["body"] = self.queryDataToDic(value, rows, columns)
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[0])))










