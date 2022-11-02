# -*- coding: utf-8 -*-
from curses.ascii import isdigit
from datetime import datetime
import time


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
    if is_zero == '' or is_zero is None:
        return False
    return False if int(is_zero) == 0 else True


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
    tmpStr = ""
    for i in range(count):
        if i > 0:
            tmpStr += ","
        tmpStr += list[st+i+1]
    body = setArr(tmpStr)
    #return len(body), body
    return count, body

def judgeStrOrInt(value):
    return isdigit(value);


def strToHex(str):
    return str.encode('UTF-8').hex()

def hexToStr(hex):
    return bytes.fromhex(hex).decode('utf-8')


def nowdateFormat(format):
    """
    현재 날짜 포멧화.
    :param str format: 포멧 규격 ex) %Y-%m-%d %H:%M:%S"
    :return str : 포멧된 날짜
    :raise error: 
   """
    now = datetime.now()
    return now.strftime(format)

def nowToMicroSecond():
    dt = datetime.now()
    return dt.microsecond

def nowToMilliSecond(name, origin):
    milles = int(round(time.time() * 1000))
    print("duration(%s): %f" % (name,(milles - origin) / 1000))
    origin = milles
    return milles
