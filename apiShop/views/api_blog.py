# -*- coding: utf-8 -*-
import json
import traceback
import requests

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SHOP_BLOG_GET
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase


class TBlog(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        try:
            body = {}
            if not args[0]["naver"]:
                value, rows, columns = self.db.resultDBQuery(PROC_SHOP_BLOG_GET % (partner_id,),QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
            else:
                body = self.getNaverBlog(clientID="UJ2SBwYTjhQSTvsZF8TO", clientSecret="3gFya4za76", query=args[0]["query"]
                                         , display=args[0]["display"], start=args[0]["start"])
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        try:
            value = None
            row = None
            columns = None
            if args[0] == 'POST':
                value, rows, columns = self.db.resultDBQuery(PROC_SHOP_BLOG_POST % (args[1]["idx"], args[1]["reply"]), QUERY_DB)
            elif args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_SHOP_BLOG_PUT % (args[1]["idx"], args[1]["reply"]), QUERY_DB)
            elif args[0] == 'DELETE':
                value, rows, columns = self.db.resultDBQuery(PROC_SHOP_BLOG_DELETE % (args[1]["idx"],), QUERY_DB)
            else:
                return -1, "undefined method", {}
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as e:
            return -1, traceback.format_exc(), None


    def getNaverBlog(self, clientID, clientSecret, query, display, start):
        url = "https://openapi.naver.com/v1/search/blog.json?query=%s&display=%d&start=%d" % (query, display, start)
        header = {
            "X-Naver-Client-Id": clientID,
            "X-naver-Client-secret": clientSecret
        }

        r = requests.get(url, headers=header)
        return json.loads(r.text)