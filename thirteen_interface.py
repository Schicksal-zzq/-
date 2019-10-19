# Author: Administrator
# date: 2019/10/17  16:33

import requests

class pokerCard:
    def __init__(self, color, number):
        self.color = color
        self.number = number

wholePoker1 = []

def colorToNum(str):
    if str == '$':
        return 1
    elif str == '&':
        return 2
    elif str == '*':
        return 3
    elif str == '#':
        return 4

def numToColor(x):
    if x == 1:
        return '$'
    elif x == 2:
        return '&'
    elif x == 3:
        return '*'
    elif x == 4:
        return '#'

def numToPoker(x):
    if x == 10:
        return '10'
    elif x == 11:
        return 'J'
    elif x == 12:
        return 'Q'
    elif x == 13:
        return 'K'
    elif x == 14:
        return 'A'
    return str(x)

def login():
    '''
    包括登入，注册，验证
    '''
    global token, user_id
    url = "https://api.shisanshui.rtxux.xyz/auth/login"
    print("请输入用户名与密码：")
    username = input()
    password = input()
    headers = {"content-type" : "application/json"}
    formdata = {"username": username, "password": password}
    response = requests.post(url, data=formdata, headers=headers)
    res = response.json()   #转为json格式便于引用
    if res['status'] != '0':
        print("用户不存在，请注册后登入：")
        print("请输入要注册的用户名与密码")
        username = input()
        password = input()
        url = "https://api.shisanshui.rtxux.xyz/auth/register"
        headers = {"content-type": "application/json"}
        formdata = {"username": username, "password": password}
        response = requests.post(url, data=formdata, headers=headers)
        print("注册情况:"+ response.text)
        url = "https://api.shisanshui.rtxux.xyz/auth/login"
        print("请输入用户名与密码：")
        username = input()
        password = input()
        headers = {"content-type": "application/json"}
        formdata = {"username": username, "password": password}
        response = requests.post(url, data=formdata, headers=headers)
        res = response.json()
    token = res['data']['token']
    user_id = res['data']['user_id']
    print("登入状态:"+ response.text)
    url = "https://api.shisanshui.rtxux.xyz/auth/validate"
    headers = {"X-Auth-Token": token}
    response = requests.get(url, headers=headers)
    print("检测状态:"+ response.text)

def ranking():
    '''
    排行榜
    '''
    url = "https://api.shisanshui.rtxux.xyz/rank"
    response = requests.get(url)
    print(response.text)

def historicalRecords(limit, page):
    '''
    历史战局列表
    '''
    global user_id
    url = 'https://api.shisanshui.rtxux.xyz/history'
    headers = {'X-Auth-Token': token}
    params = {'player_id': use,'limit': limit,'page': page}
    response = requests.get(url, params=params, headers=headers)
    print(response.text)

def historicalRecordsDetail():
    '''
    历史战局详情
    '''
    global id
    url = 'https://api.shisanshui.rtxux.xyz/history/{id}'
    headers = {'X-Auth-Token': token}
    params = {'id':id}
    response = requests.get(url, params=params, headers=headers)
    print(response.text)

def startGame():
    '''
    包括开始战局和初始化牌
    '''
    global token, id
    url = "https://api.shisanshui.rtxux.xyz/game/open"
    headers = {"X-Auth-Token": token}
    response = requests.post(url, headers=headers)
    ret = response.json()
    print(response.text)
    id = ret['data']['id'];
    card = ret['data']['card']
    card = card.replace('10', 'T')
    for i in range(0, 13):
        i *= 3
        temp = card[i+1]
        if temp == 'T':
            wholePoker1.append(pokerCard(colorToNum(card[i]), 10))
        elif temp == 'J':
            wholePoker1.append(pokerCard(colorToNum(card[i]), 11))
        elif temp == 'Q':
            wholePoker1.append(pokerCard(colorToNum(card[i]), 12))
        elif temp == 'K':
            wholePoker1.append(pokerCard(colorToNum(card[i]), 13))
        elif temp == 'A':
            wholePoker1.append(pokerCard(colorToNum(card[i]), 14))
        else:
            wholePoker1.append(pokerCard(colroToNum(card[i]), int(temp)))
