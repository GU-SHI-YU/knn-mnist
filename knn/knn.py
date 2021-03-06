# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 09:00:05 2020

@author: Gu Shiyu
"""

import datetime
from numpy import *
import numpy as np
from os import listdir
import struct
import matplotlib.pyplot as plt

#读取图片
def read_image(file_name):
    file_handle=open(file_name,"rb")  #以二进制打开文档
    file_content=file_handle.read()   #读取到缓冲区中
    offset=0
    head = struct.unpack_from('>IIII', file_content, offset)  # 取前4个整数，返回一个元组
    offset += struct.calcsize('>IIII')
    imgNum = head[1]  #图片数
    rows = head[2]   #宽度
    cols = head[3]  #高度
    images=np.empty((imgNum , 28 * 28))
    image_size=rows * cols#单个图片的大小
    fmt='>' + str(image_size) + 'B'#单个图片的format
    for i in range(imgNum):
        images[i] = np.array(struct.unpack_from(fmt, file_content, offset))
        offset += struct.calcsize(fmt)
    return images

#读取标签
def read_label(file_name):
    file_handle = open(file_name, "rb")  # 以二进制打开文档
    file_content = file_handle.read()  # 读取到缓冲区中
    head = struct.unpack_from('>II', file_content, 0)  # 取前2个整数，返回一个元组
    offset = struct.calcsize('>II')
    labelNum = head[1]  # label数
    fmt = '>' + str(labelNum) + 'B'
    label = struct.unpack_from(fmt, file_content, offset)  # 取data数据，返回一个元组
    return np.array(label)

#KNN算法
def KNN(test_data, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]#dataSet.shape[0]表示的是读取矩阵第一维度的长度，代表行数
    distance1 = np.tile(test_data, (dataSetSize)).reshape((60000,784))-dataSet
    distance2 = ((distance1**2).sum(axis=1))**0.5
    sortedDistIndicies = distance2.argsort() #返回从小到大排序的索引
    classCount=np.zeros((10), np.int32)#10是代表10个类别
    for i in range(k): #统计前k个数据类的数量
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] += 1
    max = 0
    id = 0
    for i in range(classCount.shape[0]):
        if classCount[i] >= max:
            max = classCount[i]
            id = i
    return id

def test_KNN():
    # 文件获取
    train_image = "train-images.idx3-ubyte"
    test_image = "t10k-images.idx3-ubyte"
    train_label = "train-labels.idx1-ubyte"
    test_label = "t10k-labels.idx1-ubyte"
    # 读取数据
    train_x = read_image(train_image)  # train_dataSet
    test_x = read_image(test_image)  # test_dataSet
    train_y = read_label(train_label)  # train_label
    test_y = read_label(test_label)  # test_label
    testRatio = 1  # 取数据集的前0.1为测试数据,这个参数比重可以改变
    test_row=test_x.shape[0]
    testNum = int(test_row * testRatio)
    
    errorCount = 0 # 判断错误的个数
    for i in range(testNum):
        result = KNN(test_x[i], train_x, train_y, 5)
        if result != test_y[i]:
            errorCount += 1.0# 如果mnist验证集的标签和本身标签不一样，则出错
        if(i % 100 == 0):
            print(i)
    error_rate = errorCount / testNum  # 计算出错率
    acc = 1 - error_rate
    print("\nthe total accuracy rate is: %f" % (acc))

if __name__ == "__main__":
    begin = datetime.datetime.now()
    test_KNN()
    end = datetime.datetime.now()
    print (end - begin).seconds