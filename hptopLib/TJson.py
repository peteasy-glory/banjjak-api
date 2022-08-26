# -*- coding: utf-8 -*-

import json
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.utils.encoders import JSONEncoder


class TJson:
    def dicToJson(self, data):
        if data is None:
            return None
        #return json.dumps(data, cls=DjangoJSONEncoder)
        return json.dumps(data, cls=JSONEncoder)
