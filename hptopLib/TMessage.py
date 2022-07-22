# -*- coding: utf-8 -*-


class TMessage:
    def successOk(self):
        return {"head": {"code": 200, "message": "정상"}}

    def loginFail(self):
        return {"head": {"code": 401, "message": "아이디/비밀번호를 확인 해주세요."}}

    def loginIdFail(self):
        return {"head": {"code": 402, "message": "사용할 수 없는 아이디 입니다."}}

    def loginAuthFail(self):
        return {"head": {"code": 403, "message": "등록된 사용자가 아닙니다."}}

    def error(self, message):
        return {"head": {"code": 999, "message": message}}

    def errorServer(self):
        return {"head": {"code": 500, "message": "서버 오류"}}

    def errorBadRequst(self):
        return {"head": {"code": 400, "message": "인자 오류"}}

    def errorDBSelect(self):
        return {"head": {"code": 903, "message": "데이타 가져오기 오류"}}

    def errorDBInsert(self):
        return {"head": {"code": 904, "message": "데이타 추가 오류"}}

    def errorDBUpdate(self):
        return {"head": {"code": 905, "message": "데이타 수정 오류"}}

    def errorDBDelete(self):
        return {"head": {"code": 906, "message": "데이타 삭제 오류"}}

    def errorDBQuery(self):
        return {"head": {"code": 907, "message": "데이타 쿼리 오류"}}
