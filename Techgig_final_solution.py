import pandas as pd
import numpy as np
from nltk.corpus import words, brown
import re

train_df = pd.read_csv('train.csv', header=0)
test_df = pd.read_csv('test.csv')

train_df.columns = ['id','target','description']

correct_words1 = set(word.lower() for word in words.words())
correct_words2 = set(word.lower() for word in brown.words())

unique_target_words = train_df['target'].unique()
unique_meaningful_words = [w for w in unique_target_words if w in correct_words1 or w in correct_words2]

train_df['description'] = train_df['description'].str.replace("[:';\",]",' ')
test_df['description'] = test_df['description'].str.replace("[:';\",]",' ')

unique_non_meaningful_words = [w for w in unique_target_words if w not in correct_words1 and w not in correct_words2]

pat = re.compile(r'(http //|https //|https://)?([^/\s.]+)[^\s]+\.(?:org|net|com(?:\d*))\b|\b((?:[0-9]{1,3}\.){3}[0-9]{1,3})\b')

def new_url_matcher(s):
    result = []
    items = s.split(' ')
    for i in items:
        m = pat.search(i)
        if m:
            for word in set(m.groups()):
                if word:
                    if word in unique_target_words: result.append(word)
    if len(result)<1: result.append('garbage_value')

    if len(set(result))>1: 
        for text in set(result):
            if text.find('-') != -1:
                t = text.split('-')
                try:
                    x = int(t[-1])
                except:
                    result = [text]
                    break
            else:
                result = text

    def return_first_match():
        for i in items:
            if i in unique_target_words:
                return i
            
    # returns the first matched url or word like url
    # eg. ddlsql41.inin.net ===> ddlsql41
    #     esc-vnx-01        ===> esc-vnx-01
    def return_first_word(url):
        for i in url:
            i = ''.join(i)
            if i in unique_non_meaningful_words:
                return i
    if items[0] == 'archfull' or items[0] == 'response':
        return 'ldtpocs_ddldon'
    if items[0] == 'cisco':
        ip = ['10.200.3.68.','10.200.1.21.']
        if 'service' in items and (ip[0] in s or ip[1] in s):
            if 'cisco elm client service' in s:
                return 'service'
        
        w = 'configuration item'
        ind = s.find(w)
        loca = s.find('location')
        new_word = s[ind:loca].split(' ')
        for i in new_word:
            if i in unique_target_words:
                return i
            
    if items[0] == 'status': 
        if 'gpmszmaas_ptl2' in s:
            return 'gpmszmaas_ptl2'
        if 'ldtpocs_ddldon' in s:
            return 'ldtpocs_ddldon'
    if items[0] == 'tcp' and 'ddl-ch-01' in s:
        return 'ddl-ch-01'
    if items[0] == 'emc':
        urls = re.findall(pat,s)
        f = False
        for i in urls:
            i = ''.join(i)
            if i in unique_non_meaningful_words: 
                f = True
                return i
        if not f:
            for i in items:
                if i in unique_non_meaningful_words:
                    return i

    if 'this database' in s:
        return return_first_word(re.findall(pat,s))
    if items[0] == 'database' and (items[1] == 'mirroring' 
                                   or items[1] == 'mirror'):
        return return_first_word(re.findall(pat,s))
    
    if items[0] == 'failed':
        urls = re.findall(pat,s)
        f = False
        for i in urls:
            i = ''.join(i)
            if i in unique_non_meaningful_words: 
                f = True
                return i
        if not f:
            for i in items:
                if i in unique_non_meaningful_words:
                    return i
    if items[0] == 'operations' or items[0] == 'iis' or items[0] == 'many':
        return return_first_word(re.findall(pat,s))
    
    if isinstance(result, list):
        if len(result)> 1:
            if len(set(result)) > 1:
                return ''.join(result[0])
            return ''.join(result[-1])

    if 'garbage_value' in result:
        if items[0] == 'commvault':
            if 'will' in items:
                return 'will'
            return return_first_match()
        if 'me$mocs_test' in s:
            return 'grdp'
        if items[0] == 'teahhl':
            for i in items:
                if i == 'service': continue
                if i in unique_target_words: return i
        
        return return_first_match()
    
    return ''.join(result) 


df = test_df[:]
df['StringToExtract'] = df['description'].apply(new_url_matcher)
df.to_csv('Techgig_final.csv', columns=['id','StringToExtract'], header=True, index=False)
