from helium import *
import base64
import time
import requests


def sendMsg(qqUserId, msg):
    # OneBot 接口
    api = 'http://127.0.0.1:5701/send_private_msg'
    data = {
        'message': msg,
        'user_id': qqUserId,
    }
    requests.post(api, json=data)


with open('username.txt', 'r') as f:
    username = f.read().strip()
with open('password.txt', 'r') as f:
    password = base64.b64decode(f.read().strip()).decode('utf-8')
with open('qqUserId.txt', 'r') as f:
    qqUserId = f.read().strip()
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
    click('查询')
    wait_until(S('#table1').exists)
    if (not S('.nodata').exists()):
        get_driver().save_screenshot('schedule.png')
        with open('schedule.png', 'rb') as f:
            img = base64.b64encode(f.read()).decode('utf-8')
            sendMsg(qqUserId, f'课表安排已出：[CQ:image,file=base64://{img}]')
        kill_browser()
        exit()
    time.sleep(5)
