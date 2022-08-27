
# -*- coding: utf-8 -*-
import traceback

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_ETC_SALES_PERFORMANCE
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase


class TPerformance(TAPIBookingIDBase):
    def getInfo(self, partner_id, *args):
        try:
            body = {}
            value, rows, columns = self.db.resultDBQuery(PROC_ETC_SALES_PERFORMANCE % (partner_id,
                                                                            args[0]["st_date"], args[0]["fi_date"],
                                                                            args[0]["order_type"], args[0]["where_type"]),QUERY_DB)

            if value is not None:
                data = []
                if rows < 2:
                    data.append(value)
                else:
                    data = value
                body["data"] = self.queryDataToDic(value, rows, columns)
                person = set()
                animal = set()
                for d in data:
                    person.add(d[16])
                    animal.add(d[15])
                body["customer_number"] = len(person)
                body["animal_number"] = len(animal)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        pass