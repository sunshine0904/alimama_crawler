#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Em on 2018/1/9

import requests
from config import *

SERVER_HOST = 'https://pub.alimama.com/'
LOCAL_HOST = 'https://pub.alimama.com/'


# 爬取地址
API_CRAWLER_ADDRESS = '/api/import/xxxxx'
# 分类
API_CATEGORY = '/api/import/xxxxx'
# 店铺
API_STORE = '/api/import/xxxxx'
# 商品
API_PRODUCT = 'myunion.htm?spm=a219t.7900221/21.1998910419.d7c45d32enzjh.21be75a5tLIcgI#!/promo/self/shop_detail?userNumberId='
# 商品描述
API_PRODUCT_DESC = '/api/import/xxxxx'
# 链接/淘口令
API_LINK = '/api/import/xxxxx'


def get_host():
    if get_debug():
        return LOCAL_HOST
    else:
        return SERVER_HOST

# def get_host():
#     return LOCAL_HOST


# 爬取地址
def get_crawler_address():
    result = {
        'data': {
            'start_page': 1,
            'end_page': 100,
            'product_url': "https://pub.alimama.com/items/channel/nzjh.json?channel=nzjh&toPage=1&dpyhq=1&perPageSize=50&shopTag=dpyhq&startTkRate=3&startPrice=0&endPrice=59&t=1542007653922&_tb_token_=ee57e495b0a37&pvid=21_42.120.75.54_4398_1542007639653",
            'category': 'nzjh',
            'coupon_url': 'https://pub.alimama.com/common/code/getAuctionCode.json?auctionid=&adzoneid=191266467&siteid=41858721&scenes=1&channel=tk_9k9&t=1516170554149&_tb_token_=533ee7559e61b&pvid=16_59.173.203.230_5582_1516170526631'
        }
    }
    return result


# 获取所有的分类
def get_all_category():
    return requests.get(get_host() + API_CATEGORY).json()


# 获取所有的店铺
def get_all_store():
    return requests.get(get_host() + API_STORE).json()


def create_store(params):
    r = requests.post(get_host() + API_STORE, params)
    print(u'创建店铺成功 ==> ') + params['name']
    return r.json()


def create_product(params):
    r = requests.post(get_host() + API_PRODUCT, params)
    print(u'======================= 创建商品 ======================= ')
    print(u'Name ==> ') + str(params['name'])
    print(u'tpid ==> ') + str(params['tpid'])
    print(u'tags ==> ') + str(params['tags'])
    print('          ---------------- Json ----------------         ')
    print(r.text)
    print(u'======================= 创建商品成功 ======================= ')
    return(r.json())


if __name__ == '__main__':
    print(get_crawler_address())
