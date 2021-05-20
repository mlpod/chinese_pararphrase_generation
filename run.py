# -*- encoding: utf-8 -*-
"""
@File    : run.py
@Time    : 2021/5/19 5:34 下午
@Author  : 0xCAFE
@Email   : admin@mlpod.com
"""

# 导入外部库

# 导入内部库
from translator import Translator
from model import Model

translator = Translator()
model = Model()

if __name__ == '__main__':
    while True:
        query = input('请输入待复述的句子：')
        if query == '':
            continue
        query_en = translator.translate(query, from_lang='zh', to_lang='en')
        if query_en[0] == '':
            continue
        ret_en = model.generate(query_en[0], num_return_sequences=20, num_beams=100, num_beam_groups=20, diversity_penalty=100.0)
        ret_zh = translator.translate(ret_en, from_lang='en', to_lang='zh')
        for r in ret_zh:
            print(r)