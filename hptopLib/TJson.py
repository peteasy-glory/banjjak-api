# -*- coding: utf-8 -*-

import json

class TJson:
    def dicToJson(self, data):
        if data is None:
            return None
        return json.dumps(data)