# -*- coding: utf-8 -*-


def totalPrice(src):
    price = 0
    div = src.split("|")
    for d in div:
        if ":" in d:
            tmp = d.split(":")
            price += int(tmp[1])
    if len(div[9]) > 0:
        price += int(div[9])
    if len(div[10]) > 0:
        price += int(div[10])
    if len(div[11]) > 0:
        price += int(div[11])
    return price