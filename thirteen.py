# Author: Administrator
# date: 2019/10/17  21:28

from thirteen_interface import *
from thirteen_interface import wholePoker1

ans1, ans2, ans3 = [], [], []   #标记
shui1, shui2, shui3 = 0.0, 0.0, 0.0     #水水水
bottomPoker, middlePoker, topPoker = [], [], []   #最终的牌
currentshui1, currentshui2, currentshui3 = 0.0, 0.0, 0.0    #临时
currentscore1, currentscore2, currentscore3 = 0.0, 0.0, 0.0     #临时
wholePoker1, wholePoker2, wholePoker3 = [], [], []    #分堆的牌
currentBottomPoker, currentMiddlePoker, currentTopPoker = [], [], []    #临时的牌

for i in range(0,15):
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
    flag1, flag2, num = 1, 1, 0
    for i in range(0, 4):
        a.append(x[i].number)
        num += x[i].number
        if x[i].number != x[i+1].number-1:
            flag1 = 0
        if x[i].color != x[i+1].color:
            flag2 = 0
    a.append(x[4].number)
    num = num/1000
    if flag1 and flag2:
        score = 9+num+0.9
        return score
    elif flag1:
        score = 5+num+0.5
        return score
    elif flag2:
        score = 6+(a[4]/1000)+(a[3]/100000)+(a[2]/10000000)+(a[1]/1000000000)+(a[0]/100000000000)+0.6
        return score

    '''炸弹情况'''
    if (a[0] == a[1] or a[3] == a[4]) and (a[1] == a[2] and a[2] == a[3]):
        score = 8+((4*a[2])/1000)+0.8
        return score

    '''葫芦情况'''
    if (a[0] == a[1] and a[1] == a[2] and a[3] == a[4]) or (a[0] == a[1] and a[2] == a[3] and a[3] == a[4]):
        score = 7+((3*a[2])/1000)+0.7
        return score

    '''三条情况'''
    if (a[0] == a[1] and a[1] == a[2]) or (a[1] == a[2] and a[2] == a[3]) or (a[2] == a[3] and a[3] == a[4]):
        score = 4+((3*a[2])/1000)+0.4
        return score

    '''二对情况'''
    if a[0] == a[1] and a[3] == a[4]:
        score = 3+((2*a[3])/1000)+((2*a[1])/10000000)+0.3
        return score
    elif (a[0] == a[1] and a[2] == a[3]) or (a[1] == a[2] and a[3] == a[4]):
        if a[3] == a[1] + 1:
            score = 3+((2*a[3])/1000)+((2*a[1])/100000)+0.3
        else:
            score = 3+((2*a[3])/1000)+((2*a[1])/10000000)+0.3
        return score

    '''对子情况'''
    if a[0] == a[1]:
        score = 2+((2*a[0])/1000)+(a[4]/100000)+(a[3]/10000000)+(a[2]/1000000000)+0.2
        return score
    elif a[1] == a[2]:
        score = 2+((2*a[1])/1000)+(a[4]/100000)+(a[3]/10000000)+(a[0]/1000000000)+0.2
        return score
    elif a[2] == a[3]:
        score = 2+((2*a[2])/1000)+(a[4]/100000)+(a[1]/10000000)+(a[0]/1000000000)+0.2
        return score
    elif a[3] == a[4]:
        score = 2+((2*a[3])/1000)+(a[2]/100000)+(a[1]/10000000)+(a[0]/1000000000)+0.2
        return score

    '''散牌情况'''
    score = 1+(a[4]/1000)+(a[3]/100000)+(a[2]/10000000)+(a[1]/1000000000)+(a[0]/100000000000)+0.1
    return score

def getTopScore():
    global currentshui1
    a = currentTopPoker[0].number
    b = currentTopPoker[1].number
    c = currentTopPoker[2].number
    if a == b and b == c:
        topScore = 4+((a+b+c)/1000)+0.4
    elif a == b:
        topScore = 2+((a+b)/1000)+c/10000+0.2
    elif b == c:
        topScore = 2+((b+c)/1000)+a/10000+0.2
    else:
        topScore = 1+(a+b+c)/10000+0.1
    currentshui1 = topScore-int(topScore)+1
    return topScore

def getMiddleScore():
    global currentshui2
    currentMiddlePoker.sort(key=getnumber)
    score = typeOfPokerCard(currentMiddlePoker)
    types = int(score)
    if types == 9:
        currentshui2 = score+1
    elif types == 8:
        currentshui2 = score
    elif types == 7:
        currentshui2 = score-5
    else:
        currentshui2 = score-int(score)+1
    return score

def getBottomScore():
    global currentshui3
    currentBottomPoker.sort(key=getnumber)
    score = typeOfPokerCard(currentBottomPoker)
    types = int(score)
    if types == 9:
        currentshui3 = score - 4
    elif types == 8:
        currentshui3 = score - 5
    else:
        currentshui3 = score-int(score)+1
    return score

def checkBestPoker():
    """计算头墩, 规则里面没说头墩有其他情况，我当然选择不做其他判断啦。:O(∩_∩)O~"""
    currentscore1 = getTopScore()
    '''计算中墩'''
    currentscore2 = getMiddleScore()
    '''计算底墩，只需在中墩基础上修改数值即可'''
    currentscore3 = getBottomScore()

    if currentscore1 <= currentscore2 <= currentscore3:
        ret = 0
        global shui1, shui2, shui3
        if currentshui1 > shui1:
            ret += int(currentshui1)
        elif currentshui1 < shui1:
            ret -= int(shui1)
        if currentshui2 > shui2:
            ret += int(currentshui2)
        elif currentshui2 < shui2:
            ret -= int(shui2)
        if currentshui3 > shui3:
            ret += int(currentshui3)
        elif currentshui3 < shui3:
            ret -= int(shui3)
        if ret > 0.0000001:
            shui1 = currentshui1
            shui2 = currentshui2
            shui3 = currentshui3
            for i in range(0, 5):
                middlePoker[i] = currentMiddlePoker[i]
                bottomPoker[i] = currentBottomPoker[i]
            for i in range(0, 3):
                topPoker[i] = currentTopPoker[i]

def getPokerCardTwo(n2, x2):
    for t in range(n2, 9):
        ans2[t] = 1
        currentMiddlePoker[x2] = wholePoker2[t]
        if x2 == 4:
            cnt2 = 0
            for j in range(0, 9):
                if ans2[j] == 0:
                    currentTopPoker[cnt2] = wholePoker2[j]  #剩下的牌就是前墩了
                    cnt2 += 1
            checkBestPoker()
        else:
            getPokerCardTwo(t+1, x2+1)
        ans2[t] = 0

def getPokerCardOne(n1, x1):
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
    '''前墩'''
    str = ""
    for i in range(0, 3):
        if i < 2:
            str += (numToColor(topPoker[i].color))+(numToPoker(topPoker[i].number))+' '
        else:
            str += (numToColor(topPoker[i].color))+(numToPoker(topPoker[i].number))
    print(str)
    lastPoker.append(str)

    '''中墩'''
    str = ""
    for i in range(0, 5):
        if i < 4:
            str += (numToColor(middlePoker[i].color)) + (numToPoker(middlePoker[i].number))+' '
        else:
            str += (numToColor(middlePoker[i].color)) + (numToPoker(middlePoker[i].number))
    print(str)
    lastPoker.append(str)

    '''后墩'''
    str = ""
    for i in range(0, 5):
        if i < 4:
            str += (numToColor(bottomPoker[i].color)) + (numToPoker(bottomPoker[i].number))+' '
        else:
            str += (numToColor(bottomPoker[i].color)) + (numToPoker(bottomPoker[i].number))
    print(str)
    lastPoker.append(str)
    return lastPoker


#login()
#startGame()


wholePoker1 = [pokerCard(1,2),pokerCard(1,3),pokerCard(1,4),pokerCard(1,5),pokerCard(1,6),pokerCard(1,7),pokerCard(1,8),pokerCard(1,9),pokerCard(1,10),pokerCard(1,11),pokerCard(1,12),pokerCard(1,13),pokerCard(1,14)]
'''冲冲冲，先拿三墩牌再说'''
getPokerCardOne(0, 0)

lastPoker = []
lastPoker = printPoker()
#submitGame()