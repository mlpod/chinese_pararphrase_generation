# -*- encoding: utf-8 -*-
"""
@File    : translator.py
@Time    : 2021/5/19 4:58 下午
@Author  : 0xCAFE
@Email   : admin@mlpod.com
"""

# 导入外部库
import json
import yaml
import random
import requests
from hashlib import md5


# 导入内部库


class Translator(object):
    def __init__(self):
        with open('conf.yaml', 'r') as f:
            conf = yaml.full_load(f)
        self.__appid = str(conf['appid'])
        self.__appkey = str(conf['appkey'])
        self.__url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        self.__headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def make_md5(self, s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    def translate(self, query, from_lang, to_lang):
        if type(query) == list:
            query = '\n'.join(query)

        salt = random.randint(32768, 65536)
        sign = self.make_md5(self.__appid + query + str(salt) + self.__appkey)
        payload = {'appid': self.__appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

        r = requests.post(self.__url, params=payload, headers=self.__headers)
        result = r.json()
        while 'error_code' in result and result['error_code'] == '54003':
            r = requests.post(self.__url, params=payload, headers=self.__headers)
            result = r.json()

        if 'error_code' in result:
            return ['']
        return [result['dst'] for result in result['trans_result']]


if __name__ == '__main__':
    t = Translator()
    q = 'hello'
    ret = t.translate(q, from_lang='en', to_lang='zh')
    print(ret)
