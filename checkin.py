# %%
import datetime
import random
import sys
from hashlib import md5
from time import sleep

import requests

# %%
# rand time
print('Triggered at %s' % (datetime.datetime.now()))

rand_time = random.random() * 3600
print('Scheduled at %s' % (datetime.datetime.now() + datetime.timedelta(seconds=rand_time)))
if len(sys.argv) <= 2:
    sleep(rand_time)

print('Started at %s' % (datetime.datetime.now()))

# %% const
CASTGC = sys.argv[1]
session = requests.Session()

# %% list
response = session.get(
    url=r'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do',
    headers={
        'User-Agent': 'cpdaily/9.0.15 wisedu/9.0.15',
        'Referer': 'http://ehallapp.nju.edu.cn/xgfw/sys/mrjkdkappnju/index.html'
    },
    cookies={'CASTGC': CASTGC}
)

try:
    content = response.json()
except ValueError:
    content = {}
if response.status_code == 200 and content.get('code') == '0':
    print('List: %d, %s, %s' % (response.status_code, response.reason, content.get('msg') or 'No messgage available'))
else:
    print('List: %d, %s, %s' % (response.status_code, response.reason, content.get('msg') or 'No messgage available'))
    exit(1)

data = next(x for x in content['data'] if x.get('TJSJ') != '')
wid = content['data'][0]['WID']

# %% get MD5
response = session.get(
    url=r'http://ehallapp.nju.edu.cn/xgfw//sys/yqfxmrjkdkappnju/apply/getMd5Value.do',
    headers={
        'User-Agent': 'cpdaily/9.0.15 wisedu/9.0.15',
        'Referer': 'http://ehallapp.nju.edu.cn/xgfw/sys/mrjkdkappnju/index.html'
    },
    cookies={'CASTGC': CASTGC}
)

try:
    content = response.text
except ValueError:
    content = {}
if response.status_code == 200 and len(content) > 0:
    print('MD5: %d, %s' % (response.status_code, response.reason or 'No messgage available'))
else:
    print('MD5: %d, %s' % (response.status_code, response.reason or 'No messgage available'))
    exit(1)

md5_value = content


# %% apply
data_apply = {
    'CURR_LOCATION': data['CURR_LOCATION'],
    'IS_HAS_JKQK': data['IS_HAS_JKQK'],
    'IS_TWZC': data['IS_TWZC'],
    'JRSKMYS': data['JRSKMYS'],
    'JZRJRSKMYS': data['JZRJRSKMYS'],
    'SFZJLN': data['SFZJLN'],
    'WID': wid,
    'ZJHSJCSJ': (datetime.datetime.now() - random.randint(0, 1) * datetime.timedelta(days=1)).strftime(r'%Y-%m-%d') + ' %02d' % (random.randint(0, 16))
}
data_apply['sign'] = md5('|'.join(list(data_apply.values()) + [md5_value]).encode("utf-8")).hexdigest()

print(data_apply)

response = session.get(
    url=r'http://ehallapp.nju.edu.cn/xgfw//sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do',
    params=data_apply,
    headers={
        'User-Agent': 'cpdaily/9.0.15 wisedu/9.0.15',
        'Referer': 'http://ehallapp.nju.edu.cn/xgfw/sys/mrjkdkappnju/index.html'
    },
    cookies={'CASTGC': CASTGC}
)

try:
    content = response.json()
except ValueError:
    content = {}
if response.status_code == 200 and content.get('code') == '0':
    print('Apply: %d, %s, %s' % (response.status_code, response.reason, content.get('msg') or 'No messgage available'))
else:
    print('Apply: %d, %s, %s' % (response.status_code, response.reason, content.get('msg') or 'No messgage available'))
    exit(1)
pass

# %%
print('Finished at %s' % (datetime.datetime.now()))