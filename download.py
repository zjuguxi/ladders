#!/usr/bin/env python
# encoding: utf-8

import requests
from clint.textui import progress
from bs4 import BeautifulSoup
from urllib import parse
import os
import sys

# 如不使用下述环境变量，可以用requests的proxies参数
# os.system('export https_proxy=http://127.0.0.1:1087')
# os.system('export http_proxy=http://127.0.0.1:1087')

proxies = {'http': 'http://127.0.0.1:1087',  # shadowsocks的http代理
           'https': 'http://127.0.0.1:1087'}

target_dir = '~/Desktop/' if sys.argv[1] is None

conf = {'lantern': {'name': '蓝灯Lantern for Mac',
                    'url': 'https://raw.githubusercontent.com/getlantern/lantern-binaries/master/lantern-installer-beta.dmg',
                    'path': os.path.join(target_dir, 'Mac/lantern-installer-beta.dmg')},
        'psiphon': {'name': '赛风Psiphon for Win',
                    'url': 'https://psiphon.ca/psiphon3.exe',
                    'path': os.path.join(target_dir, 'Win/psiphon3.exe')},
        'psiphon_android': {'name': '赛风Psiphon for Android',
                            'url': 'https://psiphon.ca/PsiphonAndroid.apk',
                            'path': os.path.join(target_dir, 'Android/PsiphonAndroid.apk')},
        'wujie': {'name': '无界 for Win',
                  'url': 'https://s3.amazonaws.com/xiazai/u.zip',
                  'path': os.path.join(target_dir, 'Win/无界.zip')},
        'wujie_android': {'name': '无界安卓版',
                          'url': 'https://s3.amazonaws.com/wujie/um.apk',
                          'path': os.path.join(target_dir, 'Android/无界安卓.apk')},
        'resilio_mac': {'name': '同步工具Resilio Sync for Mac',
                        'url': 'https://download-cdn.resilio.com/stable/osx/Resilio-Sync.dmg',
                        'path': os.path.join(target_dir, 'Resilio_Sync/[Mac]Resilio Sync.dmg')},
        'resilio_win': {'name': '同步工具Resilio Sync for Win',
                        'url': 'https://download-cdn.resilio.com/stable/windows64/Resilio-Sync_x64.exe',
                        'path': os.path.join(target_dir, 'Resilio_Sync/[Win64]Resilio Sync.exe')}
        }


# 抓取处理自由门的下载链接
def freegate_crawler():
    freegate_site = 'http://dongtaiwang.com'
    r = requests.get(freegate_site, proxies=proxies)
    soup = BeautifulSoup(r.text, 'lxml')
    freegate_url = freegate_site + soup.find('a', class_='download')['href']
    parse_result = parse.urlparse(freegate_url)
    file_name = parse_result[2].rpartition('/')[-1]
    freegate_dict = {'freegate': {'name': '自由门FreeGate',
                                  'url': freegate_url,
                                  'path': target_dir + '/Win/' + file_name}}
    conf.update(freegate_dict)


# 开始下载
def download(path, r, name):
    print('正在下载：{}'.format(name))
    print('该文件位置：{}'.format(path))
    with open(path, 'w+') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
            if chunk:
                f.write(str(chunk))
                f.flush()


# 处理并验证conf，并传入 download()
def download_all(conf_dict):
    for file_tuple in conf_dict.items():
        file_dict = file_tuple[1]

        r = requests.get(file_dict['url'], stream=True, proxies=proxies)
        if r.status_code == 200:
            pass
        else:
            print('现在这个链接无法下载：{}'.format(file_dict['url']))
            continue
        name = file_dict['name']
        download(file_dict['path'], r, name)


def make_folder(target_dir):
    os.system('mkdir {}'.format(target_dir))
    os.system('mkdir {}/Win'.format(target_dir))
    os.system('mkdir {}/Resilio_Sync'.format(target_dir))
    os.system('mkdir {}/Mac'.format(target_dir))
    os.system('mkdir {}/Android'.format(target_dir))


if __name__ == '__main__':

    make_folder(target_dir)
    freegate_crawler()
    download_all(conf)
    file_list = [v['name'] for k, v in conf.items()]
    for file in file_list:
        print(file)
    print('全部完成')
