#!/usr/bin/env python
# coding: utf-8

# In[4]:


import math
import random
import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
from numpy.matlib import rand
from matplotlib.artist import getp
import copy
import time

#构建初始参考距离矩阵

def InitializeCityPoints(N,maxLength,maxWidth):
    cityPoints = []
    for i in range(0,N):
        newPoint = []
        pointX = random.uniform(0,maxLength)
        pointY = random.uniform(0,maxWidth)
        newPoint.append(round(pointX,2))
        newPoint.append(round(pointY,2))
        cityPoints.append(newPoint)
    return cityPoints
def getdistance():
    for i in range(n):
        for j in range(n):
            x = pow(city_x[i] - city_x[j], 2)
            y = pow(city_y[i] - city_y[j], 2)
            distance[i][j] = pow(x + y, 0.5)
    for i in range(n):
        for j in range(n):
            if distance[i][j] == 0:
                distance[i][j] = sys.maxsize

#计算总距离
def cacl_best(rou):
    sumdis = 0.0
    for i in range(n-1):
        sumdis += distance[rou[i]][rou[i+1]]
    sumdis += distance[rou[n-1]][rou[0]]     
    return sumdis

#得到新解
def getnewroute(route, time):
    #如果是偶数次，二变换法
    '''
    注意：数组直接复制是复制地址
    例如， current = route
    想要得到一个新的有同样内容的数组，应该用： current = copy.copy(route) 
    '''
    current = copy.copy(route)  
    
    if time % 2 == 0:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        temp = current[u]
        current[u] = current[v]
        current[v] = temp
    #如果是奇数次，三变换法 
    else:
        temp2 = random.sample(range(0, n), 3)
        temp2.sort()
        u = temp2[0]
        v = temp2[1]
        w = temp2[2]
        w1 = w + 1
        temp3 = [0 for col in range(v - u + 1)]
        j =0
        for i in range(u, v + 1):
            temp3[j] = current[i]
            j += 1
        
        for i2 in range(v + 1, w + 1):
            current[i2 - (v-u+1)] = current[i2]
        w = w - (v-u+1)
        j = 0
        for i3 in range(w+1, w1):
            current[i3] = temp3[j]
            j += 1
    
    return current
    
def draw(best):
    result_x = [0 for col in range(n+1)]
    result_y = [0 for col in range(n+1)]
    
    for i in range(n):
        result_x[i] = city_x[best[i]]
        result_y[i] = city_y[best[i]]
    result_x[n] = result_x[0]
    result_y[n] = result_y[0]
    # print(result_x)
    # print(result_y)
    # plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlim(0, maxLength)  # 限定横轴的范围
    plt.ylim(0, maxWidth)  # 限定纵轴的范围
    plt.plot(result_x, result_y, marker='>', mec='r', mfc='w',label=u'route')
    plt.legend()  # 让图例生效
    plt.margins(0)
    plt.subplots_adjust(bottom=0.15)
    for i in range(len(best)):
        plt.text(result_x[i] + 0.05, result_y[i] + 0.05, str(best[i]+1), color='red')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('graph')
    plt.show()
     
def print_route(route):
    result_cur_best=[]
    for i in route:
        result_cur_best+=[i]
    for i in range(len(result_cur_best)):
        result_cur_best[i] += 1
    result_path = result_cur_best
    result_path.append(result_path[0])
    return result_path    
    
def solve():
    #得到距离矩阵
    getdistance()
    #得到初始解以及初始距离
    route = random.sample(range(0, n), n) 
    total_dis = cacl_best(route)
    print("Initial Route:", print_route(route))
    print("Initial Distance:", total_dis)
    draw(route)
    startTime = time.time()
    #新解
    newroute = []
    new_total_dis = 0.0
    best = route
    best_total_dis = total_dis
    t = T0
    
    while True:
        if t <= Tend:
            break
        #令温度为初始温度
        for rt2 in range(L):
            newroute = getnewroute(route, rt2)
            new_total_dis = cacl_best(newroute)
            delt = new_total_dis - total_dis
            if delt <= 0:
                route = newroute
                total_dis = new_total_dis
                if best_total_dis > new_total_dis:
                    best = newroute
                    best_total_dis = new_total_dis
            elif delt > 0:
                p = math.exp(-delt / t)
                ranp = random.uniform(0, 1)
                if ranp < p:
                    route = newroute
                    total_dis = new_total_dis
        t = t * a
    exTime = time.time() - startTime
    print("Executation Time:",round(exTime,4))
    print("Temperture:", t)
    print("Optimal Route:", print_route(best))
    print("Optimal Distance:", best_total_dis)  
    draw(best)   
if __name__=="__main__":

    n = 1000
    maxLength = 1000
    maxWidth = 1000
    cityPoints = InitializeCityPoints(n,maxLength,maxWidth)
    coord = np.array(cityPoints)
    print("Randomly Initialized City Points:")
    print(coord)
    w, h = coord.shape
    coordinates = np.zeros((w, h), float)
    for i in range(w):
        for j in range(h):
            coordinates[i, j] = float(coord[i, j])
    city_x=coordinates[:,0]
    city_y=coordinates[:,1]
#     print(coordinates)
#     print(city_x)
#     print(city_y)
    # #城市数量
    distance = [[0 for col in range(n)] for raw in range(n)]
    #初始温度 结束温度
    T0 = 31
    Tend = 1e-8
    #循环控制常数
    L = 10
    #温度衰减系数
    a = 0.98
    solve()


# In[ ]:




