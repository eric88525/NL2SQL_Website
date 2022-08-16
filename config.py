import torch
import os
base_url = os.getcwd()

dbConfig = {
        'host' : '127.0.0.1',
        'user' : "ericzone",
        'password': "ericzone",
        'database' : "nl2sql",
}

modelConfig = { 
        'm1_pretrained_model_name': "hfl/chinese-roberta-wwm-ext", 
        'm1_tokenizer_name_or_path': "hfl/chinese-roberta-wwm-ext", 
        'm2_pretrained_model_name': "voidful/albert_chinese_large",
        'm2_tokenizer_name_or_path': "voidful/albert_chinese_large", 
        'device':torch.device('cpu'),
        'm1_model_path':f'{base_url}/N2S/saved_models/M1v2_chinese-roberta-wwm-ext_v1',
        'm2_model_path': f'{base_url}/N2S/saved_models/M2_albert_chinese_large_v1',
        'analyze':True
}