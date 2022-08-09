# -*- coding: utf-8 -*-
from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase


class TAuthSetting(TAPIBase):
    """
    미용사 권한 부여.(기타 다른 customer_id에 해당 샵으로 접속할 수 있는 권한)
    """

    def get(self, request):
        try:
            dic = request.data
            if dic['artist_id'] is None or dic["customer_id"] is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))

            artist_id = dic["artist_id"].strip()
            customer_id = dic["customer_id"].strip()
            data, rows, columns = self.db.resultDBQuery(PROC_IS_EXIST_AUTHORITY_GET % (artist_id,customer_id), QUERY_DB)
            ret = self.message.successOk()
            body = {}
            if data is None or data[0] > 0:
                if data[0] == 3:
                    body["exist"] = True
                    body["message"] = "이미 권한이 부여된 회원입니다."
                elif data[0] == 2:
                    body["exist"] = True
                    body["message"] = "이미 샵을 운영하는 회원입니다."
                elif data[0] == 1:
                    body["exist"] = True
                    body["message"] = "가입하지 않는 회원입니다."
                else:
                    return HttpResponse(self.json.dicToJson(self.message.errorNonePostData()))
            else:
                body["exist"] = False
                body["message"] = "사용 가능한 아이디입니다"
            ret["body"] = body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))

    def put(self, request):
        try:
            dic = request.data

            if dic["artist_id"] is None or dic["customer_id"] is None or dic["name"] is None or dic["del"] is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))

            artist_id = dic["artist_id"].strip()
            customer_id = dic["customer_id"].strip()
            name = dic["name"].strip()
            data, rows, columns = self.db.resultDBQuery(PROC_SETTING_AUTHORITY_PUT % (artist_id, customer_id, name, dic["del"]),QUERY_DB)
            ret = self.message.successOk()
            if data is None:
                return HttpResponse(self.json.dicToJson(self.message.errorDBInsert()))
            if data[0] < 0:
                return HttpResponse(self.json.dicToJson(self.message.errorDBUpdate()))

            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))

    def delete(self, request):
        try:
            pass
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))


