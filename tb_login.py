#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Em on 2018/1/9


import os
import time
import json
import sys
import random
from config import *
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


COOKIE_FILE = './conf/cookie'
COOKIE_TIME_FILE = './conf/cookie_time'

# 登陆地址
login_url = 'https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http%3A%2F%2Flogin.taobao.com%2Fmember%2Ftaobaoke%2Flogin.htm%3Fis_login%3d1&full_redirect=true&disableQuickLogin=true'
DEBUG = False

def get_cookies(auto_login=False):
    # 获取 cookies
    cookies = None
    if os.path.exists(COOKIE_TIME_FILE) and os.path.exists(COOKIE_FILE):
        try:
            with open(COOKIE_TIME_FILE, 'r') as f:
                save_time = int(f.read())
                if (int(time.time()) - save_time) < 600 * 1:
                    with open(COOKIE_FILE, 'r') as f:
                        print u'存在 cookie 并且未过期'
                        cookies = json.loads(f.read())
        except Exception as e:
            if DEBUG: print e

    # 不存在 cookie 或者 cookie 过期
    if not cookies:
        print u'不存在 cookie ，登陆淘宝获取 cookie'
        # 打开浏览器
        browser = webdriver.Chrome('./chromedriver')
        browser.get(login_url)
        time.sleep(5)

        # 登陆
        if auto_login:
            print u'自动登陆获取 cookie'
            _login_simulation(browser)
        print u'手动登陆获取 cookie'

        # 判断登陆
        _login_success(browser)
        print u'登陆成功'

        # 手动登录获取 cookies
        cookies = {item["name"]: item["value"] for item in browser.get_cookies()}
        with open(COOKIE_FILE, 'w') as f:
            f.write(json.dumps(cookies))
        with open(COOKIE_TIME_FILE, 'w') as f:
            f.write(str(int(time.time())))
        print u'获取 cookie 成功，退出浏览器'
        browser.quit()
    return cookies

# 登陆成功
def _login_success(device):
    return True
    # while True:
    #     print 'wait login  ... '
    #     time.sleep(3)
    #     try:
    #         if device.find_elements_by_link_text(u'进入我的联盟'):
    #             return True
    #     except Exception as e:
    #         if DEBUG: print e


# 判断是否有滑动
def _has_move(device):
    yanzhen = device.find_element_by_id('nocaptcha')
    style = yanzhen.get_attribute('style')
    if style == 'display: block;':
        return True
    return False

# 模拟滑动
def _move_simulation(device, e):
    try:
        action = ActionChains(device)
        action.click_and_hold(e).perform()
        # action.reset_actions()
        offset = 21
        for i in range(210 / offset):
            ActionChains(device).move_by_offset(xoffset=offset, yoffset=0).perform()
            time.sleep((offset - i) / 50)
        action.release().perform()
        action.reset_actions()
    except Exception as e:
        if DEBUG: print e


# 模拟输入
def _input_simulation(e, text):
    e.send_keys(text)
    # for i in range(len(text)):
    #     sleep_time = random.randint(8, 30)
    #     time.sleep(sleep_time / 10)
    #     e.send_keys(text[i])

def _login_simulation(device, auto=False):
    while True:
        print u'点击账号登陆'
        # login_frame_e = device.find_element_by_xpath('//*[@id="mx_n_18"]/div/iframe')
        # login_frame = device.switch_to.frame(login_frame_e)

        # 输入账号密码
        print u'输入账号密码'
        static_button = device.find_element_by_id('J_Quick2Static')
        static_button.click()
        time.sleep(random.uniform(0.5, 2))
        _input_simulation(device.find_element_by_id('TPL_username_1'), get_username())
        time.sleep(random.uniform(0.5, 2))
        _input_simulation(device.find_element_by_id('TPL_password_1'), get_password())

        # 检查滑动验证 display: block;
        print u'判断是否有滑动验证'
        if _has_move(device):
            print u'有滑动验证 ================ '
            _move_simulation(device, device.find_element_by_id('nc_1_n1z'))
        

         # 点击登陆
        print u'开始登陆'
        time.sleep(0.5)
        device.find_element_by_id('J_SubmitStatic').submit()

        if device.current_url.find('https://www.alimama.com') != 0:
            print u'验证出错，刷新页面重试'
            device.refresh()
            time.sleep(10)
        else:
            break

    print u'================================ 结束 ====================================='
    time.sleep(1)


if __name__ == '__main__':
    print get_cookies(True)

