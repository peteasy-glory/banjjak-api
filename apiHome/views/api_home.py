# -*- coding: utf-8 -*-

from django.http import HttpResponse
from apiShare.constVar import QUERY_DB
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
            if request.GET.get('phone') is not None:
                value, rows, columns = self.db.resultDBQuery(PROC_CELLPHONE_SEARCH_GET % (partner_id.strip(), request.GET.get('phone')), QUERY_DB)
            else:
                return HttpResponse(self.json.dicToJson(self.message.searchPhoneFail()))
            ret = self.message.successOk()
            body = self.queryDataToDic(value, rows, columns)
            data = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            if value is not None:

                for d in data:
                    value1, rows1, columns1 = self.db.resultDBQuery(
                        PROC_NO_SHOW_COUNT_GET % (partner_id.strip(), d[1]), QUERY_DB)

                ret["body"] = body
                return HttpResponse(self.json.dicToJson(ret))
            body = self.queryDataToDic(data, rows, columns)
            ret["body"] = body
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
                    body.append(tmp)
            ret["body"] = body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[0])))