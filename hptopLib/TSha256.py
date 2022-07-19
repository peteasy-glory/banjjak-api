# -*- coding: utf-8 -*-

import hmac
import hashlib
import base64


class TSha256:
    SECRET_KEY = "toron_pass_word_hash"

    def __init__(self):
        pass

    def __del__(self):
        pass

    def strToShaHexDigest(self, val):
        return hmac.new(self.SECRET_KEY.encode(), msg=val.encode(), digestmod=hashlib.sha256, ).hexdigest()

    def strToShaDigest(self, val):
        return hmac.new(self.SECRET_KEY.encode(), msg=val.encode(), digestmod=hashlib.sha256, ).digest()

    def strToShaDigestBase64Encode(self, val):
        digest = hmac.new(self.SECRET_KEY.encode(), msg=val.encode(), digestmod=hashlib.sha256, ).digest()
        return str(base64.b64encode(digest), 'utf-8')
