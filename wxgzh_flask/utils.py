# -*- coding: utf-8 -*-
import os
import socket
import time
import zipfile
from io import BytesIO
from threading import Thread

import requests
from flask import jsonify, render_template, send_file
from selenium import webdriver
from selenium.webdriver.common.by import By

from config import main_page_url, detail_page_url, request_delay, user_agent, gzh_list_url, js_delay, source_page_path

file_path = os.path.split(os.path.realpath(__file__))


def get_selenium_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    chrome_driver = f'{file_path[0]}/chromedriver'
    driver_1 = webdriver.Chrome(options=options, executable_path=chrome_driver)
    driver_1.set_window_size(1853, 1053)
    return driver_1


driver = get_selenium_driver()


def get_qr_code():
    try:
        driver.get(main_page_url)
        time.sleep(request_delay)
        page_source = driver.get_screenshot_as_base64()
        return page_source
    except Exception:
        return 'R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='


def get_ips():
    """
    获取本地ip
    :return: 本地ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        print('get ip error')
        return ''
    return ip


def wait_for_window(vars, timeout=1000):
    time.sleep(round(timeout / 1000))
    wh_now = driver.window_handles
    wh_then = vars["window_handles"]
    if len(wh_now) > len(wh_then):
        return set(wh_now).difference(set(wh_then)).pop()


def get_fakeid(cookie, token, gzh_name):
    headers = {
        "Cookie": cookie,
        "User-Agent": user_agent,
    }
    data = {
        "action": "search_biz",
        "begin": "0",
        "count": "5",
        "query": gzh_name,
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1"
    }
    content_json = requests.get(gzh_list_url, headers=headers, params=data).json()
    return content_json['list'][0]['fakeid']


def webshot(url, path_prefix, title, driver):
    driver.maximize_window()
    # 返回网页的高度的js代码
    js_height = "return document.body.clientHeight"
    link = url
    # driver.get(link)
    try:
        driver.get(link)
        time.sleep(request_delay)
        k = 1
        height = driver.execute_script(js_height)
        while True:
            if k * 500 < height:
                js_move = "window.scrollTo(0,{})".format(k * 500)
                driver.execute_script(js_move)
                time.sleep(js_delay)
                height = driver.execute_script(js_height)
                k += 1
            else:
                break
        scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(scroll_width, scroll_height)
        driver.get_screenshot_as_file(f'{path_prefix}/pics/{title}.png')
        page_data = driver.page_source
        with open(f'{path_prefix}/html/{title}.html', "wb") as f:
            f.write(page_data.encode("utf-8", "ignore"))
        print("Process {} get one pic !!!".format(os.getpid()))
        time.sleep(0.1)
    except Exception as e:
        print(title, e)


def get_dir(filename):
    """判断文件夹是否存在，如果不存在就创建一个"""
    if not os.path.isdir(filename):
        os.makedirs(filename)


def get_dir_name(path):
    dir_l = []
    for file in os.listdir(path):
        file_path = f'{path}/{file}'
        if os.path.isdir(file_path):
            dir_l.append(file)
    return dir_l


def do_spider(cookie, token, fakeid, start_page, end_page, path_prefix, flag=False):
    get_dir(path_prefix)
    get_dir(f'{path_prefix}/pics')
    get_dir(f'{path_prefix}/html')
    url = detail_page_url
    headers = {
        "Cookie": cookie,
        "User-Agent": user_agent,
    }
    data = {
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "action": "list_ex",
        "begin": "0",
        "count": "5",
        "query": "",
        "fakeid": fakeid,
        "type": "9",
    }
    data["begin"] = "0"
    content_json = requests.get(url, headers=headers, params=data).json()
    all_no = content_json['app_msg_cnt']
    if flag:
        return jsonify(content_json)
    page = all_no // 5 if all_no % 5 == 0 else all_no // 5 + 1
    page = end_page if page > end_page else page
    start_page = abs(start_page)
    driver_1 = get_selenium_driver()
    for i in range(start_page, page):
        data["begin"] = i * 5
        while True:
            try:
                # 使用get方法进行提交
                content_json = requests.get(url, headers=headers, params=data).json()
                time.sleep(request_delay)
                # 返回了一个json，里面是每一页的数据
                for item in content_json["app_msg_list"]:
                    # 提取每页文章的标题及对应的url
                    webshot(item["link"], path_prefix, item["title"], driver_1)
                break
            except Exception:
                time.sleep(5)
                continue
    print(f'finish title {path_prefix} download')


def spider_data(path_prefix, gzh_name, start_page, end_page):
    driver.get(main_page_url)
    driver.find_element(By.LINK_TEXT, "素材管理").click()
    vars = {"window_handles": driver.window_handles}
    driver.find_element(By.CSS_SELECTOR, ".weui-desktop-btn").click()
    vars["win2454"] = wait_for_window(vars, 2000)
    driver.switch_to.window(vars["win2454"])
    driver.find_element(By.ID, "js_editor_insertlink").click()
    cookie = ' '.join([f"{i['name']}={i['value']};" for i in driver.get_cookies()])
    token = driver.current_url.split('token=')[1].split('&')[0]
    fakeid = get_fakeid(cookie, token, gzh_name)
    Thread(target=do_spider, args=[cookie, token, fakeid, start_page, end_page, path_prefix]).start()
    name_l = get_dir_name(source_page_path)
    return render_template('show_time.html', name_l=name_l)


def get_zip_file(name):
    dl_name = f'{name}.zip'
    file_list = []
    file_path = f'{source_page_path}/{name}'
    if os.path.isdir(file_path):
        for f1 in os.listdir(file_path):
            dir_path = f'{file_path}/{f1}'
            for f2 in os.listdir(dir_path):
                file_list.append(f'{dir_path}/{f2}')

    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for _file in file_list:
            with open(_file, 'rb') as fp:
                zf.writestr(_file, fp.read())
    memory_file.seek(0)
    return send_file(memory_file, attachment_filename=dl_name, as_attachment=True)
