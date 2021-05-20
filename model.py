# -*- encoding: utf-8 -*-
"""
@File    : model.py
@Time    : 2021/5/19 5:25 下午
@Author  : 0xCAFE
@Email   : admin@mlpod.com
"""

# 导入外部库
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from transformers import T5ForConditionalGeneration, T5Tokenizer

# 导入内部库



class Model(object):
    def __init__(self):
        self.__torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        # self.__model_name = 'tuner007/pegasus_paraphrase'
        # self.__tokenizer = PegasusTokenizer.from_pretrained(self.__model_name)
        # self.__model = PegasusForConditionalGeneration.from_pretrained(self.__model_name).to(torch_device)

        self.__model_name = 'ceshine/t5-paraphrase-quora-paws'
        self.__tokenizer = T5Tokenizer.from_pretrained(self.__model_name)
        self.__model = T5ForConditionalGeneration.from_pretrained(self.__model_name).to(self.__torch_device)
        print('T5-paraphrase-quora-paws model is loaded.')

    def generate(self, input_text, num_return_sequences=20, num_beams=100, num_beam_groups=20, diversity_penalty=100.0):
        batch = self.__tokenizer([input_text], truncation=True, padding='longest', max_length=60,
                                 return_tensors="pt").to(self.__torch_device)
        translated = self.__model.generate(**batch,
                            num_return_sequences=num_return_sequences,
                            num_beams=num_beams, 
                            num_beam_groups=num_beam_groups, 
                            diversity_penalty=diversity_penalty)
        texts = self.__tokenizer.batch_decode(translated, skip_special_tokens=True)
        return texts
