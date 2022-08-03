# -*- coding: utf-8 -*-


def main():
    #product = "오리|개|반짝펫살롱|중형견미용|부분미용|6:25000|기본얼굴컷:1000|4:4000|이중모_목욕:10000|5000|||" \
    #          "||0|1|스파2:9000|0|1|기장추가3:15000|1|23:쿠폰임:10000|8|1993:놀이구:200:2|1988:상품2:900:2|1997:오리고기:700:2|1994:닭고기:800:2|2004:사료1:300:2|2003:사료2:400:2|2010:털엉킴1:100:2|2009:입질1:1000:2|"
    product = "단비|개|반자주 장산점|||on|||||||||0|0|0|0|0|0|"
    p_split = product.split("|")
    if p_split[1].strip() == "개":
        return typeDog(product)
    else:
        return typeCat(product)


def typeDog(product):
    try:
        p_split = product.split("|")
        products = {
            "name": p_split[0],
            "animal": p_split[1],
            "shop": p_split[2],
            "base": {
                "size": p_split[3],
                "beauty_kind": p_split[4],
                "weight": {
                    "unit": subSplit(p_split[5], ":")[0],
                    "price": subSplit(p_split[5], ":")[1]
                },
                "hair_features": setArr(p_split[8]),
                "hair_lenth": {
                    "unit": subSplit(p_split[7], ":")[0],
                    "price": subSplit(p_split[7], ":")[1]
                }
            },
            "add": {
                "face": {
                    "unit": subSplit(p_split[6], ":")[0],
                    "price": subSplit(p_split[6], ":")[1]
                },
                "leg": {
                    "nail": p_split[9],
                    "rain_boots": p_split[10],
                    "bell": p_split[11]
                }
            }
        }
        pos = 15
        if len(p_split) > pos and p_split[pos].strip() != "" and int(p_split[pos]) > 0:  # 스파 개수
            count, body = setOffSet(pos, int(p_split[pos]), p_split)
            products["add"]["spa"] = body
            pos += count
        pos += 1
        if len(p_split) > pos and p_split[pos].strip() != "" and int(p_split[pos]) > 0:  # 염색 개수
            count, body = setOffSet(pos, int(p_split[pos]), p_split)
            products["add"]["hair_color"] = body
            pos += count
        pos += 1
        if len(p_split) > pos and p_split[pos].strip() != "" and int(p_split[pos]) > 0:  # 기타
            count, body = setOffSet(pos, int(p_split[pos]), p_split)
            products["add"]["etc"] = body
            pos += count
        pos += 1
        if len(p_split) > pos and p_split[pos].strip() != "" and int(p_split[pos]) > 0:  # 쿠폰상품
            count, body = setOffSet(pos, int(p_split[pos]), p_split)
            products["coupon"] = body
            pos += count
        pos += 1

        if len(p_split) > pos and p_split[pos].strip() != "" and int(p_split[pos]) > 0:  # 제품
            count, body = setOffSet(pos, int(p_split[pos]), p_split)
            products["goods"] = body
            pos += count

        return products
    except Exception as e:
        print(e.args[0])

def typeCat(product):
    try:
        p_split = product.split("|")
        products = {
            "name": p_split[0],
            "animal": p_split[1],
            "shop": p_split[2],
            "category": p_split[3],
            "base": {
                "weight": {
                    "unit": subSplit(p_split[4], ":")[0],
                    "price": subSplit(p_split[4], ":")[1]
                },
                "hair_beauty":p_split[5],
                "bath_shot": p_split[7],
                "bath_long": p_split[8]
            },
            "add": {
                "nail": p_split[6]
                }
        }
        pos = 9
        if len(p_split) > pos and p_split[pos].strip() != "" and int(p_split[pos]) > 0:  # 기타
            count, body = setOffSet(pos, int(p_split[pos]), p_split)
            products["add"]["etc"] = body
            pos += count
        pos += 1
        if len(p_split) > pos and p_split[pos].strip() != "" and int(p_split[pos]) > 0:  # 쿠폰상품
            count, body = setOffSet(pos, int(p_split[pos]), p_split)
            products["coupon"] = body
            pos += count
        pos += 1
        if len(p_split) > pos and p_split[pos].strip() != "" and int(p_split[pos]) > 0:  # 제품
            count, body = setOffSet(pos, int(p_split[pos]), p_split)
            products["goods"] = body
            pos += count

        return products
    except Exception as e:
        print(e.args[0])


def subSplit(str, sep):
    if str == "" or str == "on":
        return ["0","0"]
    else:
        return str.split(sep)

def setArr(str):
    product = str.split(",")
    body = []
    for p in product:
        tmp={}
        sub = p.split(":")
        if len(sub) == 2:
            tmp = {"unit":sub[0], "price":sub[1]}
        elif len(sub) == 3:
            tmp = {"idx": sub[0], "name": sub[1], "price": sub[2]}
        elif len(sub) == 4:
            tmp = {"idx":sub[0], "name":sub[1], "ea":sub[3], "price":sub[2]}
        body.append(tmp)
    return body

def setOffSet(st, count, list):
    i = 1
    tmpStr = ""
    for i in range(count):
        if i > 0:
            tmpStr += ","
        tmpStr += list[st+i+1]
    body = setArr(tmpStr)
    return len(body), body


if __name__ == '__main__':
    print(main())