# -*- coding: utf-8 -*-

from django.http import HttpResponse
from hptopLib.TAPIBase import TAPIBase


class TSearch(TAPIBase):
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

