# 大物实验：波尔共振的数据处理程序
# JamesBourbon in 20191101

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

path = os.getcwd()
# 自由振荡实验数据
data_1 = pd.read_csv('{}/自由振荡_input.csv'.format(path))
# 振幅
sita_1 = np.array(data_1['sita'])
# 周期，两者均按照实验实际，以递减方法记录
T_1 = np.array(data_1['T'])
w0_1 = 2*np.pi / T_1  # 顺便求个固有频率
# 阻尼振荡实验数据
# 直接用周期10T:振幅的字典来表示

data_2 = pd.read_csv('{}/阻尼振荡_input.csv'.format(path))
data_beita = {}
test_dir = ['test1', 'test2', 'test3']
for test in test_dir:
    data_list = data_2[test][1:]
    data_list = list(data_list) # 一步一步做type转化
    data_beita[data_2[test][0]] = data_list
    
# 受迫振动实验数据
data_3 = pd.read_csv('{}/受迫振荡_input.csv'.format(path))
# 摆轮周期10T
T_bl10 = np.array(data_3['10T_bl'])
# 振幅，此处应按照递减或递增的顺序记录数据
sita_bl = np.array(data_3['sita_bl'])
# 相位差
fai_bl = np.array(data_3['fai_bl'])


# 数据处理与输出
msg_1 = '固有频率:\n{}\n'.format(w0_1)
print(msg_1)

# 数据输出
output_file = '{}/波尔共振_output.csv'.format(path)
with open(output_file, 'w') as f:
    f.write('----波尔共振数据处理----\n')
    f.write('--------------------\n')
    f.write('自由振荡: 固有频率:\n')
    for i in w0_1:
        f.write('{:6g}\n'.format(float(i)))

# 阻尼系数的求取
def cal_beita(data_beita):
    # 逐差法求阻尼系数以及计算过程输出
    print('对数逐差法三次计算结果:')
    beita_list = []
    for key, value in data_beita.items():
        T = key / 10
        n = 10 // 2
        ln_list = []
        for i in range(n):
            ln_list.append(np.log(value[i] / value[i+n]))
        print('{}'.format(ln_list))
        with open(output_file, 'a') as f:
            f.write('\n阻尼振荡数据处理:\n对数逐差法三次计算结果:\n')
            for i in ln_list:
                f.write("{:.6g}, ".format(float(i)))
        ln_list = np.array(ln_list)
        beita_i = np.mean(ln_list) / (n * T)
        beita_list.append(beita_i)
        # 通过对五对数据的分别处理来得到逐差法的阻尼系数list
    return beita_list

beita_list = cal_beita(data_beita)
beita_mean = np.mean(np.array(beita_list))

# 受迫振动的数据处理
w_bl = 20*np.pi / T_bl10
# 求取对应实验点的固有频率
# 通过自由振动对实际摆轮进行区间较正
w0 = []
for sita_i in sita_bl:
    for i in range(len(w0_1)):
        if sita_i > sita_1[i]:
            w0.append(w0_1[i])
            break
    else:
        w0.append(w0_1[-1])
w0 = np.array(w0)
x0 = w_bl / w0 # 得到绘图的x坐标

        
# 数据再输出
with open(output_file, 'a') as f:
    f.write('\n重复三次计算所得阻尼系数值:\n')
    f.write('{}\n'.format(list(beita_list)))
    f.write('平均值: {}\n'.format(beita_mean))

with open(output_file, 'a') as f:
    f.write('\n受迫振荡数据处理:\n')
    f.write('各组数据对应w0:\n')
    for i in w0:
        f.write('{:.6g}\n'.format(float(i)))
    f.write('\n各组数据对应w/w0:\n')
    for i in x0:
        f.write('{:.6g}\n'.format(float(i)))
    
# 受迫振动的幅频特性曲线和相频特性曲线绘制
plt.rcParams['font.family'] = 'Arial Unicode MS'
plt.rcParams['font.size'] = 16
# 调整matplotlib内部设置使之支持中文,这种方法改变全局设置

# 绘制幅频特性曲线
figsize = (25,12)
plt.figure(1, figsize) #新建图框
plt.plot(x0, sita_bl, 'bo', label='实验数据点', markersize=12)
plt.plot(x0, sita_bl, 'r-', label='实验曲线', linewidth=3)
plt.xlabel('频率比 ω/ω0', fontsize=20)
plt.ylabel('振幅 θ / °', fontsize=20)
plt.title('θ ~ ω/ω0 幅频特性曲线图', fontsize=26)
plt.legend() # 显示图例
plt.grid() # 显示网格线
plt.savefig('{}/波尔共振_幅频特性曲线'.format(path))

# 绘制相频特性曲线
plt.figure(2, figsize)
plt.plot(x0, -fai_bl, 'bo', label='实验数据点', markersize=12)
plt.plot(x0, -fai_bl, 'r-', label='实验曲线', linewidth=3)
plt.grid()
plt.xlabel('频率比 ω/ω0', fontsize=20)
plt.ylabel('相位差 ∅ / °', fontsize=20)
plt.title('∅ ~ ω/ω0 相频特性曲线图', fontsize=26)
plt.legend()
plt.savefig('{}/波尔共振_相频特性曲线'.format(path))
print('数据文件和图均已保存在当前目录下')
# 显示所得图，并可对得到的两张图操作与保存
plt.show()
print('done!')
