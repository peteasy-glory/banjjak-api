# -*- coding: utf-8 -*-
import os.path

import boto3
import base64
import pymysql
import urllib.request

#S3 CloudFront
from hptopLib.TDB import TDB

EXTERNAL_S3_DOMAIN = "https://image.banjjakpet.com/customer"
s3r = boto3.resource('s3', aws_access_key_id="AKIATLSPGL6BNM6VOYWX",
                     aws_secret_access_key="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")
bucket = s3r.Bucket('bucket_name')


# db = pymysql.connect(
#     user='gobeautypet',
#     passwd='pebjjdb!0901$',
#     host='175.126.123.165',
#     db='gobeautypet',
#     charset='utf8'
# )


def prefix_exits(path):
    s3_client = boto3.client('s3')
    res = s3_client.list_objects_v2(Bucket="banjjak-s3", Prefix=path, MaxKeys=1)
    return 'Contents' in res

def download(url, file, s3Path):
    urllib.request.urlretrieve(url, file)
    upload(file, s3Path)

def upload(file, fname):
    try:
        # s3r = boto3.resource('s3', aws_access_key_id="AKIATLSPGL6BNM6VOYWX",
        #                      aws_secret_access_key="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")
        s3r.Object("banjjak-s3", fname).put(Body=base64.b64decode(file))
    except Exception as e:
        print(e)

def dbConn():
    return pymysql.connect(
        user='gobeautypet',
        passwd='pebjjdb!0901$',
        host='175.126.123.165',
        db='gobeautypet',
        charset='utf8'
    )

def resultDBQuery(qryStr, db='default'):
    qry = TDB()
    return qry.resultDBQuery(qryStr, database=db)
#대문사진, 리뷰

# qry = SELECT * FROM tb_mypet_beauty_photo WHERE prnt_yn = 'Y'
#SELECT * FROM tb_shop_frontimage
#SELECT * FROM tb_product WHERE enable_flag = 1
#SELECT * FROM tb_license WHERE enable_flag = 1
#SELECT * FROM tb_file WHERE is_delete = 1
def getData(index, qry, num):
    db = dbConn()
    cursor = db.cursor()
    cursor.execute(qry)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    dic = {}
    i = 0
    j = 0
    try:
        for r in result:
            j += 1
            if not r[num] is None and r[num] != "":
                arr = r[num].split("|")
                for s in arr:
                    path = s.replace("/pet/upload/", "upload/")
                    path = path.replace("/upload/", "upload/")
                    chk = prefix_exits(path)
                    if not chk:
                        i += 1
                        dic[i] = path
                        try:
                            download("https://gopet.kr/pet/"+path, 'down/'+os.path.basename(path), path)
                        except Exception as e:
                            print(e)
                            print(path)
            if j % 100 == 0:
                print(j)
        print("===== {0} - Query =====".format(index))
        for d in dic:
           print(str(d) + " : " + dic[d])
    except Exception as e:
        print(e)



if __name__ == '__main__':
    getData(1, "SELECT * FROM tb_usage_reviews WHERE is_delete = 0 AND is_blind = 0 and reg_time > '2022-03-01' ORDER BY review_seq DESC;", 7)
    getData(2, "SELECT * FROM tb_mypet_beauty_photo WHERE prnt_yn = 'Y' and upload_dt > '2022-03-01'", 8)
    getData(3, "SELECT * FROM tb_shop_frontimage", 1)
    getData(4, "SELECT * FROM tb_portfolio WHERE enable_flag = 1 AND update_time > '2022-03-01'", 1)
    getData(5, "SELECT * FROM tb_license WHERE enable_flag = 1   AND update_time > '2022-03-01'", 1)
    getData(6, "SELECT * FROM tb_file WHERE is_delete = 1 AND reg_dt > '2022-03-01'", 3)


    # chk = prefix_exits("upload/pettester@peteasy.kr/artist_front_image_20200619150258.jpg")
    # if not chk:
    #     print('false')

