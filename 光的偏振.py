# 大物实验数据处理 光的偏振
# JamesBourbon in 20200524
# 极坐标作图的极好例子

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

def linear(x, y):
    # 线性回归拟合，一个非常高端的拟合算法
    x_n = sm.add_constant(x)  # statsmodels进行回归时，一定要添加此常数项
    model = sm.OLS(y, x_n)  # model是回归分析模型
    results = model.fit()  # results是回归分析后的结果
    # 输出回归分析的结果并进行线性回归出图
    print(results.summary())
    print('Parameters: ', results.params)
    print('R2: ', results.rsquared)
    # 拟合系数的排列方法和多项式系数排列方法相反
    # 需要在这里做一个多项式系数的reverse
    result_poly = []
    result_poly.append(results.params[1])
    result_poly.append(results.params[0])
    return np.array(result_poly), results.rsquared
    # 返回线性拟合参数和R^2值


input_file = "光的偏振.csv"

lw = 3.5
ms = 12.5
fs = 22
font = 'KaiTi'
# font = 'Arial Unicode MS
# 配色：红紫配色 探索出来的很好的双色配色法
# 极坐标图的显示是角度制，输入是弧度制

data = pd.read_csv(input_file)
x = np.array(data['\\theta'])
x_r = np.array(data['\\theta'] * np.pi/180)
y0 = np.array(data['I_0'])
y1 = np.array(data['I_1/4_30'])
y21 = np.array(data['I_1/2_0'])
y22 = np.array(data['I_1/2_30'])
cosx2 = np.cos(x_r) ** 2

# 线性拟合
P_linear, R2 = linear(cosx2, y0)
xx = np.arange(0, 1, 0.01)
yy = np.polyval(P_linear, xx)

# 马吕斯定律
plt.figure(1)

plt.rcParams['font.family'] = font
plt.rcParams['font.size'] = fs-2
# 调整matplotlib内部设置使之支持中文,这种方法改变全局设置
# 坐标轴刻度
my_x_ticks = np.arange(0, 390, 30)
plt.xticks(my_x_ticks)
# 作图
plt.plot(x, y0, '-.',color='purple', linewidth=lw)
plt.plot(x, y0, 'ro', label='实验数据点', markersize=ms,)
plt.xlabel('θ /°', fontsize=fs)
plt.ylabel('光强I', fontsize=fs)
plt.title('验证马吕斯定律曲线', fontsize=fs+4)
plt.grid()
plt.legend()

# 马吕斯定律线性拟合
plt.figure(2)
plt.rcParams['font.family'] = font
plt.rcParams['font.size'] = fs-2
# 调整matplotlib内部设置使之支持中文,这种方法改变全局设置
plt.plot(xx, yy, '-.', color='purple', label='拟合曲线', linewidth=lw)
plt.plot(cosx2, y0, 'ro', label='实验数据点', markersize=ms ,linewidth=lw)
plt.xlabel(r'$cos^2(θ)$', fontsize=fs)
plt.ylabel('光强I', fontsize=fs)
plt.title('验证马吕斯定律线性拟合线', fontsize=fs+4)
# 拟合线描述图例
txt_point = (0.6, 15)
# 找到的一个最好点，亦可对此处代码进行改进
msg = '拟合方程: y = {:.4g} x + {:.4g}\n    R2 = {:.4f}'.format(
    P_linear[0], P_linear[1], R2)
plt.annotate(msg, xy=txt_point, xytext=txt_point)
plt.grid()
plt.legend()

# 1/4波片的I的极坐标图
# Matplotlib最强大的调整是面向对象的方法
fig3 = plt.figure(3)
plt.rcParams['font.family'] = font
plt.rcParams['font.size'] = fs-2
# 调整轴对象的属性
ax1 = fig3.add_axes([0.1,0.1,0.8,0.8],polar=True)
# 添加极坐标轴的默认方法
# ax1.set_thetamin, thetamax, rmin rmax, yticks
# 不能用坐标图常用的plt.xticks方式
ax1.set_xticks(np.arange(0, 2*np.pi, np.pi/6))
# 调整matplotlib内部设置使之支持中文,这种方法改变全局设置
ax1.plot(x_r, y1, '-',color='purple', lw=lw)
ax1.plot(x_r, y1, 'o', color='red', label='偏离光轴30度', ms=ms)
ax1.set_xlabel('θ /°', fontsize=fs)
# ax1.set_ylabel('光强I', fontsize=fs,)
ax1.set_title('通过1/4波片的偏振光光强-角度曲线', fontsize=fs+4)
fig3.legend(loc='best')

# 1/2波片的I的极坐标图
# 红紫配色方案和红棕配色方案都是科研作图的不错选择
fig4 = plt.figure(4)
plt.rcParams['font.family'] = font
plt.rcParams['font.size'] = fs-2
# 调整matplotlib内部设置使之支持中文,这种方法改变全局设置
ax2 = fig4.add_axes([0.1,0.1,0.8,0.8],polar=True)
ax2.set_xticks(np.arange(0, 2*np.pi, np.pi/6))

ax2.plot(x_r, y21, 'o-', color='red', label='偏离光轴0度', ms=ms, lw=lw)
ax2.plot(x_r, y22, 'o-', color='purple',label='偏离光轴30度', ms=ms, lw=lw)
ax2.set_xlabel('θ /°', fontsize=fs)
# ax2.set_ylabel('光强I', fontsize=fs,)
ax2.set_title('通过1/2波片的偏振光光强-角度曲线', fontsize=fs+4)
fig4.legend(loc='best')

# 普通极坐标图
plt.figure(5)
plt.rcParams['font.family'] = font
plt.rcParams['font.size'] = fs-2
# 调整matplotlib内部设置使之支持中文,这种方法改变全局设置
plt.polar(x_r, y21, 'o-', color='red', label='偏离光轴0度', ms=ms, lw=lw)
plt.polar(x_r, y22, 'o-', color='purple',label='偏离光轴30度', ms=ms, lw=lw)
plt.xlabel('θ /°', fontsize=fs)
# ax2.set_ylabel('光强I', fontsize=fs,)
plt.title('通过1/2波片的偏振光光强-角度曲线', fontsize=fs+4)
plt.legend(loc='best')


plt.show()
