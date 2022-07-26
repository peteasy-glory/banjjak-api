# -*- coding: utf-8 -*-

import json
from django.core.serializers.json import DjangoJSONEncoder

class TJson:
    def dicToJson(self, data):
        if data is None:
            return None
        return json.dumps(data, cls=DjangoJSONEncoder)