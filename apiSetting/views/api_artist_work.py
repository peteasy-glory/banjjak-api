# -*- coding: utf-8 -*-

from apiShare.constVar import QUERY_DB
from apiShare.funcLib import zeroToBool
from apiShare.sqlQuery import *
from hptopLib.TAPIIDBase import TAPIIDBase


class TArtistWork(TAPIIDBase):
    """
    미용사 근무 정보.
    """

    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_ARTIST_WORKING_GET % (partner_id), QUERY_DB)
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
                    tmp["is_leave"] = True if int(d[5]) == 1 else False # zeroToBool(d[5])
                    tmp["is_show"] = True if int(d[6]) == 2 else False
                    sub = d[7].split(',')
                    for s in sub:
                        resub = s.split('|')
                        artist.append({"idx": resub[0], "week": resub[1], "time_st": resub[2], "time_fi": resub[3]})
                    tmp["work"] = artist
                    body.append(tmp)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[0] == 'POST':
                value, rows, columns = self.db.resultDBQuery(PROC_SETTING_BREAK_TIME_MODIFY % (args[1]["partner_id"]
                                                            , args[1]["break_time"]),QUERY_DB)
            elif args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_SETTING_BREAK_TIME_MODIFY % (args[1]["partner_id"]
                                                                                               , args[1]["break_time"]),QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None

