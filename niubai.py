# 扭摆法验证平行轴定理
# JamesBourbon in 20191210 refined
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import os
from statistic_model import linear

# 数据输入
'''I_stick = 4.089E-3  # 由之前的数据处理可以得到金属杆的理论转动惯量
k = 0.03075 # 由之前的数据处理可以得到扭摆弹簧的转动系数
data_hk = np.array([241.70, 3.331, 3.510, 0.570])
# 按照质量，长度，外径，内径的格式输入数据
x0 = np.arange(5, 30, 5)
T_mean = np.array([2.636, 3.408, 4.400, 5.504, 6.664,]) '''
# 周期数据
try:
    path = os.getcwd()
    data_T_x0 = pd.read_csv('{}/扭摆_input_1.csv'.format(path))
    data_other = pd.read_csv('{}/扭摆_input_2.csv'.format(path))
except:
    print('输入文件准备有误！系统将使用内置文件完成程序并给出示例')
    data_T_x0 = pd.read_csv('扭摆_input_1.csv')
    data_other = pd.read_csv('扭摆_input_2.csv')
# 数据处理
T_mean = np.array(data_T_x0['T_mean'])
x0 = np.array(data_T_x0['x0'])
I_stick = np.array(data_other['数值'][data_other['物理量'] 
                                 == 'I_stick'], dtype=np.float64)
k = np.array(data_other['数值'][data_other['物理量']
                                 == 'k'], dtype=np.float64)
m = np.array(data_other['数值'][data_other['物理量']
                               == 'm'], dtype=np.float64)
l = np.array(data_other['数值'][data_other['物理量']
                                 == 'l'], dtype=np.float64)
Ra = np.array(data_other['数值'][data_other['物理量'] 
                              == 'Ra'], dtype=np.float64)
Rb = np.array(data_other['数值'][data_other['物理量']
                                 == 'Rb'], dtype=np.float64)
I_hk = (1/8) * (m*1E-3) * ((Ra*1E-2)**2 + (Rb
            * 1E-2)**2) + (1/6) * (m*1E-3) * (l*1E-2)**2
I_ideal = I_stick + I_hk + 2 * m*1E-3 * (x0*1E-2)**2
I_real = k * T_mean**2 / (4 * np.pi**2)
E = (I_ideal - I_real) / I_real

msg1 = '滑块转动惯量: {}\n'.format(I_hk)
msg2 = '理论转动惯量分布: {}\n'.format(I_ideal)
msg3 = '实际转动惯量分布: {}\n'.format(I_real)
msg4 = '相对误差依次为: {}\n'.format(E)
msg = msg1 + msg2 + msg3 + msg4
print(msg)
# 顺便写入文件
with open('扭摆_output.csv','w') as f:
    f.write(msg)

# 线性拟合
P_linear, R2 = linear(x0**2, I_real)
xx = np.arange(0,700,1)
yy = np.polyval(P_linear, xx)

# 作图
plt.figure(figsize=(25,16))
plt.rcParams['font.family'] = 'Arial Unicode MS'
plt.rcParams['font.size'] = 18
# 调整matplotlib内部设置使之支持中文,这种方法改变全局设置
plt.plot(x0**2, I_real, 'bo', label='实验数据点', markersize=14)
plt.plot(xx, yy, 'r-.', label='拟合曲线', linewidth=4)
plt.xlabel(r'$x^2 / cm^2$', fontsize=20)
plt.ylabel(r'$I / Kg·m^2$', fontsize=20)
plt.title('平行轴定理验证实验曲线图', fontsize=28)

# 拟合线描述图例
txt_point = (x0[-2]**2, I_real[2])
# 相对点法
msg = '拟合方程: y = {:g} x + {:g}\n     R2 = {:.4f}'.format(
    P_linear[0], P_linear[1], R2)
plt.annotate(msg, xy=txt_point, xytext=txt_point, fontsize=24)

# 出图设置
plt.grid()
plt.legend()
plt.savefig('{}/扭摆.png'.format(path))
print('The picture is saved and output file is created! ')
# plt.show()
print('done!')
