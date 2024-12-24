import json
import time
import base64
import requests
from helium import *


def sendMsg(qqUserId, msg):
    # OneBot 接口
    api = 'http://127.0.0.1:5701/send_private_msg'
    data = {
        'message': msg,
        'user_id': qqUserId,
    }
    requests.post(api, json=data)


with open('config.json', 'r') as f:
    config = json.load(f)
    username = config['username']
    password = base64.b64decode(config['password']).decode('utf-8')
    qqUserId = config['qqUserId']

driver = start_chrome('http://jwgl.usst.edu.cn/sso/jziotlogin')

wait_until(Button('登录').exists)
write(username, into='用户名')
write(password, into='密码')
click('登录')

wait_until(Text('选课').exists)
click('选课')
click('个人课表查询')

wait_until(Button('查询').exists)
while True:
    wait_until(S('#table1').exists)
    if (not S('.nodata').exists()):
        sendMsg(qqUserId, '课表安排已出')
        click('列表')
        time.sleep(1)
        img = get_driver().execute_cdp_cmd('Page.captureScreenshot', {
            'format': 'png',
            'captureBeyondViewport': True,
        })['data']
        sendMsg(qqUserId, f'[CQ:image,file=base64://{img}]')
        kill_browser()
        exit()
    time.sleep(5)
    click('查询')
