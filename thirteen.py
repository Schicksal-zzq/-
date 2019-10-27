# Author: Administrator
# date: 2019/10/17  21:28

import time
import json
from thirteen_interface import *

ans1, ans2, ans3 = [], [], []   #标记
shui1, shui2, shui3 = 0.0, 0.0, 0.0     #水水水
score1, score2, score3 = 0.0, 0.0, 0.0  #大大大小
currentshui1, currentshui2, currentshui3 = 0.0, 0.0, 0.0    #临时
bottomPoker, middlePoker, topPoker, lastPoker= [], [], [], []   #最终的牌
currentscore1, currentscore2, currentscore3 = 0.0, 0.0, 0.0     #临时
wholePoker1, wholePoker2, wholePoker3 = [], [], []    #分堆的牌
currentBottomPoker, currentMiddlePoker, currentTopPoker = [], [], []    #临时的牌

def initAll():
    ans1.clear()
    ans2.clear()
    ans3.clear()
    topPoker.clear()
    middlePoker.clear()
    bottomPoker.clear()
    wholePoker1.clear()
    wholePoker2.clear()
    wholePoker3.clear()
    currentTopPoker.clear()
    currentBottomPoker.clear()
    currentMiddlePoker.clear()
    global shui1, shui2, shui3
    global score1, score2, score3
    global currentshui1, currentshui2, currentshui3
    global currentscore1, currentscore2, currentscore3
    shui1, shui2, shui3 = 0.0, 0.0, 0.0
    score1, score2, score3 = 0.0, 0.0, 0.0
    currentshui1, currentshui2, currentshui3 = 0.0, 0.0, 0.0
    currentscore1, currentscore2, currentscore3 = 0.0, 0.0, 0.0

    for i in range(0, 15):
        ans1.append(0)
        ans2.append(0)
        ans3.append(0)
        bottomPoker.append(pokerCard(0, 0))
        middlePoker.append(pokerCard(0, 0))
        topPoker.append(pokerCard(0, 0))
        wholePoker1.append(pokerCard(0, 0))
        wholePoker2.append(pokerCard(0, 0))
        wholePoker3.append(pokerCard(0, 0))
        currentTopPoker.append(pokerCard(0, 0))
        currentMiddlePoker.append(pokerCard(0, 0))
        currentBottomPoker.append(pokerCard(0, 0))


def getnumber(x):
    return x.number


def typeOfPokerCard(x):
    """先处理同花顺，顺子和同花"""
    a = []
    flag1, flag2 = 1, 1
    for i in range(0, 4):
        a.append(x[i].number)
        if x[i].number != x[i+1].number-1:
            flag1 = 0
        if x[i].color != x[i+1].color:
            flag2 = 0
    a.append(x[4].number)
    if flag1 and flag2:
        score = 9+(a[4]/100)+(a[3]/100000)+(a[2]/10000000)+(a[1]/1000000000)+(a[0]/100000000000)
        return score
    elif flag1:
        score = 5+(a[4]/100)+(a[3]/100000)+(a[2]/10000000)+(a[1]/1000000000)+(a[0]/100000000000)
        return score
    elif flag2:
        score = 6+(a[4]/100)+(a[3]/100000)+(a[2]/10000000)+(a[1]/1000000000)+(a[0]/100000000000)
        return score

    '''炸弹情况'''
    if (a[0] == a[1] or a[3] == a[4]) and a[1] == a[2] and a[2] == a[3]:
        score = 8+((4*a[2])/100)
        return score

    '''葫芦情况'''
    if (a[0] == a[1] and a[1] == a[2] and a[3] == a[4]) or (a[0] == a[1] and a[2] == a[3] and a[3] == a[4]):
        score = 7+((3*a[2])/100)
        return score

    '''三条情况'''
    if a[0] == a[1] and a[1] == a[2] or a[1] == a[2] and a[2] == a[3] or a[2] == a[3] and a[3] == a[4]:
        score = 4+((3*a[2])/100)
        return score

    '''二对情况'''
    if (a[0] == a[1] and a[2] == a[3]) or (a[1] == a[2] and a[3] == a[4]) or (a[0] == a[1] and a[3] == a[4]):
        if a[3] == a[1] + 1:
            score = 3+((2*a[3])/100)+((2*a[1])/100)+0.15
        else:
            score = 3+((2*a[3])/100)+((2*a[1])/100000)
        return score

    '''对子情况'''
    if a[0] == a[1]:
        score = 2+((2*a[0])/100)+(a[4]/100000)+(a[3]/10000000)+(a[2]/1000000000)
        return score
    elif a[1] == a[2]:
        score = 2+((2*a[1])/100)+(a[4]/100000)+(a[3]/10000000)+(a[0]/1000000000)
        return score
    elif a[2] == a[3]:
        score = 2+((2*a[2])/100)+(a[4]/100000)+(a[1]/10000000)+(a[0]/1000000000)
        return score
    elif a[3] == a[4]:
        score = 2+((2*a[3])/100)+(a[2]/100000)+(a[1]/10000000)+(a[0]/1000000000)
        return score

    '''散牌情况'''
    score = 1+(a[4]/100)+(a[3]/100000)+(a[2]/10000000)+(a[1]/1000000000)+(a[0]/100000000000)
    return score


def getTopScore():
    global currentshui1, currentTopPoker
    a = currentTopPoker[0].number
    b = currentTopPoker[1].number
    c = currentTopPoker[2].number
    if a == b and b == c:
        topScore = 4+((a+b+c)/100)
        currentshui1 = 1.7
    elif a == b:
        topScore = 2+((2*a)/100)+c/10000
        currentshui1 = 1.42+(topScore-int(topScore))/100
        if topScore > 2.20:
            currentshui1 += 0.12
    elif b == c:
        topScore = 2+((2*b)/100)+a/10000
        currentshui1 = 1.42+(topScore-int(topScore))/100
        if topScore > 2.20:
            currentshui1 += 0.12
    else:
        topScore = 1+c/100+b/10000+a/1000000
        currentshui1 = 1.22+(topScore-int(topScore))/100
    return topScore


def getMiddleScore():
    global currentshui2, currentMiddlePoker
    score = typeOfPokerCard(currentMiddlePoker)
    types = int(score)
    if types == 9:
        currentshui2 = 10.0
    elif types == 8:
        currentshui2 = 8.0
    elif types == 7:
        currentshui2 = 2.0
    elif types == 6:
        currentshui2 = 1.9+(score-int(score))/100
    elif types == 5:
        currentshui2 = 1.8+(score-int(score))/100
    elif types == 4:
        currentshui2 = 1.55
    elif types == 3:
        currentshui2 = 1.4+(score-int(score))/100
    elif types == 2:
        currentshui2 = 1.1+(score-int(score))/100
    else:
        currentshui2 = 1.0
    return score


def getBottomScore():
    global currentshui3, currentBottomPoker
    score = typeOfPokerCard(currentBottomPoker)
    types = int(score)
    if types == 9:
        currentshui3 = 5.0
    elif types == 8:
        currentshui3 = 4.0
    elif types == 7:
        currentshui3 = 1.99
    elif types == 6:
        currentshui3 = 1.89+(score-int(score))/100
    elif types == 5:
        currentshui3 = 1.79+(score-int(score))/100
    elif types == 4:
        currentshui3 = 1.54
    elif types == 3:
        currentshui3 = 1.39+(score-int(score))/100
    elif types == 2:
        currentshui3 = 1.09+(score-int(score))/100
    else:
        currentshui3 = 1.00
    return score


def checkBestPoker():
    global currentscore1, currentscore2, currentscore3
    """计算头墩, 规则里面没说头墩有其他情况，当然选择不做其他判断!!。"""
    currentscore1 = getTopScore()
    '''计算中墩'''
    currentscore2 = getMiddleScore()
    '''计算底墩，只需在中墩基础上修改数值即可'''
    currentscore3 = getBottomScore()

    if currentscore1 <= currentscore2 <= currentscore3:
        ret = 0
        global shui1, shui2, shui3, score1, score2, score3, currentshui1, currentshui2, currentshui3
        global middlePoker, bottomPoker, topPoker, currentTopPoker, currentMiddlePoker, currentBottomPoker
        if currentshui1+currentshui2+currentshui3 > shui1+shui2+shui3:
            shui1 = currentshui1
            shui2 = currentshui2
            shui3 = currentshui3
            for i in range(0, 5):
                middlePoker[i] = currentMiddlePoker[i]
                bottomPoker[i] = currentBottomPoker[i]
            for i in range(0, 3):
                topPoker[i] = currentTopPoker[i]


def getPokerCardTwo(n2, x2):
    global ans2, currentMiddlePoker, wholePoker2, currentTopPoker
    for t in range(n2, 8):
        ans2[t] = 1
        currentMiddlePoker[x2] = wholePoker2[t]
        if x2 == 4:
            cnt2 = 0
            for j in range(0, 8):
                if ans2[j] == 0:
                    currentTopPoker[cnt2] = wholePoker2[j]  #剩下的牌就是前墩了
                    cnt2 += 1
            checkBestPoker()
        else:
            getPokerCardTwo(t+1, x2+1)
        ans2[t] = 0


def getPokerCardOne(n1, x1):
    global ans1, currentBottomPoker, wholePoker1, wholePoker2
    for t in range(n1, 13):
        ans1[t] = 1
        currentBottomPoker[x1] = wholePoker1[t]
        if x1 == 4:
            cnt1 = 0
            for j in range(0, 13):
                if ans1[j] == 0:
                    wholePoker2[cnt1] = wholePoker1[j]   #把没用过的牌记下来
                    cnt1 += 1
            getPokerCardTwo(0, 0)
        else:
            getPokerCardOne(t+1, x1+1)
        ans1[t] = 0


def printPoker():
    """前墩"""
    str = ""
    global shui1, shui2, shui3, lastPoker, topPoker, middlePoker, bottomPoker
    for i in range(0, 3):
        str += (numToColor(topPoker[i].color)) + (numToPoker(topPoker[i].number))
        if i < 2:
            str += ' '
    print(str)
    lastPoker.append(str)

    '''中墩'''
    str = ""
    for i in range(0, 5):
        str += (numToColor(middlePoker[i].color)) + (numToPoker(middlePoker[i].number))
        if i < 4:
            str += ' '
    print(str)
    lastPoker.append(str)

    '''后墩'''
    str = ""
    for i in range(0, 5):
        str += (numToColor(bottomPoker[i].color)) + (numToPoker(bottomPoker[i].number))
        if i < 4:
            str += ' '
    print(str)
    print(shui1+shui2+shui3)
    lastPoker.append(str)
    return lastPoker

ranking()
login()
i = 10
while(i):
    initAll()
    wholePoker1 = startGame()
    wholePoker1.sort(key=getnumber)
    getPokerCardOne(0, 0)
    lastPoker = []
    lastPoker = printPoker()
    id = submitGame(lastPoker)
    #i -= 1
    time.sleep(10)
    historicalRecordsDetail(id)
    historicalRecords(10, 10)
