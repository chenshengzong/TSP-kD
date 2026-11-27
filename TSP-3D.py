import math                         # 导入模块 math
import random                       # 导入模块 random
import pandas as pd                 # 导入模块 pandas 并简写成 pd
import numpy as np                  # 导入模块 numpy 并简写成 np YouCans
import matplotlib.pyplot as plt     # 导入模块 matplotlib.pyplot 并简写成 plt
import time
import copy

# 子程序：读取TSPLib数据
def read_TSPLib(fileName):
    res = []
    with open(fileName, 'r') as fid:
        for item in fid:
            if len(item.strip())!=0:
                res.append(item.split())
    loadData = np.array(res).astype('float')      # 数据格式：i Xi Yi
    coordinates = loadData[:,1::]
    return coordinates

# 子程序：计算各城市间的距离，得到距离矩阵
def getDistMat(nCities, coordinates):
    max=0
    distMat = np.zeros((nCities,nCities))       # 初始化距离矩阵
    for i in range(nCities):
        for j in range(i,nCities):
            # np.linalg.norm 求向量的范数（默认求 二范数），得到 i、j 间的距离
            distMat[i][j] = distMat[j][i] = round(np.linalg.norm(coordinates[i]-coordinates[j]))
            if distMat[i][j]>max:
                max=distMat[i][j]
    return distMat,max                              # 城市间距离取整（四舍五入）

#近邻表格
def getJinlin(nCities,num,distMat):
    Jinlindis = np.zeros((nCities,1))       # 近邻距离，只有这个距离之内的可以被选择
    k=0
    j=0
    Jinlin=[]
    for dis1 in distMat:
        discopy=dis1.copy()
        discopy.sort()
        Jinlindis[k]=discopy[num]               #设置每个城市第num-1距离为半径
        k=k+1
    for dis2 in distMat:
        pointset=[]
        for i in range(0,nCities):    
            if dis2[i]<=Jinlindis[j] and i!=j:
                pointset.append(i)
        Jinlin.append(pointset)
        j=j+1
    return  Jinlin

# 子程序：计算 TSP 路径长度
def calTourMileage(tourGiven, nCities, distMat):
    # custom function caltourMileage(nCities, tour, distMat):
    # to compute mileage of the given tour
    mileageTour = distMat[tourGiven[nCities-1], tourGiven[0]]   # dist((n-1),0)
    for i in range(nCities-1):                                  # dist(0,1),...dist((n-2)(n-1))
        mileageTour += distMat[tourGiven[i], tourGiven[i+1]]
    return round(mileageTour)                     # 路径总长度取整（四舍五入）

# 子程序：绘制 TSP 路径图
def plot_tour(tour, value, coordinates):
    # custom function plot_tour(tour, nCities, coordinates)
    num = len(tour)
    x0, y0 = coordinates[tour[num - 1]]
    x1, y1 = coordinates[tour[0]]
    plt.scatter(int(x0), int(y0), s=15, c='r')      # 绘制城市坐标点 C(n-1)
    plt.plot([x1, x0], [y1, y0], c='b')             # 绘制旅行路径 C(n-1)~C(0)
    for i in range(num - 1):
        x0, y0 = coordinates[tour[i]]
        x1, y1 = coordinates[tour[i + 1]]
        plt.scatter(float(x0), float(y0), s=15, c='r')  # 绘制城市坐标点 C(i)
        plt.plot([x1, x0], [y1, y0], c='b')         # 绘制旅行路径 C(i)~C(i+1)
    plt.xlabel("Total mileage of the tour:{:.1f}".format(value))
    plt.title("Optimization tour of TSP{:d}".format(num))  # 设置图形标题
    plt.show()

def distroy1(tourNow,nCities,distMat,num):                                                      #贪心摧毁前num个
    LIST=[]
    list=[]
    mileageTour0 = distMat[tourNow[nCities-1], tourNow[0]]+distMat[tourNow[0], tourNow[1]]
    list.append([tourNow[0],mileageTour0])
    for i in range(1,nCities-1):
        mileageTour = distMat[tourNow[i-1], tourNow[i]]+distMat[tourNow[i], tourNow[i+1]]
        list.append([tourNow[i],mileageTour])
    mileageTour1 = distMat[tourNow[nCities-2], tourNow[nCities-1]]+distMat[tourNow[nCities-1], tourNow[0]]
    list.append([tourNow[nCities-1],mileageTour1])
    my_lest=sorted(list , key=lambda k: k[1],reverse=True)                                     #二维坐标进行降序
    for j in range(num):
        LIST.append(my_lest[j][0])                                                             #LIST是要拆除的坐标
    tourNew=[]                                                                                  #这是初始解拆除LIST要拆除坐标后的解
    for l in range(nCities):
        if tourNow[l] not in LIST:
            tourNew.append(tourNow[l])
    return LIST,tourNew                                                                     #返回的是拆除名单和出去拆除名单后的解

def distroy2(tourNow,nCities,num):                                                              #随机摧毁num个
    LIST=random.sample(range(nCities),num)
    tourNew=[]                                                                                  #这是初始解拆除LIST要拆除坐标后的解
    for l in range(nCities):
        if tourNow[l] not in LIST:
            tourNew.append(tourNow[l])
    return LIST,tourNew                                                                       #返回的是拆除名单和出去拆除名单后的解

def distroy3(tourNow,nCities,num):                                                              #随机摧毁num个连续城市
    LIST=[]
    x=random.randint(0,nCities-1)
    tourNow1=[]
    for i in range(nCities):
        tourNow1.append(tourNow[i])
    tourNow2= tourNow1[x:] + tourNow1[:x]
    for j in range(num):
        LIST.append(tourNow2[j])
    tourNew=[]                                                                                  #这是初始解拆除LIST要拆除坐标后的解
    for l in range(nCities):
        if tourNow[l] not in LIST:
            tourNew.append(tourNow[l])
    return LIST,tourNew                                                                       #返回的是拆除名单和出去拆除名单后的解


def distroy4(tourNow,nCities,num,jinlin,Jinnum):                                              #非近邻摧毁
    LIST=[]
    x=random.randint(0,nCities-1)
    if num>Jinnum:
        for ii in range(Jinnum):
            LIST.append(jinlin[tourNow[x]][ii])
        while True:
            y=random.randint(0,nCities-1)
            if tourNow[y] not in LIST:
                LIST.append(tourNow[y])
                if len(LIST)==num:
                    break
    else:
        y=random.randint(0,nCities-1)
        LIST1=random.sample(range(Jinnum),num)
        for ii in range(num):
            LIST.append(jinlin[tourNow[x]][LIST1[ii]])
    tourNew=[]                                                                                  #这是初始解拆除LIST要拆除坐标后的解
    for l in range(nCities):
        if tourNow[l] not in LIST:
            tourNew.append(tourNow[l])    
    return LIST,tourNew 


def repair1(LIST,tourNew,distMat,num):                                  #噪声贪心修复
    tourstart=tourNew
    for i in range(num):
        value=[]
        for j in range(len(tourstart)-1):
            if j==0:
                value1=distMat[tourstart[j], LIST[i]]+distMat[tourstart[-1], LIST[i]]-distMat[tourstart[-1], tourstart[j]]
                value.append(value1)
            else:
                value1=distMat[tourstart[j], LIST[i]]+distMat[tourstart[j-1], LIST[i]]-distMat[tourstart[j-1], tourstart[j]]
                value.append(value1)
        bestvalue=min(value)
        position=value.index(bestvalue)
        tourstart.insert(position,LIST[i])
    return tourstart

def repair2(LIST,tourNew,num,jinlin):                                #k近邻修复
    tourNow1=[]
    for i in range(len(tourNew)):
        tourNow1.append(tourNew[i])
    for j in range(num):
        x=LIST[j]
        n=0
        while True:
            n=n+1
            y=random.sample(jinlin[x],1)
            if y in tourNow1:
                break
            if n>20:
                zindex=random.randint(0, len(tourNew)-1)
                y=tourNew[zindex]
                break
        yindex=tourNow1.index(y)
        tourNow1.insert(yindex,LIST[j])
    return tourNow1

def repair3(LIST,tourNew,distMat,num,u,temp_max):                     #噪声贪心修复，u表示噪音系数
    tourstart=tourNew
    for i in range(num):
        value=[]
        for j in range(len(tourstart)-1):
            r3=random.random()
            if j==0:
                value1=distMat[tourstart[j], LIST[i]]+distMat[tourstart[-1], LIST[i]]-distMat[tourstart[-1], tourstart[j]]+temp_max*(2*r3-1)*u
                value.append(value1)
            else:
                value1=distMat[tourstart[j], LIST[i]]+distMat[tourstart[j-1], LIST[i]]-distMat[tourstart[j-1], tourstart[j]]+temp_max*(2*r3-1)*u
                value.append(value1)
        bestvalue=min(value)
        position=value.index(bestvalue)
        tourstart.insert(position,LIST[i])
    return tourstart        
 

def creatT(Tlength,nCities,distMat,nummax,jinlin,Jinnum,temp_max):      #创建初始解和初始温度，初始列表用两倍长度以去除噪声
     gapgroup=[]
     tourNow=np.random.permutation(nCities)
     valueNow= calTourMileage(tourNow,nCities,distMat)
     while True:
          r1=random.uniform(0,1)                                            #r1控制破坏
          r2=random.uniform(0,1)                                            #r2控制修复
          num=random.randint(int(2/nummax),nummax)                                     #破坏点的个数(不改了，效果不大)
          u=0.1       
          if r1<=0.25:
              LIST,tourNew=distroy1(tourNow,nCities,distMat,num) 
          elif r1>0.25 and r1<=0.5:
              LIST,tourNew=distroy2(tourNow,nCities,num)
          elif r1>0.5 and r1<=0.75:
              LIST,tourNew=distroy3(tourNow,nCities,num)
          else:
              LIST,tourNew=distroy4(tourNow,nCities,num,jinlin,Jinnum) 
          if r2<0.5:
               tourNew=repair1(LIST,tourNew,distMat,num)                
          else:
               tourNew=repair3(LIST,tourNew,distMat,num,u,temp_max)  
          valueNew = calTourMileage(tourNew,nCities,distMat)
          if valueNew<=valueNow:
              tourNow=tourNew
              valueNow=valueNew
          else:
              gap=valueNew -valueNow
              tourNow=tourNew
              valueNow=valueNew
              gapgroup.append(gap)
              gapgrouplength=len(gapgroup) 
              if gapgrouplength>=Tlength*3:
                  break
     gapgroup.sort()
     TT=gapgroup[int(2*Tlength):int(3*Tlength)]
     TT.sort()
     return TT,tourNow,valueNow

def caculatetour(result, Vtruck, Vfly, SR,SL, result1length, distMat,UAV_endurance):
    result1=result[0]                       #TSP路径
    result2=result[1]
    L1 = 0                              # 无人机1飞行距离
    L2 = 0                              # 无人机2飞行距离
    L3 = 0                              # 无人机3飞行距离
    fly1num=0                           # 无人机1段内服务点
    fly2num=0                           # 无人机2段内服务点
    fly3num=0                           # 无人机3段内服务点    
    fly1lastpoint=result1[0]            
    fly2lastpoint=result1[0]
    fly3lastpoint=result1[0]
    trucklastpoint=result1[0]
    T1=0                                 # 无人机1到达时间  
    T2=0                                 # 无人机2到达时间  
    T3=0                                 # 卡车到达时间
    T4=0                                 # 无人机4到达时间   
    judge=1                              # 判断解是不是可行的
    for i in range(1, result1length):
        if result2[i]%2 == 1 :                                              # 为奇数              
            if result2[i]== 1:
                T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)
                trucklastpoint=result1[i]
            else:
                if result2[i]== 3:                                          # 无人机1和卡车汇合
                    if fly1num>=1:
                        L1=L1+distMat[result1[i], fly1lastpoint]
                        if L1>UAV_endurance:
                            judge=0
                        T1=T1+L1/Vfly+SL+SR
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR
                    else:
                        T1=T1+(distMat[result1[i], trucklastpoint]/Vtruck)
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)
                    Tmax=max(T1,T3)
                    T1=Tmax
                    T3=Tmax
                    L1=0
                    fly1num=0
                    trucklastpoint=result1[i]
                    fly1lastpoint=result1[i]
                elif result2[i]== 5:                                          # 无人机2和卡车汇合
                    if fly2num>=1:
                        L2=L2+distMat[result1[i], fly2lastpoint]
                        T2=T2+L2/Vfly+SL+SR
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR
                        if L2>UAV_endurance:
                            judge=0
                    else:
                        T2=T2
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)
                    Tmax=max(T2,T3)
                    T2=Tmax
                    T3=Tmax
                    L2=0
                    fly2num=0
                    trucklastpoint=result1[i]
                    fly2lastpoint=result1[i]
                elif result2[i]== 7:
                    if fly1num>=1 and fly2num>=1:
                        L1=L1+distMat[result1[i], fly1lastpoint]
                        T1=T1+L1/Vfly+SL+SR
                        L2=L2+distMat[result1[i], fly2lastpoint]
                        T2=T2+L2/Vfly+SL+SR
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR+SL+SR
                        Tmax=max(T1,T2,T3)
                    elif fly1num>=1 and fly2num==0:
                        L1=L1+distMat[result1[i], fly1lastpoint]
                        T1=T1+L1/Vfly+SL+SR     
                        T2=T2             
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR 
                        Tmax=max(T1,T3)
                    elif fly1num==0 and fly2num>=1:
                        T1=T1
                        L2=L2+distMat[result1[i], fly2lastpoint]
                        T2=T2+L2/Vfly+SL+SR
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR
                        Tmax=max(T2,T3)   
                    else:
                        T1=T1
                        T2=T2
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)
                        Tmax=max(T1,T2,T3)
                    if L1>UAV_endurance or L2>UAV_endurance:
                        judge=0
                    T1=Tmax
                    T2=Tmax
                    T3=Tmax
                    L1=0
                    L2=0
                    fly1num=0
                    fly2num=0
                    trucklastpoint=result1[i]
                    fly1lastpoint=result1[i]
                    fly2lastpoint=result1[i]
                elif result2[i]== 9:
                    if fly3num>=1:
                        L3=L3+distMat[result1[i], fly3lastpoint]
                        T4=T4+L3/Vfly+SL+SR
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR
                        if L3>UAV_endurance:
                            judge=0
                    else:
                        T4=T4
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)
                    Tmax=max(T3,T4)
                    T4=Tmax
                    T3=Tmax
                    L3=0
                    fly3num=0
                    trucklastpoint=result1[i]
                    fly3lastpoint=result1[i]
                elif result2[i]== 11:
                    if fly1num>=1 and fly3num>=1:
                        L1=L1+distMat[result1[i], fly1lastpoint]
                        T1=T1+L1/Vfly+SL+SR
                        L3=L3+distMat[result1[i], fly3lastpoint]
                        T4=T4+L3/Vfly+SL+SR
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR+SL+SR
                        Tmax=max(T1,T3,T4)             
                    elif fly1num>=1 and fly3num==0:
                        L1=L1+distMat[result1[i], fly1lastpoint]
                        T1=T1+L1/Vfly+SL+SR     
                        T4=T4             
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR 
                        Tmax=max(T1,T3)  
                    elif fly1num==0 and fly3num>=1:
                        T1=T1
                        L3=L3+distMat[result1[i], fly3lastpoint]
                        T4=T4+L3/Vfly+SL+SR
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR
                        Tmax=max(T3,T4)   
                    else:
                        T1=T1
                        T4=T4
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)
                        Tmax=max(T1,T3,T4)
                    if L1>UAV_endurance or L3>UAV_endurance:
                        judge=0
                    T1=Tmax
                    T3=Tmax
                    T4=Tmax
                    L1=0
                    L3=0
                    fly1num=0
                    fly3num=0
                    trucklastpoint=result1[i]
                    fly1lastpoint=result1[i]
                    fly3lastpoint=result1[i]
                elif result2[i]== 13:
                    if fly2num>=1 and fly3num>=1:
                        L2=L2+distMat[result1[i], fly2lastpoint]
                        T2=T2+L2/Vfly+SL+SR
                        L3=L3+distMat[result1[i], fly3lastpoint]
                        T4=T4+L3/Vfly+SL+SR
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR+SL+SR
                        Tmax=max(T2,T3,T4)             
                    elif fly2num>=1 and fly3num==0:
                        L2=L2+distMat[result1[i], fly2lastpoint]
                        T2=T2+L2/Vfly+SL+SR     
                        T4=T4             
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR 
                        Tmax=max(T2,T3)  
                    elif fly2num==0 and fly3num>=1:
                        T2=T2
                        L3=L3+distMat[result1[i], fly3lastpoint]
                        T4=T4+L3/Vfly+SL+SR
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR
                        Tmax=max(T3,T4)   
                    else:
                        T2=T2
                        T4=T4
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)
                        Tmax=max(T2,T3,T4)
                    if L2>UAV_endurance or L3>UAV_endurance:
                        judge=0
                    T2=Tmax
                    T3=Tmax
                    T4=Tmax
                    L2=0
                    L3=0
                    fly2num=0
                    fly3num=0
                    trucklastpoint=result1[i]
                    fly2lastpoint=result1[i]
                    fly3lastpoint=result1[i]
                elif result2[i]== 15:
                    if fly1num>=1 and fly2num>=1 and fly3num>=1 :
                        L1=L1+distMat[result1[i], fly1lastpoint]
                        T1=T1+L1/Vfly+SL+SR
                        L2=L2+distMat[result1[i], fly2lastpoint]
                        T2=T2+L2/Vfly+SL+SR
                        L3=L3+distMat[result1[i], fly3lastpoint]
                        T4=T4+L3/Vfly+SL+SR
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR+SL+SR+SL+SR
                        Tmax=max(T1,T2,T3,T4)  
                    elif fly1num==0 and fly2num>=1 and fly3num>=1 :
                        T1=T1
                        L2=L2+distMat[result1[i], fly2lastpoint]
                        T2=T2+L2/Vfly+SL+SR
                        L3=L3+distMat[result1[i], fly3lastpoint]
                        T4=T4+L3/Vfly+SL+SR
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR+SL+SR
                        Tmax=max(T2,T3,T4)                      
                    elif fly1num>=1 and fly2num==0 and fly3num>=1 :
                        L1=L1+distMat[result1[i], fly1lastpoint]
                        T1=T1+L1/Vfly+SL+SR
                        T2=T2
                        L3=L3+distMat[result1[i], fly3lastpoint]
                        T4=T4+L3/Vfly+SL+SR
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR+SL+SR
                        Tmax=max(T1,T3,T4)  
                    elif fly1num>=1 and fly2num>=1 and fly3num==0 :
                        L1=L1+distMat[result1[i], fly1lastpoint]
                        T1=T1+L1/Vfly+SL+SR
                        L2=L2+distMat[result1[i], fly2lastpoint]
                        T2=T2+L2/Vfly+SL+SR
                        T4=T4
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR+SL+SR
                        Tmax=max(T1,T2,T3) 
                    elif fly1num>=1 and fly2num==0 and fly3num==0 :
                        L1=L1+distMat[result1[i], fly1lastpoint]
                        T1=T1+L1/Vfly+SL+SR
                        T2=T2
                        T4=T4
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR+SL+SR
                        Tmax=max(T1,T2,T3) 
                    elif fly1num==0 and fly2num>=1 and fly3num==0 :
                        T1=T1
                        L2=L2+distMat[result1[i], fly1lastpoint]
                        T2=T2+L2/Vfly+SL+SR
                        T4=T4
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR+SL+SR
                        Tmax=max(T1,T2,T3) 
                    elif fly1num==0 and fly2num==0 and fly3num>=1 :
                        T1=T1
                        T2=T2
                        L3=L3+distMat[result1[i], fly3lastpoint]
                        T4=T4+L3/Vfly+SL+SR
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)+SL+SR+SL+SR
                        Tmax=max(T1,T2,T3) 
                    else:
                        T1=T1
                        T2=T2
                        T3=T3+(distMat[result1[i], trucklastpoint]/Vtruck)
                        T4=T4
                        Tmax=T3                   
                    if L1>UAV_endurance or L2>UAV_endurance or L3>UAV_endurance:
                        judge=0
                    T1=Tmax
                    T2=Tmax
                    T3=Tmax
                    T4=Tmax
                    L1=0
                    L2=0
                    L3=0
                    fly1num=0
                    fly2num=0
                    fly3num=0
                    trucklastpoint=result1[i]
                    fly1lastpoint=result1[i]
                    fly2lastpoint=result1[i]
                    fly3lastpoint=result1[i]                            
        else:
            if result2[i]== 2:
                L1=L1+distMat[result1[i], fly1lastpoint]
                fly1num=fly1num+1
                fly1lastpoint=result1[i]
            elif result2[i]== 4:
                L2=L2+distMat[result1[i], fly2lastpoint]
                fly2num=fly2num+1
                fly2lastpoint=result1[i]
            elif result2[i]== 8:
                L3=L3+distMat[result1[i], fly3lastpoint]
                fly3num=fly3num+1
                fly3lastpoint=result1[i]
    return T3,judge

def raodong_fangfei(result,point):
    result1=result[1].copy()
    result2=result[1].copy()
    result1[point]=2
    result2[point]=4
    tour1=[result[0],result1]
    tour2=[result[0],result2]
    return tour1,tour2

def raodong_duannei(result,startpoint_index,endpoint_index):
    result2=result[1].copy()
    rd3=random.random()
    x1_index=random.randint(startpoint_index+1, endpoint_index-1)  
    if result2[x1_index]==2:             
        if rd3<=0.5:
            result2[x1_index]=1
        else:
            result2[x1_index]=4
    elif result2[x1_index]==1:             
        if rd3<=0.5:
            result2[x1_index]=2
        else:
            result2[x1_index]=4
    elif result2[x1_index]==4:             
        if rd3<=0.5:
            result2[x1_index]=2
        else:
            result2[x1_index]=1
    result_1=[result[0],result2]
    return result_1    

def raodong_fangfei1(tournow,ij):
    tour=copy.deepcopy(tournow)
    tour[1][ij]=2
    return tour

def raodong_fenpei1(tournow,result1length):
    tour=copy.deepcopy(tournow)
    x1_index=random.randint(1, result1length-1)
    if tour[1][x1_index]==2:
        tour[1][x1_index]=13
    elif tour[1][x1_index]==13:
        tour[1][x1_index]=2
    return tour 

def raodong_fangfei2(tournow,il):
    tour=copy.deepcopy(tournow)
    if tour[1][il]==13:
        tour[1][il]=4    
    elif tour[1][il]==15:
        tour[1][il]=11 
    return tour

def raodong_fenpei2(tournow,result1length):
    tour=copy.deepcopy(tournow)
    x1_index=random.randint(1, result1length-1)
    if tour[1][x1_index]==4:
        tour[1][x1_index]=9
    elif tour[1][x1_index]==9:
        tour[1][x1_index]=4
    return tour 

def raodong_fangfei3(tournow,il):
    tour=copy.deepcopy(tournow)
    if tour[1][il]==9:
        tour[1][il]=8    
    elif tour[1][il]==11:
        tour[1][il]=3 
    elif tour[1][il]==13:
        tour[1][il]=5 
    return tour

def raodong_fenpei3(tournow,result1length):
    tour=copy.deepcopy(tournow)
    x1_index=random.randint(1, result1length-1)
    if tour[1][x1_index]==2:
        pp=random.random()
        if pp>=0.3:
            tour[1][x1_index]=1
        elif pp>=0.3 and pp<0.6:
            tour[1][x1_index]=8
        else:
            tour[1][x1_index]=4
    elif tour[1][x1_index]==4:
        pp=random.random()
        if pp>=0.5:
            tour[1][x1_index]=1
        elif pp>=0.3 and pp<0.6:
            tour[1][x1_index]=8
        else:
            tour[1][x1_index]=2
    elif tour[1][x1_index]==1:
        pp=random.random()
        if pp>=0.5:
            tour[1][x1_index]=2
        elif pp>=0.3 and pp<0.6:
            tour[1][x1_index]=8
        else:
            tour[1][x1_index]=4
    elif tour[1][x1_index]==8:
        pp=random.random()
        if pp>=0.5:
            tour[1][x1_index]=1
        elif pp>=0.3 and pp<0.6:
            tour[1][x1_index]=2
        else:
            tour[1][x1_index]=4
    return tour 

def local_raodong(tournow,result1length):
    i = random.randint(1, result1length-2)         # 产生第一个 [0,n) 区间内的随机整数
    while True:
        j = random.randint(1, result1length-2)
        if i!=j : break                      # 保证 i, j 不相等
    tour=copy.deepcopy(tournow)
    r=random.random()
    if r>0.5:
        tour[1][i],tour[1][j] = tournow[1][j],tournow[1][i] # 交换 城市 i 和 j 的位置————简洁的实现方法
    else:
        nn = min([i, j])
        xx = max([i, j])
        gap = tournow[1][nn:xx+1]
        gap1 = gap[::-1]  # 片段反转
        tour[1][nn:xx+1] = gap1
    return tour

# 子程序：初始化模拟退火算法的控制参数
def initParameter():
    nMarkov =60        # Markov链长度，也即内循环运行次数
    Maxinter=100         #外循环次数
    Tlength=30        #温度列表长度
    Jinnum=20    #近邻表参数
    nummax=30    #破坏长度上限
    u=0.1                    #噪声系数
    UAV_endurance=1000
    SR = 5
    SL = 5
    Vfly = 1.5
    Vtruck = 1
    return nMarkov,Maxinter,Jinnum,Tlength,nummax,u,UAV_endurance,SR,SL,Vfly,Vtruck    

def main():
    start=time.time()
    coordinates =read_TSPLib('berlin52.txt')                       #案例点的坐标
    nMarkov,Maxinter,Jinnum,Tlength,nummax,u,UAV_endurance,SR,SL,Vfly,Vtruck= initParameter()           # 调用子程序，获得设置参数                                                      #近邻系数
    nCities = coordinates.shape[0]                                       #根据输入的城市坐标 获得城市数量 nCities
    distMat,temp_max = getDistMat(nCities, coordinates) 
    jinlin=getJinlin(nCities,Jinnum,distMat)                              #制作近邻表
    TT,tourNow,valueNow=creatT(Tlength,nCities,distMat,nummax,jinlin,Jinnum,temp_max)
    recordBest = []                                                       # 初始化 最优路径记录表
    recordNow  = []                                                       # 初始化 最优路径记录表
    tourBest  = tourNow                                                                              
    valueBest = valueNow                                                                                        
    BEST=[]
    BEST.append(tourBest)
    pd1=0.25
    pd2=0.25
    pd3=0.25
    pd4=0.25
    pr1=0.5
    pr3=0.5
    for wai in range(Maxinter):
            tNow=TT[Tlength-1]
            Tc=[]
            timed1=0
            timed2=0
            timed3=0
            timed4=0
            timer1=0
            timer3=0
            sd1=0 
            sd2=0 
            sd3=0  
            sd4=0 
            sr1=0 
            sr3=0 
            n=0
            while n<nMarkov:
                n=n+1
                r1=random.uniform(0,pd1+pd2+pd3+pd4)                                            #r1控制破坏
                r2=random.uniform(0,pr1+pr3)                                            #r2控制修复
                num=random.randint(int(nummax/4),nummax)
                if r1<pd1:                                                                 # 五种破坏算子
                    LIST,tourNew=distroy1(tourNow,nCities,distMat,num) 
                    timed1=timed1+1
                elif r1<pd2+pd1 and r1>=pd1:
                    LIST,tourNew=distroy2(tourNow,nCities,num)
                    timed2=timed2+1
                elif r1<pd3+pd2+pd1 and r1>=pd2+pd1:
                    LIST,tourNew=distroy3(tourNow,nCities,num)
                    timed3=timed3+1
                else:
                    LIST,tourNew=distroy4(tourNow,nCities,num,jinlin,Jinnum) 
                    timed4=timed4+1  
                random.shuffle(LIST)        
                if r2<pr1:
                    tourNew=repair1(LIST,tourNew,distMat,num)    
                    timer1=timer1+1               
                else:
                    tourNew=repair3(LIST,tourNew,distMat,num,u,temp_max)  
                    timer3=timer3+1
                valueNew = calTourMileage(tourNew,nCities,distMat)
                deltaE = valueNew - valueNow
                if valueNew<=valueNow:
                    if r1<pd1:                                                                 # 五种破坏算子
                        sd1=sd1+1
                    elif r1<pd2+pd1 and r1>=pd1:
                        sd2=sd2+1
                    elif r1<pd3+pd2+pd1 and r1>=pd2+pd1:
                        sd3=sd3+1
                    else:
                        sd4=sd4+1
                    if r2<pr1:
                        sr1=sr1+1              
                    else:
                        sr3=sr3+1                             
                    accept = True
                    if valueNew < valueBest:
                        if r1<pd1:                                                                 # 五种破坏算子
                            sd1=sd1+2
                        elif r1<pd2+pd1 and r1>=pd1:
                            sd2=sd2+2
                        elif r1<pd3+pd2+pd1 and r1>=pd2+pd1:
                            sd3=sd3+2
                        else:
                            sd4=sd4+2
                        if r2<pr1:
                            sr1=sr1+2            
                        else:
                            sr3=sr3+2      
                        BEST.append(tourNew)
                        tourBest = tourNew
                        valueBest = valueNew 
                else:
                    pAccept= math.exp(-deltaE/tNow)
                    pp=random.random()
                    if pAccept > pp :
                         Tc.append(-deltaE/math.log(pp))
                         accept = True
                    else:
                        accept = False
                # 保存新解
                if accept == True:                      # 如果接受新解，则将新解保存为当前解
                    tourNow = tourNew               
                    valueNow = valueNew
                    if r1<pd1:                                                                 # 五种破坏算子
                        sd1=sd1+1
                    elif r1<pd2+pd1 and r1>=pd1:
                        sd2=sd2+1
                    elif r1<pd3+pd2+pd1 and r1>=pd2+pd1:
                        sd3=sd3+1
                    else:
                        sd4=sd4+1
                    if r2<pr1:
                        sr1=sr1+1             
                    else:
                        sr3=sr3+1  
            Tclength=len(Tc)                            
            all=0
            if Tclength!=0 :                            #温度表的更新
               Tc.sort()
            #    Tavg=Tc[-1]
               for i in range(Tclength):
                   all=all+Tc[i]
               Tavg=(all/Tclength)
               TT.pop()
               TT.append(Tavg)  
               TT.sort()                  
            sdall=sd1/(timed1+0.001)+sd2/(0.001+timed2)+sd3/(0.001+timed3)+sd4/(timed4+0.001)                            #概率动态调整
            srall=sr1/(timer1+0.001)+sr3/(timer3+0.001)
            pd1=pd1*0.7+(sd1/(timed1+0.001))/(0.001+sdall)*0.3
            pd2=pd2*0.7+(sd2/(0.001+timed2))/(0.001+sdall)*0.3
            pd3=pd3*0.7+(sd3/(0.001+timed3))/(0.001+sdall)*0.3
            pd4=pd4*0.7+(sd4/(timed4+0.001))/(0.001+sdall)*0.3
            pr1=pr1*0.7+(sr1/(0.001+timer1))/(srall+0.001)*0.3
            pr3=pr3*0.7+(sr3/(0.001+timer3))/(srall+0.001)*0.3
            recordBest.append(valueBest)                
            recordNow.append(valueNow)                  # 将当前路径长度追加到 当前路径记录表
            print(f'求解{wai}次温度为{tNow}历史最优结果为 {valueBest} {valueNow}   {pd1}  {pd2}  {pd3} {pd4}  {pr1}  {pr3}        ')   
    zero_index = tourBest.index(0)
    resultTSP = tourBest[zero_index:] + tourBest[:zero_index]
    result1 = resultTSP + [0]                                                                           #第一层编码
    result1length=len(result1)                                                                        #城市数量n+1
    result2=[15]*result1length 
    tournow=[result1,result2]                                                                     #FSTSP的编码
    valuenow,judge=caculatetour(tournow, Vtruck, Vfly, SR,SL, result1length, distMat,UAV_endurance)
    tour_best=copy.deepcopy(tournow)
    value_best=valuenow
    for ij in range(1,result1length-1):
        tournew=raodong_fangfei1(tournow,ij)
        valuenew,judge1=caculatetour(tournew, Vtruck, Vfly, SR,SL, result1length, distMat,UAV_endurance)
        if judge1==1:
            tournow=tournew
            valuenow=valuenew
    for ik in range(2000):
        r3=random.random()
        if r3>0:
            tournew=raodong_fenpei1(tournow,result1length)
            valuenew,judge1=caculatetour(tournew, Vtruck, Vfly, SR,SL, result1length, distMat,UAV_endurance)
        else:
            tournew=local_raodong(tournow,result1length)
            valuenew,judge1=caculatetour(tournew, Vtruck, Vfly, SR,SL, result1length, distMat,UAV_endurance) 
        if valuenew<=valuenow and judge1==1:
            tournow=tournew
            valuenow=valuenew
            if valuenew<value_best:
                tour_best=tournew
                value_best=valuenew  
    for il in range(1,result1length-1):
        tournew=raodong_fangfei2(tournow,il)
        valuenew,judge1=caculatetour(tournew, Vtruck, Vfly, SR,SL, result1length, distMat,UAV_endurance)
        if judge1==1:
            tournow=tournew
            valuenow=valuenew
    for im in range(5000):
        tournew=raodong_fenpei2(tournow,result1length)
        valuenew,judge1=caculatetour(tournew, Vtruck, Vfly, SR,SL, result1length, distMat,UAV_endurance)
        if valuenew<=valuenow and judge1==1:
            tournow=tournew
            valuenow=valuenew
            if valuenew<value_best:
                tour_best=tournew
                value_best=valuenew  
    for io in range(1,result1length-1):
        tournew=raodong_fangfei3(tournow,io)
        valuenew,judge1=caculatetour(tournew, Vtruck, Vfly, SR,SL, result1length, distMat,UAV_endurance)
        if judge1==1:
            tournow=tournew
            valuenow=valuenew
    for ip in range(5000):
        tournew=raodong_fenpei3(tournow,result1length)
        valuenew,judge1=caculatetour(tournew, Vtruck, Vfly, SR,SL, result1length, distMat,UAV_endurance)
        if valuenew<valuenow and judge1==1:
            tournow=tournew
            valuenow=valuenew
            if valuenew<value_best:
                tour_best=tournew
                value_best=valuenew  
    tour_best=copy.deepcopy(tournow)
    value_best=valuenow
    print(tournow)
    print(valuenow)
    fig = plt.figure()                                             # 这里的代码是画最优卡车无人机路径图
    x1 = [coordinates[tour_best[0][0]][0]]                         #1是卡车，2是无人机1,3是无人机2，4是无人机3
    y1 = [coordinates[tour_best[0][0]][1]]
    x2 = [coordinates[tour_best[0][0]][0]]             
    y2 = [coordinates[tour_best[0][0]][1]]
    x3 = [coordinates[tour_best[0][0]][0]]            
    y3 = [coordinates[tour_best[0][0]][1]]
    x4 = [coordinates[tour_best[0][0]][0]]            
    y4 = [coordinates[tour_best[0][0]][1]]    
    fly1num=0
    fly2num=0
    fly3num=0
    for point in range(1, result1length):
        if tour_best[1][point] == 1:
            x1.append(coordinates[tour_best[0][point]][0])
            y1.append(coordinates[tour_best[0][point]][1])
        elif tour_best[1][point] == 2:
            x2.append(coordinates[tour_best[0][point]][0])
            y2.append(coordinates[tour_best[0][point]][1])
            fly1num=fly1num+1
        elif tour_best[1][point] == 3:
            if fly1num != 0:
                x2.append(coordinates[tour_best[0][point]][0])
                y2.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x2, y2, 'o:b', markersize=4)                     #改色
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
            fly1num=0           
        elif tour_best[1][point] == 4:
            x3.append(coordinates[tour_best[0][point]][0])
            y3.append(coordinates[tour_best[0][point]][1])
            fly2num=fly2num+1
        elif tour_best[1][point] == 5:
            if fly2num != 0:
                x3.append(coordinates[tour_best[0][point]][0])
                y3.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x3, y3, 'o--r', markersize=4)                           #改色
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
            fly2num=0     
        elif tour_best[1][point] == 7:
            if fly1num != 0:
                x2.append(coordinates[tour_best[0][point]][0])
                y2.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x2, y2, 'o:b', markersize=4)                          #改色
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
                plt.plot(x3, y3, 'o--r', markersize=4)                       #改色
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
            fly2num=0     
            fly1num=0  
        elif tour_best[1][point] == 8:
            x4.append(coordinates[tour_best[0][point]][0])
            y4.append(coordinates[tour_best[0][point]][1])
            fly3num=fly3num+1 
        elif tour_best[1][point] == 9:
            if fly3num != 0:
                x4.append(coordinates[tour_best[0][point]][0])
                y4.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x4, y4, 'o--g', markersize=4)                           #改色
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
            fly3num=0     
        elif tour_best[1][point] == 11:
            if fly1num != 0:
                x2.append(coordinates[tour_best[0][point]][0])
                y2.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x2, y2, 'o:b', markersize=4)                           #改色
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
            fly1num=0     
            if fly3num != 0:
                x4.append(coordinates[tour_best[0][point]][0])
                y4.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x4, y4, 'o--g', markersize=4)                           #改色
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
            fly3num=0     
        elif tour_best[1][point] == 13:
            if fly2num != 0:
                x3.append(coordinates[tour_best[0][point]][0])
                y3.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x3, y3, 'o--r', markersize=4)                           #改色
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
            fly2num=0     
            if fly3num != 0:
                x4.append(coordinates[tour_best[0][point]][0])
                y4.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x4, y4, 'o--g', markersize=4)                           #改色
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
            fly3num=0     
        elif tour_best[1][point] == 15:
            if fly1num != 0:
                x2.append(coordinates[tour_best[0][point]][0])
                y2.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x2, y2, 'o:b', markersize=4)                           #改色
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
            fly1num=0   
            if fly2num != 0:
                x3.append(coordinates[tour_best[0][point]][0])
                y3.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x3, y3, 'o--r', markersize=4)                           #改色
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
            fly2num=0     
            if fly3num != 0:
                x4.append(coordinates[tour_best[0][point]][0])
                y4.append(coordinates[tour_best[0][point]][1])
                x1.append(coordinates[tour_best[0][point]][0])
                y1.append(coordinates[tour_best[0][point]][1])
                plt.plot(x4, y4, 'o--g', markersize=4)                           #改色
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
            fly3num=0     
    # 添加无人机和卡车路线箭头
    for i in range(len(x1) - 1):
        plt.arrow(x1[i], y1[i], x1[i + 1] - x1[i], y1[i + 1] - y1[i], head_width=0.05, head_length=0.1, fc='k', ec='k',
                  linestyle='-', linewidth=1.5, length_includes_head=True)  # 卡车路线箭头
    # plt.scatter(x1, y1)
    # plt.scatter(x2, y2,'')
    plt.plot(x2, y2, 'o:b', markersize=4,label='uav1')              #改颜色在这里
    plt.plot(x3, y3, 'o--r', markersize=4,label='uav2')   
    plt.plot(x4, y4, 'o--g', markersize=4,label='uav3')   
    plt.plot(x1, y1, 'o-k', label='truck', markersize=4)  # 卡车路线
    plt.scatter(coordinates[tour_best[0][0]][0], coordinates[tour_best[0][0]][1], color='r', marker='*', s=150, label='depot')  # 用星号表示0序号值对应的客户节点
    plt.legend(loc='upper right', prop={'family': 'Times New Roman'}, fontsize=10, frameon=True, ncol=1)
    plt.show()
    exit()

if __name__ == '__main__':
    main()

