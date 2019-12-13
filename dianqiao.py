import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import os

path = os.getcwd()
input_file = '{}/电桥_input.csv'.format(path)
data = pd.read_csv(input_file)
L = data['L'] # mm
R = data['R'] # 1E-3Ω
d1 = data['d'] # mm
d0 = data['d0'][0] # mm

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

P_linear, R2 = linear(L, R)
# 此处会输出一次拟合所得参数和R值
d_real = d1 - d0
d_real = np.mean(d_real)
p_result = (np.pi/4) * (d_real * 1E-3) ** 2 * P_linear[0]
print('电阻率计算值: {} Ω·m'.format(p_result))
# 计算电阻率结果

xx = np.arange(np.min(L), np.max(L), 0.1)  # 插值
yy = np.polyval(P_linear, xx)

# 作图
plt.figure(1,figsize=(25,16))
plt.rcParams['font.family'] = 'Arial Unicode MS'
plt.rcParams['font.size'] = 18
# 调整matplotlib内部设置使之支持中文,这种方法改变全局设置
plt.plot(L, R, 'bo', label='实验数据点', markersize=14)
plt.plot(xx, yy, 'r-.', label='拟合曲线', linewidth=4)
plt.ylabel('$R / x10^{-3} Ω$', fontsize=22)
plt.xlabel('L / mm', fontsize=22)
plt.title('铜棒电阻R-L关系图', fontsize=28)

# 设置坐标轴范围
x_min = np.min(L) - 10.0
y_min = np.min(R) - 0.05
x_max = np.max(L) + 10.0
y_max = np.max(R) + 0.10
x_delta = 10
y_delta = 0.10
plt.xlim((x_min, x_max))
plt.ylim((y_min, y_max))
# 设置坐标轴刻度
my_x_ticks = np.arange(x_min, x_max, x_delta)
my_y_ticks = np.arange(y_min, y_max, y_delta)
plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)

# 拟合线描述图例
txt_point = (L[3], R[2])
# 找到的一个最好点，亦可对此处代码进行改进
msg = '拟合方程: y = {:.4g} x + {:.3g}\n    R2 = {:.4f}'.format(
    P_linear[0], P_linear[1], R2) 
plt.annotate(msg, xy=txt_point, xytext=txt_point)

# 出图设置
plt.grid()
plt.legend()
plt.savefig('{}/开尔文电桥.png'.format(path))
print('the picture is saved!')
print('done!')
# plt.show()