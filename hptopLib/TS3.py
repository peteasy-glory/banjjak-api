# -*- coding: utf-8 -*-
import traceback

import boto3
import base64


class TS3:
    def __init__(self):
        self.s3 = boto3.resource('s3', aws_access_key_id="AKIATLSPGL6BNM6VOYWX",
                             aws_secret_access_key="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")

    def __del__(self):
        self.s3 = None

    def frontUpload(self, partner_id, file_name, origin_file):
        try:
            self.s3.Object("banjjak-s3", "upload/"+partner_id+"/"+file_name).put(Body=base64.b64decode(origin_file))
            return 0, "/upload/"+partner_id+"/"+file_name
        except Exception as e:
            return -1, traceback.format_exc()
