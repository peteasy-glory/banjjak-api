# -*- coding: utf-8 -*-


def totalPrice(src):
    price = 0
    div = src.split("|")
    for d in div:
        if ":" in d:
            if d.count(":") == 3:
                tmp = d.split(":")
                price += (int(tmp[2]) * int(tmp[3]))
            else:
                tmp = d.split(":")
                price += int(tmp[1])
    if len(div) > 10 and len(div[9]) > 0:
        price += int(div[9])
    if len(div) > 10 and len(div[10]) > 0:
        price += int(div[10])
    if len(div) > 11 and len(div[11]) > 0:
        price += int(div[11])
    return price




def zeroToBool(is_zero):
    return False if is_zero == 0 else True


def productToDic(product):
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
        if int(p_split[pos]) > 0:  # 스파 개수
            count, body = setOffSet(pos, int(p_split[pos]), p_split)
            products["add"]["spa"] = body
            pos += count
        pos += 1
        if int(p_split[pos]) > 0:  # 염색 개수
            count, body = setOffSet(pos, int(p_split[pos]), p_split)
            products["add"]["hair_color"] = body
            pos += count
        pos += 1
        if int(p_split[pos]) > 0:  # 기타
            count, body = setOffSet(pos, int(p_split[pos]), p_split)
            products["add"]["etc"] = body
            pos += count
        pos += 1
        if int(p_split[pos]) > 0:  # 쿠폰상품
            count, body = setOffSet(pos, int(p_split[pos]), p_split)
            products["coupon"] = body
            pos += count
        pos += 1
        if int(p_split[pos]) > 0:  # 제품
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
                "hair":p_split[5],
                "bath": setArr(p_split[7])
            },
            "add": {
                "nail": p_split[6]
                }
        }
        pos = 8
        if int(p_split[pos]) > 0:  # 기타
            count, body = setOffSet(pos, int(p_split[pos]), p_split)
            products["add"]["etc"] = body
            pos += count
        pos += 1
        if int(p_split[pos]) > 0:  # 쿠폰상품
            count, body = setOffSet(pos, int(p_split[pos]), p_split)
            products["coupon"] = body
            pos += count
        pos += 1
        if int(p_split[pos]) > 0:  # 제품
            count, body = setOffSet(pos, int(p_split[pos]), p_split)
            products["goods"] = body
            pos += count

        return products
    except Exception as e:
        print(e.args[0])


def subSplit(str, sep):
    if str == "":
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