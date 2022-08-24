# -*- coding: utf-8 -*-

import os
import base64
from PIL import Image
import io

class TImage:
    def base64ToImage(self, base64Str, saveFile):
        try:
            ext = self.splitFile(saveFile)[1][1].replace(".", "").lower()
            if os.path.isfile(saveFile):
                os.remove(saveFile)
            if not os.path.isdir(os.path.dirname(saveFile)):
                os.makedirs(os.path.dirname(saveFile))
            imgdata = base64.b64decode(base64Str)
            dataBytesIO = io.BytesIO(imgdata)
            image = Image.open(dataBytesIO)
            if ext == 'jpg':
                image.save(saveFile, 'jpeg')
            else:
                image.save(saveFile, ext)
        except Exception as e:
            print(e)

    def imageToBase64(self, readFile):
        with open(readFile, "rb") as img_file:
            return base64.b64encode(img_file.read())

    def splitFile(self, filePath):
        file = os.path.basename(filePath)
        return os.path.dirname(filePath), os.path.splitext(file)

    def mkDir(self, filePath):
        os.makedirs(filePath)
