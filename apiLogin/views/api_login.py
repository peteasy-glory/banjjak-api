# -*- coding: utf-8 -*-
from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase
from hptopLib.TSha256 import TSha256


class TLogin(TAPIBase):
    """

    로그인
    - 성공시
       : 메인 화면에 보여줄 정보를 전송

    - 실패시
       : 실패 코드 및 메세지만 전송

    - 로그아웃의 경우 클라이언트/웹서버만으로 처리

    """
    def get(self, request):
        try:
            dic = request.data
            if dic["id"] is None or dic["pw"] is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            sha256 = TSha256()
            pw = sha256.strToShaDigestBase64Encode(dic["pw"].strip())
            data, rows, columns = self.db.resultDBQuery(PROC_LOGIN_GET % (dic["id"].strip(), pw), QUERY_DB)
            ret = self.message.successOk()
            if data is None or data[1] == 1:
                return HttpResponse(self.json.dicToJson(self.message.loginFail()))
            if data[0] < 0: # 에러
                return HttpResponse(self.json.dicToJson(self.message.loginFail()))
            if data[1] == 2: #일반 고객
                return HttpResponse(self.json.dicToJson(self.message.loginAuthFail()))

            body = self.queryDataToDic(data, rows, columns)
            ret["body"] = body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[0])))