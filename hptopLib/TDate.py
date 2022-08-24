# -*- coding: utf-8 -*-

from datetime import datetime

class TDate:
    def currentDateTime(self):
        curr = datetime.now()
        return {"YYYY": curr.strftime("%Y"), "MM": curr.strftime("%m") \
            , "DD": curr.strftime("%d"), "hh": curr.strftime("%H") \
            , "mm": curr.strftime("%M"), "ss": curr.strftime("%S")}

    def customDateTime(self, format_date="%Y%m%d%H%M%S%f"):
        return datetime.now().strftime(format_date)

    @staticmethod
    def now():
        return datetime.now()