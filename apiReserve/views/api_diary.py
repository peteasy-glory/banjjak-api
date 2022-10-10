# -*- coding: utf-8 -*-
import traceback

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_RESERVE_DIARY_GET, PROC_RESERVE_DIARY_POST, PROC_RESERVE_DIARY_HISTORY_GET, PROC_RESERVE_DIARY_LIST_GET, PROC_RESERVE_DIARY_LIST_SELECT_GET
from hptopLib.TAPIBookingBase import TAPIBookingBase
from hptopLib.TAPIBooking import TAPIBooking

class TDiary(TAPIBookingBase):

    def getInfo(self, payment_idx, *args):
        try:
            body = []
            value, rows, columns = self.db.resultDBQuery(PROC_RESERVE_DIARY_GET % (payment_idx,),QUERY_DB)

            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
                # if rows < 2:
                #     data.append(value)
                # else:
                #     data = value
                # body.append(data)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        try:
            value = None
            row = None
            columns = None
            if args[1] == 'POST':
                value, rows, columns = self.db.resultDBQuery(
                    PROC_RESERVE_DIARY_POST % (
                        args[0]["payment_log_seq"],
                        args[0]["artist_id"],
                        args[0]["pet_seq"],
                        args[0]["cellphone"],
                        args[0]["etiquette_1"],
                        args[0]["etiquette_2"],
                        args[0]["etiquette_3"],
                        args[0]["etiquette_etc"],
                        args[0]["etiquette_etc_memo"],
                        args[0]["condition_1"],
                        args[0]["condition_2"],
                        args[0]["condition_3"],
                        args[0]["condition_etc"],
                        args[0]["condition_etc_memo"],
                        args[0]["tangles_1"],
                        args[0]["tangles_2"],
                        args[0]["tangles_3"],
                        args[0]["tangles_4"],
                        args[0]["tangles_5"],
                        args[0]["tangles_6"],
                        args[0]["tangles_7"],
                        args[0]["tangles_etc"],
                        args[0]["tangles_etc_memo"],
                        args[0]["part_1"],
                        args[0]["part_2"],
                        args[0]["part_3"],
                        args[0]["part_4"],
                        args[0]["part_5"],
                        args[0]["part_6"],
                        args[0]["part_etc"],
                        args[0]["part_etc_memo"],
                        args[0]["skin_1"],
                        args[0]["skin_2"],
                        args[0]["skin_3"],
                        args[0]["skin_4"],
                        args[0]["skin_5"],
                        args[0]["skin_6"],
                        args[0]["skin_7"],
                        args[0]["skin_etc"],
                        args[0]["skin_etc_memo"],
                        args[0]["bath_1"],
                        args[0]["bath_2"],
                        args[0]["bath_3"],
                        args[0]["bath_etc"],
                        args[0]["bath_etc_memo"],
                        args[0]["notice_1"],
                        args[0]["notice_2"],
                        args[0]["notice_3"],
                        args[0]["notice_4"],
                        args[0]["notice_etc"],
                        args[0]["notice_etc_memo"],
                        args[0]["file_path"]
                    ), QUERY_DB)
            else:
                return -1, "undefined method", {}
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as e:
            return -1, traceback.format_exc(), None

class TDiaryHistory(TAPIBooking):

    def getInfo(self, *args):
        try:
            print(args[0])
            body = []
            value, rows, columns = self.db.resultDBQuery(PROC_RESERVE_DIARY_HISTORY_GET % (args[0]['artist_id'],args[0]['cellphone'],args[0]['pet_seq']),QUERY_DB)

            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
                # if rows < 2:
                #     data.append(value)
                # else:
                #     data = value
                # body.append(data)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

class TDiaryList(TAPIBooking):

    def getInfo(self, *args):
        try:
            print(args[0])
            body = []
            value, rows, columns = self.db.resultDBQuery(PROC_RESERVE_DIARY_LIST_GET % (args[0]['artist_id'],args[0]['cellphone']),QUERY_DB)

            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
                # if rows < 2:
                #     data.append(value)
                # else:
                #     data = value
                # body.append(data)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

class TDiaryListSelect(TAPIBooking):

    def getInfo(self, *args):
        try:
            print(args[0])
            body = []
            value, rows, columns = self.db.resultDBQuery(PROC_RESERVE_DIARY_LIST_SELECT_GET % (args[0]['artist_id'],args[0]['cellphone'],args[0]['date']),QUERY_DB)

            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
                # if rows < 2:
                #     data.append(value)
                # else:
                #     data = value
                # body.append(data)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None