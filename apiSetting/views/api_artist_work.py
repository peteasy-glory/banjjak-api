# -*- coding: utf-8 -*-
from inspect import getframeinfo, currentframe

from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.funcLib import zeroToBool
from apiShare.sqlQuery import *
from hptopLib.TAPISettingBase import TAPISettingBase


class TArtistWork(TAPISettingBase):
    """
    미용사 근무 정보.
    """

    def __init__(self):
        pass

    def __del__(self):
        pass

    def getInfo(self, partner_id):
        try:
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
                    tmp["is_host"] = zeroToBool(d[4])
                    tmp["is_leave"] = zeroToBool(d[5])
                    tmp["is_show"] = True if d[6] == 2 else False
                    sub = d[7].split(',')
                    for s in sub:
                        resub = s.split('|')
                        artist.append({"idx": resub[0], "week": resub[1], "time_st": resub[2], "time_fi": resub[3]})
                    tmp["work"] = artist
                    body.append(tmp)
            return 0, "success", body
        except Exception as e:
            frame_info = getframeinfo(currentframe())
            msg = "[PATH: %s, LINE: %s, FUNC: %s, ERR: %s" % (
                    frame_info.filename, frame_info.lineno, frame_info.function, e.args[0])
            return -1, msg, None

    def post(self, request):
        try:
            pass
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))

    def put(self, request):
        try:
            pass
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))
