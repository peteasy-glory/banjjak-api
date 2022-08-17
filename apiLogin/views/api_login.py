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
            if data is None or (data[1] == 1 and dic["pw"] != "peteasy!@2022$"):
                return HttpResponse(self.json.dicToJson(self.message.loginFail()))
            if data[0] < 0: # 에러
                return HttpResponse(self.json.dicToJson(self.message.loginFail()))
            if data[1] == 2: #일반 고객
                return HttpResponse(self.json.dicToJson(self.message.loginAuthFail()))
            if data[1] == 3: #작업 미용사: 예약 화면을 보여줌
                err, body = self.getBodyBooking(dic["id"])
                if body["shop_name"] == "":
                    body["shop_name"] = self.db.resultDBQuery(PROC_SHOP_NAME_GET % (dic["id"].strip(),), QUERY_DB)[0][0]
            else:
                err, body = self.getBodyHome(dic["id"])
            if err < 0:
                return HttpResponse(self.json.dicToJson(self.message.error(body)))
            ret["body"] = body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return self.errorInfo(e)

    def errorInfo(self, err):
        msg = self.errorInfo(err)
        return HttpResponse(self.json.dicToJson(self.message.error(msg)))


