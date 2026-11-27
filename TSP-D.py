import math  # 导入模块 math
import random  # 导入模块 random
import pandas as pd  # 导入模块 pandas 并简写成 pd
import numpy as np  # 导入模块 numpy 并简写成 np YouCans
import matplotlib.pyplot as plt  # 导入模块 matplotlib.pyplot 并简写成 plt
import time
import copy


# 子程序：读取TSPLib数据
def read_TSPLib(fileName):
    res = []
    with open(fileName, 'r') as fid:
        for item in fid:
            if len(item.strip()) != 0:
                res.append(item.split())
    loadData = np.array(res).astype('float')  # 数据格式：i Xi Yi
    coordinates = loadData[:, 1::]
    return coordinates


# 子程序：计算各城市间的距离，得到距离矩阵
def getDistMat(nCities, coordinates):
    max = 0
    distMat = np.zeros((nCities, nCities))  # 初始化距离矩阵
    for i in range(nCities):
        for j in range(i, nCities):
            # np.linalg.norm 求向量的范数（默认求 二范数），得到 i、j 间的距离
            distMat[i][j] = distMat[j][i] = round(np.linalg.norm(coordinates[i] - coordinates[j]))
            if distMat[i][j] > max:
                max = distMat[i][j]
    return distMat, max  # 城市间距离取整（四舍五入）


# 近邻表格
def getJinlin(nCities, num, distMat):
    Jinlindis = np.zeros((nCities, 1))  # 近邻距离，只有这个距离之内的可以被选择
    k = 0
    j = 0
    Jinlin = []
    for dis1 in distMat:
        discopy = dis1.copy()
        discopy.sort()
        Jinlindis[k] = discopy[num]  # 设置每个城市第num-1距离为半径
        k = k + 1
    for dis2 in distMat:
        pointset = []
        for i in range(0, nCities):
            if dis2[i] <= Jinlindis[j] and i != j:
                pointset.append(i)
        Jinlin.append(pointset)
        j = j + 1
    return Jinlin


# 子程序：计算 TSP 路径长度
def calTourMileage(tourGiven, nCities, distMat):
    # custom function caltourMileage(nCities, tour, distMat):
    # to compute mileage of the given tour
    mileageTour = distMat[tourGiven[nCities - 1], tourGiven[0]]  # dist((n-1),0)
    for i in range(nCities - 1):  # dist(0,1),...dist((n-2)(n-1))
        mileageTour += distMat[tourGiven[i], tourGiven[i + 1]]
    return round(mileageTour)  # 路径总长度取整（四舍五入）


# 子程序：绘制 TSP 路径图
def plot_tour(tour, value, coordinates):
    # custom function plot_tour(tour, nCities, coordinates)
    num = len(tour)
    x0, y0 = coordinates[tour[num - 1]]
    x1, y1 = coordinates[tour[0]]
    plt.scatter(int(x0), int(y0), s=15, c='r')  # 绘制城市坐标点 C(n-1)
    plt.plot([x1, x0], [y1, y0], c='b')  # 绘制旅行路径 C(n-1)~C(0)
    for i in range(num - 1):
        x0, y0 = coordinates[tour[i]]
        x1, y1 = coordinates[tour[i + 1]]
        plt.scatter(float(x0), float(y0), s=15, c='r')  # 绘制城市坐标点 C(i)
        plt.plot([x1, x0], [y1, y0], c='b')  # 绘制旅行路径 C(i)~C(i+1)
    plt.xlabel("Total mileage of the tour:{:.1f}".format(value))
    plt.title("Optimization tour of TSP{:d}".format(num))  # 设置图形标题
    plt.show()


def distroy1(tourNow, nCities, distMat, num):  # 贪心摧毁前num个
    LIST = []
    list = []
    mileageTour0 = distMat[tourNow[nCities - 1], tourNow[0]] + distMat[tourNow[0], tourNow[1]]
    list.append([tourNow[0], mileageTour0])
    for i in range(1, nCities - 1):
        mileageTour = distMat[tourNow[i - 1], tourNow[i]] + distMat[tourNow[i], tourNow[i + 1]]
        list.append([tourNow[i], mileageTour])
    mileageTour1 = distMat[tourNow[nCities - 2], tourNow[nCities - 1]] + distMat[tourNow[nCities - 1], tourNow[0]]
    list.append([tourNow[nCities - 1], mileageTour1])
    my_lest = sorted(list, key=lambda k: k[1], reverse=True)  # 二维坐标进行降序
    for j in range(num):
        LIST.append(my_lest[j][0])  # LIST是要拆除的坐标
    tourNew = []  # 这是初始解拆除LIST要拆除坐标后的解
    for l in range(nCities):
        if tourNow[l] not in LIST:
            tourNew.append(tourNow[l])
    return LIST, tourNew  # 返回的是拆除名单和出去拆除名单后的解


def distroy2(tourNow, nCities, num):  # 随机摧毁num个
    LIST = random.sample(range(nCities), num)
    tourNew = []  # 这是初始解拆除LIST要拆除坐标后的解
    for l in range(nCities):
        if tourNow[l] not in LIST:
            tourNew.append(tourNow[l])
    return LIST, tourNew  # 返回的是拆除名单和出去拆除名单后的解


def distroy3(tourNow, nCities, num):  # 随机摧毁num个连续城市
    LIST = []
    x = random.randint(0, nCities - 1)
    tourNow1 = []
    for i in range(nCities):
        tourNow1.append(tourNow[i])
    tourNow2 = tourNow1[x:] + tourNow1[:x]
    for j in range(num):
        LIST.append(tourNow2[j])
    tourNew = []  # 这是初始解拆除LIST要拆除坐标后的解
    for l in range(nCities):
        if tourNow[l] not in LIST:
            tourNew.append(tourNow[l])
    return LIST, tourNew  # 返回的是拆除名单和出去拆除名单后的解


def distroy4(tourNow, nCities, num, jinlin, Jinnum):  # 非近邻摧毁
    LIST = []
    x = random.randint(0, nCities - 1)
    if num > Jinnum:
        for ii in range(Jinnum):
            LIST.append(jinlin[tourNow[x]][ii])
        while True:
            y = random.randint(0, nCities - 1)
            if tourNow[y] not in LIST:
                LIST.append(tourNow[y])
                if len(LIST) == num:
                    break
    else:
        y = random.randint(0, nCities - 1)
        LIST1 = random.sample(range(Jinnum), num)
        for ii in range(num):
            LIST.append(jinlin[tourNow[x]][LIST1[ii]])
    tourNew = []  # 这是初始解拆除LIST要拆除坐标后的解
    for l in range(nCities):
        if tourNow[l] not in LIST:
            tourNew.append(tourNow[l])
    return LIST, tourNew


def repair1(LIST, tourNew, distMat, num):  # 噪声贪心修复
    tourstart = tourNew
    for i in range(num):
        value = []
        for j in range(len(tourstart) - 1):
            if j == 0:
                value1 = distMat[tourstart[j], LIST[i]] + distMat[tourstart[-1], LIST[i]] - distMat[
                    tourstart[-1], tourstart[j]]
                value.append(value1)
            else:
                value1 = distMat[tourstart[j], LIST[i]] + distMat[tourstart[j - 1], LIST[i]] - distMat[
                    tourstart[j - 1], tourstart[j]]
                value.append(value1)
        bestvalue = min(value)
        position = value.index(bestvalue)
        tourstart.insert(position, LIST[i])
    return tourstart


def repair2(LIST, tourNew, num, jinlin):  # k近邻修复
    tourNow1 = []
    for i in range(len(tourNew)):
        tourNow1.append(tourNew[i])
    for j in range(num):
        x = LIST[j]
        n = 0
        while True:
            n = n + 1
            y = random.sample(jinlin[x], 1)
            if y in tourNow1:
                break
            if n > 20:
                zindex = random.randint(0, len(tourNew) - 1)
                y = tourNew[zindex]
                break
        yindex = tourNow1.index(y)
        tourNow1.insert(yindex, LIST[j])
    return tourNow1


def repair3(LIST, tourNew, distMat, num, u, temp_max):  # 噪声贪心修复，u表示噪音系数
    tourstart = tourNew
    for i in range(num):
        value = []
        for j in range(len(tourstart) - 1):
            r3 = random.random()
            if j == 0:
                value1 = distMat[tourstart[j], LIST[i]] + distMat[tourstart[-1], LIST[i]] - distMat[
                    tourstart[-1], tourstart[j]] + temp_max * (2 * r3 - 1) * u
                value.append(value1)
            else:
                value1 = distMat[tourstart[j], LIST[i]] + distMat[tourstart[j - 1], LIST[i]] - distMat[
                    tourstart[j - 1], tourstart[j]] + temp_max * (2 * r3 - 1) * u
                value.append(value1)
        bestvalue = min(value)
        position = value.index(bestvalue)
        tourstart.insert(position, LIST[i])
    return tourstart


def creatT(Tlength, nCities, distMat, nummax, jinlin, Jinnum, temp_max):  # 创建初始解和初始温度，初始列表用两倍长度以去除噪声
    gapgroup = []
    tourNow = np.random.permutation(nCities)
    valueNow = calTourMileage(tourNow, nCities, distMat)
    while True:
        r1 = random.uniform(0, 1)  # r1控制破坏
        r2 = random.uniform(0, 1)  # r2控制修复
        num = random.randint(int(2 / nummax), nummax)  # 破坏点的个数(不改了，效果不大)
        u = 0.1
        if r1 <= 0.25:
            LIST, tourNew = distroy1(tourNow, nCities, distMat, num)
        elif r1 > 0.25 and r1 <= 0.5:
            LIST, tourNew = distroy2(tourNow, nCities, num)
        elif r1 > 0.5 and r1 <= 0.75:
            LIST, tourNew = distroy3(tourNow, nCities, num)
        else:
            LIST, tourNew = distroy4(tourNow, nCities, num, jinlin, Jinnum)
        if r2 < 0.5:
            tourNew = repair1(LIST, tourNew, distMat, num)
        else:
            tourNew = repair3(LIST, tourNew, distMat, num, u, temp_max)
        valueNew = calTourMileage(tourNew, nCities, distMat)
        if valueNew <= valueNow:
            tourNow = tourNew
            valueNow = valueNew
        else:
            gap = valueNew - valueNow
            tourNow = tourNew
            valueNow = valueNew
            gapgroup.append(gap)
            gapgrouplength = len(gapgroup)
            if gapgrouplength >= Tlength * 3:
                break
    gapgroup.sort()
    TT = gapgroup[int(2 * Tlength):int(3 * Tlength)]
    TT.sort()
    return TT, tourNow, valueNow


def caculatetour(result, Vtruck, Vfly, SR, SL, result1length, distMat):
    result2 = result[1]
    result1 = result[0]
    L1 = 0  # 飞行距离
    L2 = 0  # 卡车距离
    flynum = 0
    flylastpoint = result1[0]
    trucklastpoint = result1[0]
    timetotal = 0
    for i in range(1, result1length):
        if result2[i] == 1:
            flynum = flynum + 1
            L1 = L1 + distMat[result1[i], flylastpoint]
            flylastpoint = result1[i]
        elif result2[i] == 2:
            L2 = L2 + distMat[result1[i], trucklastpoint]
            trucklastpoint = result1[i]
        elif result2[i] == 0:
            if flynum > 0:
                L1 = L1 + distMat[result1[i], flylastpoint]
                time1 = L1 / Vfly + SR + SL  # 飞行时间
            else:
                time1 = 0  # 飞行时间
            L2 = L2 + distMat[result1[i], trucklastpoint]
            trucklastpoint = result1[i]
            flylastpoint = result1[i]
            if flynum > 0:
                time2 = L2 / Vtruck + SR + SL  # 卡车时间
                flynum = 0
            else:
                time2 = L2 / Vtruck
            time3 = max(time1, time2)
            timetotal = timetotal + time3
            L2 = 0
            L1 = 0
    return timetotal


def fstspdestroy1(tournow1, distMat, UAV_endurance, negativepoint1, result1length, u2, temp_max):
    tournow = copy.deepcopy(tournow1)
    negativepoint = copy.deepcopy(negativepoint1)
    result = tournow[:]
    result2 = result[1]
    result1 = result[0]
    LIST1 = []
    LIST2 = []
    for pos in range(1, result1length - 1):
        if result1[pos] not in negativepoint and result1[pos + 1] not in negativepoint and result1[
            pos - 1] not in negativepoint:
            r3 = random.random()
            r = 2 * r3 - 1
            posindex = result[0].index(result1[pos])
            # mileageTour = distMat[result1[posindex-1], result1[posindex]]+distMat[result1[posindex], result1[posindex+1]]-distMat[result1[posindex-1], result1[posindex+1]]
            mileageTour = u2 * r * temp_max + distMat[result1[posindex - 1], result1[posindex]] + distMat[
                result1[posindex], result1[posindex + 1]] - distMat[result1[posindex - 1], result1[posindex + 1]]
            if distMat[result1[posindex - 1], result1[posindex]] + distMat[
                result1[posindex], result1[posindex + 1]] <= UAV_endurance:
                LIST1.append([result1[posindex], mileageTour])
    my_lest = sorted(LIST1, key=lambda k: k[1], reverse=True)  # 二维坐标进行降序
    #  print(my_lest)
    if len(my_lest) >= 1:
        point = my_lest[0][0]
        pointindex = result[0].index(point)
        startpoint_index = pointindex - 1
        endpoint_index = pointindex + 1
        LIST2.append(point)
        while True:
            if result1[endpoint_index] in negativepoint:
                endd = 10000000000
            else:
                endd = distMat[result1[endpoint_index], result1[pointindex]]
            if result1[startpoint_index] in negativepoint:
                startd = 1000000000000
                if endd == 10000000000:
                    break
            else:
                startd = distMat[result1[startpoint_index], result1[pointindex]]
            if endd <= startd:  # 向后添加
                d = 0
                for i in range(endpoint_index - startpoint_index + 1):
                    d = d + distMat[result1[startpoint_index + i], result1[startpoint_index + i + 1]]
                if d <= UAV_endurance:
                    LIST2.append(result1[endpoint_index])
                    endpoint_index = endpoint_index + 1
                else:
                    break
            else:
                d = 0
                for i in range(endpoint_index - startpoint_index + 1):
                    d = d + distMat[result1[startpoint_index + i - 1], result1[startpoint_index + i]]
                if d <= UAV_endurance:
                    LIST2.append(result1[startpoint_index])
                    startpoint_index = startpoint_index - 1
                else:
                    break
        for j in range(result1length):
            if result1[j] in LIST2:
                result2[j] = 1
                negativepoint.append(result1[j])
        negativepoint.append(result1[startpoint_index])  # 起飞降落点都要放在禁飞列表中
        negativepoint.append(result1[endpoint_index])
    else:
        point = 0
        LIST2 = []  # 一个满足条件起飞的点都没有
        startpoint_index, endpoint_index = 0, 0
        pointindex = 0
    result = [result1, result2]
    return result, negativepoint, startpoint_index, endpoint_index, point


def fstspdestroy2(startpoint_index, endpoint_index, result):  # 翻转扰动1变2,2变1
    result2 = result[1].copy()
    if endpoint_index - startpoint_index > 2:
        x1_index = random.randint(startpoint_index + 1, endpoint_index - 1)
        if result2[x1_index] == 1:
            result2[x1_index] = 2
        elif result2[x1_index] == 2:
            result2[x1_index] = 1
    elif endpoint_index - startpoint_index == 2:
        if result2[startpoint_index + 1] == 1:
            result2[startpoint_index + 1] = 2
        elif result2[startpoint_index + 1] == 2:
            result2[startpoint_index + 1] = 1
    result_1 = [result[0], result2]
    return result_1


def fstspdestroy3(startpoint_index, endpoint_index, result):  # 反转插入交换
    result2 = result[1].copy()
    if endpoint_index - startpoint_index == 3:  # 中间只有两个，那只能交换
        gap = result2[startpoint_index + 1]
        result2[startpoint_index + 1] = result2[endpoint_index - 1]
        result2[endpoint_index - 1] = gap
    elif endpoint_index - startpoint_index > 3:
        rd3 = random.random()
        # print(rd3)
        if rd3 <= 0.3:  # 交换
            x1_index = random.randint(startpoint_index + 1, endpoint_index - 1)
            while True:
                x2_index = random.randint(startpoint_index + 1, endpoint_index - 1)
                if x1_index != x2_index:
                    break
            gap = result2[x1_index]
            result2[x1_index] = result2[x2_index]
            result2[x2_index] = gap
        elif rd3 > 0.3 and rd3 <= 0.7:  # 反转
            x1_index = random.randint(startpoint_index + 1, endpoint_index - 1)
            while True:
                x2_index = random.randint(startpoint_index + 1, endpoint_index - 1)
                if x1_index != x2_index:
                    break
            nn = min([x1_index, x2_index])
            xx = max([x1_index, x2_index])
            gap = result2[nn:xx + 1]
            gap1 = gap[::-1]  # 片段反转
            result2[nn:xx + 1] = gap1
        else:  # 插入
            x1_index = random.randint(startpoint_index + 1, endpoint_index - 1)
            while True:
                x2_index = random.randint(startpoint_index + 1, endpoint_index - 1)
                if x1_index != x2_index:
                    break
            gap = result2[x1_index]
            del result2[x1_index]
            result2.insert(x2_index, gap)
    result_1 = [result[0], result2]
    return result_1


def fstspdestroy4(startpoint_index, endpoint_index, result, distMat, UAV_endurance, negativepoint, result1length):
    result2 = result[1].copy()
    result1 = result[0]
    rd4 = random.random()
    jud = 0
    H = 0
    Q = 0
    if rd4 < 0.5:  # 向后
        while True:
            if endpoint_index == result1length - 1:
                break
            else:
                H = 1
                jud = 1
                if rd4 < 0.25:
                    result2[endpoint_index] = 2
                else:
                    result2[endpoint_index] = 1
                break
    else:
        while True:
            if startpoint_index == 0:
                break
            else:
                Q = 1
                jud = 1
                if rd4 < 0.75:
                    result2[startpoint_index] = 2
                else:
                    result2[startpoint_index] = 1
                break
    if jud == 1:
        flynum = 0
        flylastpoint = result1[0]
        L1 = 0  # 飞行距离
        for i in range(1, result1length):
            if result2[i] == 1:
                flynum = flynum + 1
                L1 = L1 + distMat[result1[i], flylastpoint]
                flylastpoint = result1[i]
            elif result2[i] == 0:
                if flynum > 0:
                    L1 = L1 + distMat[result1[i], flylastpoint]
                    if L1 > UAV_endurance:
                        jud = 0
                    flynum = 0
                    flylastpoint = result1[i]
                    L1 = 0
                else:
                    flynum = 0
                    flylastpoint = result1[i]
                    L1 = 0
    if jud == 0:
        Q = 0
        H = 0
        result_1 = result
    else:
        if H == 1:
            result_1 = [result[0], result2]
        elif Q == 1:
            result_1 = [result[0], result2]
    return result_1, jud, H, Q, startpoint_index, endpoint_index


def caculatetour1(result, Vtruck, Vfly, SR, SL, result1length, distMat, UAV_endurance):
    result1 = result[0]  # TSP路径
    result2 = result[1]
    L1 = 0  # 无人机1飞行距离
    L2 = 0  # 无人机2飞行距离
    L3 = 0  # 无人机3飞行距离
    fly1num = 0  # 无人机1段内服务点
    fly2num = 0  # 无人机2段内服务点
    fly3num = 0  # 无人机3段内服务点
    fly1lastpoint = result1[0]
    fly2lastpoint = result1[0]
    fly3lastpoint = result1[0]
    trucklastpoint = result1[0]
    T1 = 0  # 无人机1到达时间
    T2 = 0  # 无人机2到达时间
    T3 = 0  # 卡车到达时间
    T4 = 0  # 无人机4到达时间
    judge = 1  # 判断解是不是可行的
    for i in range(1, result1length):
        if result2[i] % 2 == 1:  # 为奇数
            if result2[i] == 1:
                T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck)
                trucklastpoint = result1[i]
            else:
                if result2[i] == 3:  # 无人机1和卡车汇合
                    if fly1num >= 1:
                        L1 = L1 + distMat[result1[i], fly1lastpoint]
                        if L1 > UAV_endurance:
                            judge = 0
                        T1 = T1 + L1 / Vfly + SL + SR
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR
                    else:
                        T1 = T1 + (distMat[result1[i], trucklastpoint] / Vtruck)
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck)
                    Tmax = max(T1, T3)
                    T1 = Tmax
                    T3 = Tmax
                    L1 = 0
                    fly1num = 0
                    trucklastpoint = result1[i]
                    fly1lastpoint = result1[i]
                elif result2[i] == 5:  # 无人机2和卡车汇合
                    if fly2num >= 1:
                        L2 = L2 + distMat[result1[i], fly2lastpoint]
                        T2 = T2 + L2 / Vfly + SL + SR
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR
                        if L2 > UAV_endurance:
                            judge = 0
                    else:
                        T2 = T2
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck)
                    Tmax = max(T2, T3)
                    T2 = Tmax
                    T3 = Tmax
                    L2 = 0
                    fly2num = 0
                    trucklastpoint = result1[i]
                    fly2lastpoint = result1[i]
                elif result2[i] == 7:
                    if fly1num >= 1 and fly2num >= 1:
                        L1 = L1 + distMat[result1[i], fly1lastpoint]
                        T1 = T1 + L1 / Vfly + SL + SR
                        L2 = L2 + distMat[result1[i], fly2lastpoint]
                        T2 = T2 + L2 / Vfly + SL + SR
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR + SL + SR
                        Tmax = max(T1, T2, T3)
                    elif fly1num >= 1 and fly2num == 0:
                        L1 = L1 + distMat[result1[i], fly1lastpoint]
                        T1 = T1 + L1 / Vfly + SL + SR
                        T2 = T2
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR
                        Tmax = max(T1, T3)
                    elif fly1num == 0 and fly2num >= 1:
                        T1 = T1
                        L2 = L2 + distMat[result1[i], fly2lastpoint]
                        T2 = T2 + L2 / Vfly + SL + SR
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR
                        Tmax = max(T2, T3)
                    else:
                        T1 = T1
                        T2 = T2
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck)
                        Tmax = max(T1, T2, T3)
                    if L1 > UAV_endurance or L2 > UAV_endurance:
                        judge = 0
                    T1 = Tmax
                    T2 = Tmax
                    T3 = Tmax
                    L1 = 0
                    L2 = 0
                    fly1num = 0
                    fly2num = 0
                    trucklastpoint = result1[i]
                    fly1lastpoint = result1[i]
                    fly2lastpoint = result1[i]
                elif result2[i] == 9:
                    if fly3num >= 1:
                        L3 = L3 + distMat[result1[i], fly3lastpoint]
                        T4 = T4 + L3 / Vfly + SL + SR
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR
                        if L3 > UAV_endurance:
                            judge = 0
                    else:
                        T4 = T4
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck)
                    Tmax = max(T3, T4)
                    T4 = Tmax
                    T3 = Tmax
                    L3 = 0
                    fly3num = 0
                    trucklastpoint = result1[i]
                    fly3lastpoint = result1[i]
                elif result2[i] == 11:
                    if fly1num >= 1 and fly3num >= 1:
                        L1 = L1 + distMat[result1[i], fly1lastpoint]
                        T1 = T1 + L1 / Vfly + SL + SR
                        L3 = L3 + distMat[result1[i], fly3lastpoint]
                        T4 = T4 + L3 / Vfly + SL + SR
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR + SL + SR
                        Tmax = max(T1, T3, T4)
                    elif fly1num >= 1 and fly3num == 0:
                        L1 = L1 + distMat[result1[i], fly1lastpoint]
                        T1 = T1 + L1 / Vfly + SL + SR
                        T4 = T4
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR
                        Tmax = max(T1, T3)
                    elif fly1num == 0 and fly3num >= 1:
                        T1 = T1
                        L3 = L3 + distMat[result1[i], fly3lastpoint]
                        T4 = T4 + L3 / Vfly + SL + SR
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR
                        Tmax = max(T3, T4)
                    else:
                        T1 = T1
                        T4 = T4
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck)
                        Tmax = max(T1, T3, T4)
                    if L1 > UAV_endurance or L3 > UAV_endurance:
                        judge = 0
                    T1 = Tmax
                    T3 = Tmax
                    T4 = Tmax
                    L1 = 0
                    L3 = 0
                    fly1num = 0
                    fly3num = 0
                    trucklastpoint = result1[i]
                    fly1lastpoint = result1[i]
                    fly3lastpoint = result1[i]
                elif result2[i] == 13:
                    if fly2num >= 1 and fly3num >= 1:
                        L2 = L2 + distMat[result1[i], fly2lastpoint]
                        T2 = T2 + L2 / Vfly + SL + SR
                        L3 = L3 + distMat[result1[i], fly3lastpoint]
                        T4 = T4 + L3 / Vfly + SL + SR
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR + SL + SR
                        Tmax = max(T2, T3, T4)
                    elif fly2num >= 1 and fly3num == 0:
                        L2 = L2 + distMat[result1[i], fly2lastpoint]
                        T2 = T2 + L2 / Vfly + SL + SR
                        T4 = T4
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR
                        Tmax = max(T2, T3)
                    elif fly2num == 0 and fly3num >= 1:
                        T2 = T2
                        L3 = L3 + distMat[result1[i], fly3lastpoint]
                        T4 = T4 + L3 / Vfly + SL + SR
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR
                        Tmax = max(T3, T4)
                    else:
                        T2 = T2
                        T4 = T4
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck)
                        Tmax = max(T2, T3, T4)
                    if L2 > UAV_endurance or L3 > UAV_endurance:
                        judge = 0
                    T2 = Tmax
                    T3 = Tmax
                    T4 = Tmax
                    L2 = 0
                    L3 = 0
                    fly2num = 0
                    fly3num = 0
                    trucklastpoint = result1[i]
                    fly2lastpoint = result1[i]
                    fly3lastpoint = result1[i]
                elif result2[i] == 15:
                    if fly1num >= 1 and fly2num >= 1 and fly3num >= 1:
                        L1 = L1 + distMat[result1[i], fly1lastpoint]
                        T1 = T1 + L1 / Vfly + SL + SR
                        L2 = L2 + distMat[result1[i], fly2lastpoint]
                        T2 = T2 + L2 / Vfly + SL + SR
                        L3 = L3 + distMat[result1[i], fly3lastpoint]
                        T4 = T4 + L3 / Vfly + SL + SR
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR + SL + SR + SL + SR
                        Tmax = max(T1, T2, T3, T4)
                    elif fly1num == 0 and fly2num >= 1 and fly3num >= 1:
                        T1 = T1
                        L2 = L2 + distMat[result1[i], fly2lastpoint]
                        T2 = T2 + L2 / Vfly + SL + SR
                        L3 = L3 + distMat[result1[i], fly3lastpoint]
                        T4 = T4 + L4 / Vfly + SL + SR
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR + SL + SR
                        Tmax = max(T2, T3, T4)
                    elif fly1num >= 1 and fly2num == 0 and fly3num >= 1:
                        L1 = L1 + distMat[result1[i], fly1lastpoint]
                        T1 = T1 + L1 / Vfly + SL + SR
                        T2 = T2
                        L3 = L3 + distMat[result1[i], fly3lastpoint]
                        T4 = T4 + L3 / Vfly + SL + SR
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR + SL + SR
                        Tmax = max(T1, T3, T4)
                    elif fly1num >= 1 and fly2num >= 1 and fly3num == 0:
                        L1 = L1 + distMat[result1[i], fly1lastpoint]
                        T1 = T1 + L1 / Vfly + SL + SR
                        L2 = L2 + distMat[result1[i], fly2lastpoint]
                        T2 = T2 + L2 / Vfly + SL + SR
                        T4 = T4
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR + SL + SR
                        Tmax = max(T1, T2, T3)
                    else:
                        T1 = T1
                        T2 = T2
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck)
                        T4 = T4
                        Tmax = T3
                    if L1 > UAV_endurance or L2 > UAV_endurance or L3 > UAV_endurance:
                        judge = 0
                    T1 = Tmax
                    T2 = Tmax
                    T3 = Tmax
                    T4 = Tmax
                    L1 = 0
                    L2 = 0
                    L3 = 0
                    fly1num = 0
                    fly2num = 0
                    fly3num = 0
                    trucklastpoint = result1[i]
                    fly1lastpoint = result1[i]
                    fly2lastpoint = result1[i]
                    fly3lastpoint = result1[i]
        else:
            if result2[i] == 2:
                L1 = L1 + distMat[result1[i], fly1lastpoint]
                fly1num = fly1num + 1
                fly1lastpoint = result1[i]
            elif result2[i] == 4:
                L2 = L2 + distMat[result1[i], fly2lastpoint]
                fly2num = fly2num + 1
                fly2lastpoint = result1[i]
            elif result2[i] == 8:
                L3 = L3 + distMat[result1[i], fly3lastpoint]
                fly3num = fly3num + 1
                fly3lastpoint = result1[i]
    return T1, judge


def caculatetour2(result, Vtruck, Vfly, SR, SL, result1length, distMat, UAV_endurance):
    result1 = result[0]  # TSP路径
    result2 = result[1]
    L1 = 0  # 无人机1飞行距离
    fly1num = 0  # 无人机1段内服务点
    fly1lastpoint = result1[0]
    trucklastpoint = result1[0]
    T1 = 0  # 无人机1到达时间
    T3 = 0  # 卡车到达时间
    judge = 1  # 判断解是不是可行的
    for i in range(1, result1length):
        if result2[i] % 2 == 1:  # 为奇数
            if result2[i] == 1:
                T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck)
                trucklastpoint = result1[i]
            else:
                if result2[i] == 3:  # 无人机1和卡车汇合
                    if fly1num == 1:
                        L1 = L1 + distMat[result1[i], fly1lastpoint]
                        if L1 > UAV_endurance:
                            judge = 0
                        T1 = T1 + L1 / Vfly + SL + SR
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR
                    elif fly1num > 1:
                        L1 = L1 + distMat[result1[i], fly1lastpoint]
                        T1 = T1 + L1 / Vfly + SL + SR
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck) + SL + SR
                        judge = 0
                    else:
                        T1 = T1 + (distMat[result1[i], trucklastpoint] / Vtruck)
                        T3 = T3 + (distMat[result1[i], trucklastpoint] / Vtruck)
                    Tmax = max(T1, T3)
                    T1 = Tmax
                    T3 = Tmax
                    L1 = 0
                    fly1num = 0
                    trucklastpoint = result1[i]
                    fly1lastpoint = result1[i]
        else:
            if result2[i] == 2:
                L1 = L1 + distMat[result1[i], fly1lastpoint]
                fly1num = fly1num + 1
                fly1lastpoint = result1[i]
    return T3, judge


def raodong_fenpei1(tournow, result1length):
    tour = copy.deepcopy(tournow)
    x1_index = random.randint(1, result1length - 1)
    if tour[1][x1_index] == 2:
        tour[1][x1_index] = 1
    elif tour[1][x1_index] == 1:
        tour[1][x1_index] = 2
    return tour


def local_raodong(tournow, result1length):
    i = random.randint(1, result1length - 2)  # 产生第一个 [0,n) 区间内的随机整数
    while True:
        j = random.randint(1, result1length - 2)
        if i != j: break  # 保证 i, j 不相等
    tour = copy.deepcopy(tournow)
    r = random.random()
    if r > 0.5:
        tour[1][i], tour[1][j] = tournow[1][j], tournow[1][i]  # 交换 城市 i 和 j 的位置————简洁的实现方法
    else:
        nn = min([i, j])
        xx = max([i, j])
        gap = tournow[1][nn:xx + 1]
        gap1 = gap[::-1]  # 片段反转
        tour[1][nn:xx + 1] = gap1
    return tour


# 子程序：初始化模拟退火算法的控制参数
def initParameter():
    nMarkov = 60  # Markov链长度，也即内循环运行次数
    Maxinter = 150  # 外循环次数
    Tlength = 35  # 温度列表长度
    Jinnum = 20  # 近邻表参数
    nummax = 25  # 破坏长度上限
    u = 0.1  # 第一阶段噪声系数
    u2 = 0  # 第二阶段噪声系数
    UAV_endurance = 950
    SR = 1
    SL = 1
    Vfly = 1.5
    Vtruck = 1
    return nMarkov, Maxinter, Jinnum, Tlength, nummax, u, UAV_endurance, SR, SL, Vfly, Vtruck, u2


def main():
    start = time.time()
    coordinates = read_TSPLib('kroA100.txt')  # 案例点的坐标
    nMarkov, Maxinter, Jinnum, Tlength, nummax, u, UAV_endurance, SR, SL, Vfly, Vtruck, u2 = initParameter()  # 调用子程序，获得设置参数                                                      #近邻系数
    nCities = coordinates.shape[0]  # 根据输入的城市坐标 获得城市数量 nCities
    distMat, temp_max = getDistMat(nCities, coordinates)
    # print(distMat)
    jinlin = getJinlin(nCities, Jinnum, distMat)  # 制作近邻表
    TT, tourNow, valueNow = creatT(Tlength, nCities, distMat, nummax, jinlin, Jinnum, temp_max)
    recordBest = []  # 初始化 最优路径记录表
    recordNow = []  # 初始化 最优路径记录表
    tourBest = tourNow
    valueBest = valueNow
    BEST = []
    BEST.append(tourBest)
    pd1 = 0.25
    pd2 = 0.25
    pd3 = 0.25
    pd4 = 0.25
    pr1 = 0.5
    pr3 = 0.5
    for wai in range(Maxinter):
        tNow = TT[Tlength - 1]
        Tc = []
        timed1 = 0
        timed2 = 0
        timed3 = 0
        timed4 = 0
        timer1 = 0
        timer3 = 0
        sd1 = 0
        sd2 = 0
        sd3 = 0
        sd4 = 0
        sr1 = 0
        sr3 = 0
        n = 0
        while n < nMarkov:
            n = n + 1
            r1 = random.uniform(0, pd1 + pd2 + pd3 + pd4)  # r1控制破坏
            r2 = random.uniform(0, pr1 + pr3)  # r2控制修复
            num = random.randint(int(nummax / 4), nummax)
            if r1 < pd1:  # 五种破坏算子
                LIST, tourNew = distroy1(tourNow, nCities, distMat, num)
                timed1 = timed1 + 1
            elif r1 < pd2 + pd1 and r1 >= pd1:
                LIST, tourNew = distroy2(tourNow, nCities, num)
                timed2 = timed2 + 1
            elif r1 < pd3 + pd2 + pd1 and r1 >= pd2 + pd1:
                LIST, tourNew = distroy3(tourNow, nCities, num)
                timed3 = timed3 + 1
            else:
                LIST, tourNew = distroy4(tourNow, nCities, num, jinlin, Jinnum)
                timed4 = timed4 + 1
            random.shuffle(LIST)
            if r2 < pr1:
                tourNew = repair1(LIST, tourNew, distMat, num)
                timer1 = timer1 + 1
            else:
                tourNew = repair3(LIST, tourNew, distMat, num, u, temp_max)
                timer3 = timer3 + 1
            valueNew = calTourMileage(tourNew, nCities, distMat)
            deltaE = valueNew - valueNow
            if valueNew <= valueNow:
                if r1 < pd1:  # 五种破坏算子
                    sd1 = sd1 + 1
                elif r1 < pd2 + pd1 and r1 >= pd1:
                    sd2 = sd2 + 1
                elif r1 < pd3 + pd2 + pd1 and r1 >= pd2 + pd1:
                    sd3 = sd3 + 1
                else:
                    sd4 = sd4 + 1
                if r2 < pr1:
                    sr1 = sr1 + 1
                else:
                    sr3 = sr3 + 1
                accept = True
                if valueNew < valueBest:
                    if r1 < pd1:  # 五种破坏算子
                        sd1 = sd1 + 2
                    elif r1 < pd2 + pd1 and r1 >= pd1:
                        sd2 = sd2 + 2
                    elif r1 < pd3 + pd2 + pd1 and r1 >= pd2 + pd1:
                        sd3 = sd3 + 2
                    else:
                        sd4 = sd4 + 2
                    if r2 < pr1:
                        sr1 = sr1 + 2
                    else:
                        sr3 = sr3 + 2
                    BEST.append(tourNew)
                    tourBest = tourNew
                    valueBest = valueNew
            else:
                pAccept = math.exp(-deltaE / tNow)
                pp = random.random()
                if pAccept > pp:
                    Tc.append(-deltaE / math.log(pp))
                    accept = True
                else:
                    accept = False
            # 保存新解
            if accept == True:  # 如果接受新解，则将新解保存为当前解
                tourNow = tourNew
                valueNow = valueNew
                if r1 < pd1:  # 五种破坏算子
                    sd1 = sd1 + 1
                elif r1 < pd2 + pd1 and r1 >= pd1:
                    sd2 = sd2 + 1
                elif r1 < pd3 + pd2 + pd1 and r1 >= pd2 + pd1:
                    sd3 = sd3 + 1
                else:
                    sd4 = sd4 + 1
                if r2 < pr1:
                    sr1 = sr1 + 1
                else:
                    sr3 = sr3 + 1
        Tclength = len(Tc)
        all = 0
        if Tclength != 0:  # 温度表的更新
            Tc.sort()
            #    Tavg=Tc[-1]
            for i in range(Tclength):
                all = all + Tc[i]
            Tavg = (all / Tclength)
            TT.pop()
            TT.append(Tavg)
            TT.sort()
        sdall = sd1 / (timed1 + 0.001) + sd2 / (0.001 + timed2) + sd3 / (0.001 + timed3) + sd4 / (
                    timed4 + 0.001)  # 概率动态调整
        srall = sr1 / (timer1 + 0.001) + sr3 / (timer3 + 0.001)
        pd1 = pd1 * 0.7 + (sd1 / (timed1 + 0.001)) / (0.001 + sdall) * 0.3
        pd2 = pd2 * 0.7 + (sd2 / (0.001 + timed2)) / (0.001 + sdall) * 0.3
        pd3 = pd3 * 0.7 + (sd3 / (0.001 + timed3)) / (0.001 + sdall) * 0.3
        pd4 = pd4 * 0.7 + (sd4 / (timed4 + 0.001)) / (0.001 + sdall) * 0.3
        pr1 = pr1 * 0.7 + (sr1 / (0.001 + timer1)) / (srall + 0.001) * 0.3
        pr3 = pr3 * 0.7 + (sr3 / (0.001 + timer3)) / (srall + 0.001) * 0.3
        recordBest.append(valueBest)
        recordNow.append(valueNow)  # 将当前路径长度追加到 当前路径记录表
        # SL.append(valueBest)
        print(
            f'求解{wai}次温度为{tNow}历史最优结果为 {valueBest} {valueNow}   {pd1}  {pd2}  {pd3} {pd4}  {pr1}  {pr3}        ')
    zero_index = tourBest.index(0)
    resultTSP = tourBest[zero_index:] + tourBest[:zero_index]
    result1 = resultTSP + [0]  # 第一层编码
    result1length = len(result1)
    result2 = [0] * result1length
    tournow = [result1, result2]  # FSTSP的编码
    valuenow = caculatetour(tournow, Vtruck, Vfly, SR, SL, result1length, distMat)
    negativepoint = [0]  # 不允许起飞降落的城市

    # 新的贪心分段策略
    start = 0
    i = 1
    while i < result1length:
        # 尝试从start开始，构建一个无人机段
        # 初始化当前段的终点为start
        end = start
        # 从start+1开始，尝试将点加入当前段
        for j in range(start + 1, result1length):
            # 计算从start到j的路径距离
            path_dist = 0
            for k in range(start, j):
                path_dist += distMat[result1[k], result1[k + 1]]
            # 如果路径距离不超过无人机航程，则更新end为j
            if path_dist <= UAV_endurance:
                end = j
            else:
                break

        # 如果end大于start，则构建一个无人机段
        if end > start:
            # 将start+1到end-1的点标记为无人机服务点（2）
            for k in range(start + 1, end):
                result2[k] = 2
            # 将起点和终点加入negativepoint
            negativepoint.append(result1[start])
            negativepoint.append(result1[end])
            # 更新start为end，开始下一段
            start = end
            i = end + 1
        else:
            # 否则，将当前点i标记为卡车点，并移动start到i
            start = i
            i += 1

    # 更新tournow[1]为新的result2
    tournow[1] = result2
    # 重新计算当前路径的时间
    valuenow = caculatetour(tournow, Vtruck, Vfly, SR, SL, result1length, distMat)

    # 记录当前最优
    tourbest = copy.deepcopy(tournow)
    valuebest = valuenow

    negativepoint = [0]  # 不允许起飞降落的城市
    n = 0
    tourbest = copy.deepcopy(tournow)
    valuebest = valuenow
    # 新的分段策略：贪心分段，应分尽分
    start = 0
    i = 1
    while i < result1length:
        # 如果当前点已经是negativepoint，则跳过，不能作为无人机段的起点（但实际上，我们是从卡车点开始，所以起点不会是negativepoint）
        # 我们尝试从start开始，构建一个无人机段
        # 初始化当前段的无人机飞行距离为0
        flight_distance = 0
        j = i
        # 记录当前段的最后一个点，初始为start
        last_point = start
        # 尝试将j作为当前段的终点（卡车点）
        while j < result1length:
            # 计算从last_point到j的距离，并加到flight_distance
            # 注意：如果last_point是起点，那么无人机从起点飞到j（如果j是终点，那么无人机从j-1飞到j，然后从j飞回起点？不对，我们重新考虑）
            # 实际上，我们考虑的是从start到j的路径，中间点（start+1到j-1）由无人机服务，那么无人机飞行距离为：
            #   dist(start, start+1) + dist(start+1, start+2) + ... + dist(j-1, j) + dist(j, start)
            # 但是，这样计算的是无人机从起点出发，依次访问中间点，然后从最后一个中间点飞到终点，然后从终点飞回起点？不对，无人机是返回到终点（卡车点），所以不需要从终点飞回起点。
            # 正确飞行距离：无人机从起点（卡车点）起飞，依次访问中间点，然后飞到终点（卡车点）。所以，飞行距离为：
            #   dist(start, start+1) + dist(start+1, start+2) + ... + dist(j-1, j)
            # 但是，这样计算的是从起点到终点的路径距离，不包括返回起点。因为无人机在终点与卡车汇合。

            # 所以，我们计算从start到j的路径距离（即依次经过start, start+1, ..., j-1, j的路径距离），但是，起点和终点都是卡车点，所以无人机飞行的距离就是这整个路径的距离。
            # 但是，注意：起点和终点都是卡车点，所以无人机飞行距离应该是路径上所有边的距离之和，即从start到j的路径距离。

            # 计算从start到j的路径距离
            path_dist = 0
            for k in range(start, j):
                path_dist += distMat[result1[k], result1[k + 1]]
            # 如果这个距离小于等于UAV_endurance，那么我们可以将j作为终点
            if path_dist <= UAV_endurance:
                # 更新j，继续向后尝试
                j += 1
            else:
                break

        # 此时，j是第一个使得路径距离超过UAV_endurance的点，所以我们可以将j-1作为终点
        end = j - 1

        # 如果end大于start，那么我们可以构建一个从start到end的无人机段
        if end > start:
            # 将start+1到end-1的点标记为无人机服务点（2）
            for k in range(start + 1, end):
                result2[k] = 2
            # 将start和end点标记为卡车服务点，并且是起降点（3）
            # 注意：原程序后续会将2改为1，0改为3，所以我们这里先标记为2和0，后面再统一转换
            # 但是，我们后续有转换步骤，所以这里先按照原来的方式：无人机服务点标记为2，卡车点标记为0（起点和终点）
            # 但是，起点和终点已经是0（因为result2初始为0），所以我们只需要将中间点标记为2

            # 将起点和终点加入negativepoint，防止后续分段时被用作无人机服务点
            negativepoint.append(result1[start])
            negativepoint.append(result1[end])

            # 更新start为end，开始下一段
            start = end
            i = end + 1
        else:
            # 如果没有找到可以构建无人机段的终点，那么当前点start+1不能作为无人机段的起点，我们将其标记为卡车点，并向后移动
            # 但是，我们也可以考虑将start+1作为下一个段的起点（卡车点），所以不需要标记为无人机点
            start = i
            i += 1

    # 分段结束后，我们得到result2，然后将其赋值给tournow[1]
    tournow[1] = result2
    for ia in range(0, result1length):
        if tourbest[1][ia] == 1:
            tourbest[1][ia] = 2
        elif tourbest[1][ia] == 0:
            tourbest[1][ia] = 3
    tournow = tourbest
    valuenow, judge = caculatetour1(tournow, Vtruck, Vfly, SR, SL, result1length, distMat, UAV_endurance)
    for io in range(1, result1length - 1):
        if tournow[1][io] == 2:
            tournow[1][io] = 1
            valuenow, judge1 = caculatetour1(tournow, Vtruck, Vfly, SR, SL, result1length, distMat, UAV_endurance)
    for ip in range(1, result1length - 1):
        if tournow[1][ip] == 1:
            tournew = copy.deepcopy(tournow)
            tournew[1][ip] = 2
            valuenew, judge1 = caculatetour2(tournew, Vtruck, Vfly, SR, SL, result1length, distMat, UAV_endurance)
            if judge1 == 1:
                tournow = tournew
                valuenow = valuenew
    tour_best = copy.deepcopy(tournow)
    value_best = valuenow
    for ik in range(10000):  # 对放飞段进行局部扰动
        r3 = random.random()
        if r3 > 1:
            tournew = raodong_fenpei1(tournow, result1length)
            valuenew, judge1 = caculatetour2(tournew, Vtruck, Vfly, SR, SL, result1length, distMat, UAV_endurance)
        else:
            tournew = local_raodong(tournow, result1length)
            valuenew, judge1 = caculatetour2(tournew, Vtruck, Vfly, SR, SL, result1length, distMat, UAV_endurance)
        if valuenew < valuenow and judge1 == 1:
            tournow = tournew
            valuenow = valuenew
            if valuenew < value_best:
                tour_best = tournew
                value_best = valuenew
    print(tour_best)
    print(value_best)
    fig = plt.figure()  # 这里的代码是画最优卡车无人机路径图
    x1 = [coordinates[tour_best[0][0]][0]]  # 1是卡车，2是无人机1,3是无人机2，4是无人机3
    y1 = [coordinates[tour_best[0][0]][1]]
    x2 = [coordinates[tour_best[0][0]][0]]
    y2 = [coordinates[tour_best[0][0]][1]]
    x3 = [coordinates[tour_best[0][0]][0]]
    y3 = [coordinates[tour_best[0][0]][1]]
    x4 = [coordinates[tour_best[0][0]][0]]
    y4 = [coordinates[tour_best[0][0]][1]]
    fly1num = 0
    fly2num = 0
    fly3num = 0
    for point in range(1, result1length):
        if tour_best[1][point] == 1:
            x1.append(coordinates[tour_best[0][point]][0])
            y1.append(coordinates[tour_best[0][point]][1])
        elif tour_best[1][point] == 2:
            x2.append(coordinates[tour_best[0][point]][0])
            y2.append(coordinates[tour_best[0][point]][1])
            fly1num = fly1num + 1
        elif tour_best[1][point] == 3:
            if fly1num != 0:
                x2.append(coordinates[tour_best[0][point]][0])
                y2.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x2, y2, 'o:b', markersize=4)  # 改色
                for j in range(len(x2) - 1):
                    plt.annotate('', xy=(x2[j + 1], y2[j + 1]), xytext=(x2[j], y2[j]),
                                 arrowprops=dict(arrowstyle="->", linewidth=1, linestyle=':', color='b', alpha=1))
                x2 = [coordinates[tour_best[0][point]][0]]
                y2 = [coordinates[tour_best[0][point]][1]]
            else:
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                x2 = [coordinates[tour_best[0][point]][0]]
                y2 = [coordinates[tour_best[0][point]][1]]
            fly1num = 0
        elif tour_best[1][point] == 4:
            x3.append(coordinates[tour_best[0][point]][0])
            y3.append(coordinates[tour_best[0][point]][1])
            fly2num = fly2num + 1
        elif tour_best[1][point] == 5:
            if fly2num != 0:
                x3.append(coordinates[tour_best[0][point]][0])
                y3.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x3, y3, 'o--r', markersize=4)  # 改色
                for j in range(len(x3) - 1):
                    plt.annotate('', xy=(x3[j + 1], y3[j + 1]), xytext=(x3[j], y3[j]),
                                 arrowprops=dict(arrowstyle="->", linewidth=1, linestyle=':', color='r', alpha=1))
                x3 = [coordinates[tour_best[0][point]][0]]
                y3 = [coordinates[tour_best[0][point]][1]]
            else:
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                x3 = [coordinates[tour_best[0][point]][0]]
                y3 = [coordinates[tour_best[0][point]][1]]
            fly2num = 0
        elif tour_best[1][point] == 7:
            if fly1num != 0:
                x2.append(coordinates[tour_best[0][point]][0])
                y2.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x2, y2, 'o:b', markersize=4)  # 改色
                for j in range(len(x2) - 1):
                    plt.annotate('', xy=(x2[j + 1], y2[j + 1]), xytext=(x2[j], y2[j]),
                                 arrowprops=dict(arrowstyle="->", linewidth=1, linestyle=':', color='b', alpha=1))
                x2 = [coordinates[tour_best[0][point]][0]]
                y2 = [coordinates[tour_best[0][point]][1]]
            else:
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                x2 = [coordinates[tour_best[0][point]][0]]
                y2 = [coordinates[tour_best[0][point]][1]]
            if fly2num != 0:
                x3.append(coordinates[tour_best[0][point]][0])
                y3.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x3, y3, 'o--r', markersize=4)  # 改色
                for j in range(len(x3) - 1):
                    plt.annotate('', xy=(x3[j + 1], y3[j + 1]), xytext=(x3[j], y3[j]),
                                 arrowprops=dict(arrowstyle="->", linewidth=1, linestyle=':', color='r', alpha=1))
                x3 = [coordinates[tour_best[0][point]][0]]
                y3 = [coordinates[tour_best[0][point]][1]]
            else:
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                x3 = [coordinates[tour_best[0][point]][0]]
                y3 = [coordinates[tour_best[0][point]][1]]
            fly2num = 0
            fly1num = 0
        elif tour_best[1][point] == 8:
            x4.append(coordinates[tour_best[0][point]][0])
            y4.append(coordinates[tour_best[0][point]][1])
            fly3num = fly3num + 1
        elif tour_best[1][point] == 9:
            if fly3num != 0:
                x4.append(coordinates[tour_best[0][point]][0])
                y4.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x4, y4, 'o--g', markersize=4)  # 改色
                for j in range(len(x4) - 1):
                    plt.annotate('', xy=(x4[j + 1], y4[j + 1]), xytext=(x4[j], y4[j]),
                                 arrowprops=dict(arrowstyle="->", linewidth=1, linestyle=':', color='g', alpha=1))
                x4 = [coordinates[tour_best[0][point]][0]]
                y4 = [coordinates[tour_best[0][point]][1]]
            else:
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                x4 = [coordinates[tour_best[0][point]][0]]
                y4 = [coordinates[tour_best[0][point]][1]]
            fly3num = 0
        elif tour_best[1][point] == 11:
            if fly1num != 0:
                x2.append(coordinates[tour_best[0][point]][0])
                y2.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x2, y2, 'o:b', markersize=4)  # 改色
                for j in range(len(x2) - 1):
                    plt.annotate('', xy=(x2[j + 1], y2[j + 1]), xytext=(x2[j], y2[j]),
                                 arrowprops=dict(arrowstyle="->", linewidth=1, linestyle=':', color='b', alpha=1))
                x2 = [coordinates[tour_best[0][point]][0]]
                y2 = [coordinates[tour_best[0][point]][1]]
            else:
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                x2 = [coordinates[tour_best[0][point]][0]]
                y2 = [coordinates[tour_best[0][point]][1]]
            fly1num = 0
            if fly3num != 0:
                x4.append(coordinates[tour_best[0][point]][0])
                y4.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x4, y4, 'o--g', markersize=4)  # 改色
                for j in range(len(x4) - 1):
                    plt.annotate('', xy=(x4[j + 1], y4[j + 1]), xytext=(x4[j], y4[j]),
                                 arrowprops=dict(arrowstyle="->", linewidth=1, linestyle=':', color='g', alpha=1))
                x4 = [coordinates[tour_best[0][point]][0]]
                y4 = [coordinates[tour_best[0][point]][1]]
            else:
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                x4 = [coordinates[tour_best[0][point]][0]]
                y4 = [coordinates[tour_best[0][point]][1]]
            fly3num = 0
        elif tour_best[1][point] == 13:
            if fly2num != 0:
                x3.append(coordinates[tour_best[0][point]][0])
                y3.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x3, y3, 'o--r', markersize=4)  # 改色
                for j in range(len(x3) - 1):
                    plt.annotate('', xy=(x3[j + 1], y3[j + 1]), xytext=(x3[j], y3[j]),
                                 arrowprops=dict(arrowstyle="->", linewidth=1, linestyle=':', color='r', alpha=1))
                x3 = [coordinates[tour_best[0][point]][0]]
                y3 = [coordinates[tour_best[0][point]][1]]
            else:
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                x3 = [coordinates[tour_best[0][point]][0]]
                y3 = [coordinates[tour_best[0][point]][1]]
            fly2num = 0
            if fly3num != 0:
                x4.append(coordinates[tour_best[0][point]][0])
                y4.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x4, y4, 'o--g', markersize=4)  # 改色
                for j in range(len(x4) - 1):
                    plt.annotate('', xy=(x4[j + 1], y4[j + 1]), xytext=(x4[j], y4[j]),
                                 arrowprops=dict(arrowstyle="->", linewidth=1, linestyle=':', color='g', alpha=1))
                x4 = [coordinates[tour_best[0][point]][0]]
                y4 = [coordinates[tour_best[0][point]][1]]
            else:
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                x4 = [coordinates[tour_best[0][point]][0]]
                y4 = [coordinates[tour_best[0][point]][1]]
            fly3num = 0
        elif tour_best[1][point] == 15:
            if fly1num != 0:
                x2.append(coordinates[tour_best[0][point]][0])
                y2.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x2, y2, 'o:b', markersize=4)  # 改色
                for j in range(len(x2) - 1):
                    plt.annotate('', xy=(x2[j + 1], y2[j + 1]), xytext=(x2[j], y2[j]),
                                 arrowprops=dict(arrowstyle="->", linewidth=1, linestyle=':', color='b', alpha=1))
                x2 = [coordinates[tour_best[0][point]][0]]
                y2 = [coordinates[tour_best[0][point]][1]]
            else:
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                x2 = [coordinates[tour_best[0][point]][0]]
                y2 = [coordinates[tour_best[0][point]][1]]
            fly1num = 0
            if fly2num != 0:
                x3.append(coordinates[tour_best[0][point]][0])
                y3.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x3, y3, 'o--r', markersize=4)  # 改色
                for j in range(len(x3) - 1):
                    plt.annotate('', xy=(x3[j + 1], y3[j + 1]), xytext=(x3[j], y3[j]),
                                 arrowprops=dict(arrowstyle="->", linewidth=1, linestyle=':', color='r', alpha=1))
                x3 = [coordinates[tour_best[0][point]][0]]
                y3 = [coordinates[tour_best[0][point]][1]]
            else:
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                x3 = [coordinates[tour_best[0][point]][0]]
                y3 = [coordinates[tour_best[0][point]][1]]
            fly2num = 0
            if fly3num != 0:
                x4.append(coordinates[tour_best[0][point]][0])
                y4.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x4, y4, 'o--g', markersize=4)  # 改色
                for j in range(len(x4) - 1):
                    plt.annotate('', xy=(x4[j + 1], y4[j + 1]), xytext=(x4[j], y4[j]),
                                 arrowprops=dict(arrowstyle="->", linewidth=1, linestyle=':', color='g', alpha=1))
                x4 = [coordinates[tour_best[0][point]][0]]
                y4 = [coordinates[tour_best[0][point]][1]]
            else:
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                x4 = [coordinates[tour_best[0][point]][0]]
                y4 = [coordinates[tour_best[0][point]][1]]
            fly3num = 0
            # 添加无人机和卡车路线箭头
    for i in range(len(x1) - 1):
        plt.arrow(x1[i], y1[i], x1[i + 1] - x1[i], y1[i + 1] - y1[i], head_width=0.05, head_length=0.1, fc='k', ec='k',
                  linestyle='-', linewidth=1.5, length_includes_head=True)  # 卡车路线箭头
    # plt.scatter(x1, y1)
    # plt.scatter(x2, y2,'')
    plt.plot(x2, y2, 'o:b', markersize=4, label='uav1')  # 改颜色在这里
    #     plt.plot(x3, y3, 'o--r', markersize=4,label='uav2')
    #     plt.plot(x4, y4, 'o--g', markersize=4,label='uav3')
    plt.plot(x1, y1, 'o-k', label='truck', markersize=4)  # 卡车路线
    plt.scatter(coordinates[tour_best[0][0]][0], coordinates[tour_best[0][0]][1], color='r', marker='*', s=150,
                label='depot')  # 用星号表示0序号值对应的客户节点
    plt.legend(loc='upper right', prop={'family': 'Times New Roman'}, fontsize=10, frameon=True, ncol=1)
    plt.show()
    exit()


if __name__ == '__main__':
    main()
