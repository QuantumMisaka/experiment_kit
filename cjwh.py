# JamesBourbon in 20201116
# 沉降物化实验的数据处理
# 曲线拟合scipy.optimize.curve_fit初应用

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from statistic_model import linear  # 引入线性拟合
from scipy.optimize import curve_fit

# 数据导入
data = pd.read_csv('cjwh.csv')
y = np.array(data['m'])
x = np.array(data['t'])
# 实验参数
eta = 0.0009111  # 黏度,Pa·S
rho = 2700 # 滑石粉密度,kg/m3
rho_0 = 997.2995 # 介质密度,kg/m3
h = 0.13 # 沉降高度,m
g = 9.81

# 线性拟合求mc
x_c = x[-8:] # t
y_c = y[-8:] # m
x_cc = 1000/x_c
P_linear, R2 = linear(x_cc, y_c)
xx_c = np.linspace(np.min(x_cc), np.max(x_cc), 50)
yy_c = np.polyval(P_linear, xx_c)

mc = P_linear[1] #最大沉降质量,g
print(f'mc:{mc}')

# 线性拟合图作图
# 作图
plt.figure(1)
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['font.size'] = 16
# 调整matplotlib内部设置使之支持中文,这种方法改变全局设置
plt.plot(xx_c, yy_c, 'r-.', label='拟合曲线', linewidth=4)
plt.plot(x_cc, y_c, 'bo', label='实验数据点', markersize=10)
plt.xlabel(u'$1000/t (s^{-1})$', fontsize=24)
plt.ylabel(u'沉降重量 $m/g$', fontsize=24)
plt.title('线性拟合外推法求取沉降总量曲线图', fontsize=28)
plt.grid()
plt.legend()
# 拟合线描述图例
txt_point = (np.mean(xx_c[xx_c >= np.mean(xx_c)]), np.mean(yy_c))
# 相对点法
msg = '拟合方程: y={:.4g}x+{:.4g}\n  R2 = {:.4f}'.format(
    P_linear[0], P_linear[1], R2)
plt.annotate(msg, xy=txt_point, xytext=txt_point)

# 曲线拟合函数定义
def func(t,a,b,c):
    global mc
    return mc * (1-np.exp(-a * t**(b + c*np.log(t))))

# curve_fit环节
popt,pcov = curve_fit(func,x,y)
a,b,c = popt[0],popt[1],popt[2]
yy = func(x,a,b,c)
print(a,b,c)

# 作图
plt.figure(2)
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['font.size'] = 16
# 调整matplotlib内部设置使之支持中文,这种方法改变全局设置
plt.plot(x, yy, 'r-', label='拟合曲线', linewidth=2.2)
plt.plot(x, y, 'bo', label='实验数据点', markersize=5)
plt.xlabel('时间 $t/s$', fontsize=24)
plt.ylabel('沉降重量 $m/g$', fontsize=24)
plt.title('多级分散体系沉降曲线图', fontsize=28)
# 拟合线描述图例
txt_point = (np.mean(x), np.mean(yy))
# 相对点法
msg = '拟合方程:\n $m_t = mc * [1-exp(- (a) * t ^{(b + c \ln (t)) } ) ]$'
msg = msg.replace('mc', f'{mc:.4g}')
msg = msg.replace('a', f'{a:.4g}')
msg = msg.replace('b', f'{b:.4g}')
msg = msg.replace('c', f'{c:.4g}')
plt.annotate(msg, xy=txt_point, xytext=txt_point)
plt.grid()
plt.legend()

# 导函数
# 导函数形式是固定的 直接内置
def dfunc(t,a,b,c):
    global mc
    return a*mc*t**(b + c*np.log(t))*(
        (b + 2*c*np.log(t))/t)*np.exp(-a*t**(b + c*np.log(t)))

# 由半径求取对应的完全沉降时间的函数
def func_tr(r, eta=eta, rho=rho, rho_0=rho_0, h=h, g=g):
    t = (9*eta*h)/(2*g*(rho-rho_0)*r**2)
    return t

# 利用切线斜率求截距
def func_St(t, mt, dmdt):
    S = mt - t*dmdt
    return S
# 数据处理求分布函数折线图
r = np.arange(1,14) # um
dr = 1 # um
t_r = func_tr(r*1E-6)
m_tr = func(t_r,a,b,c)
dmdt_r = dfunc(t_r,a,b,c)
S_r = func_St(t_r, m_tr, dmdt_r)
dS_r = []
for i in range(1,len(S_r)):
    dS_r.append(S_r[i-dr]-S_r[i])
dS_r = np.array(dS_r)
f_Sr = dS_r / (mc * dr * 1E-6)

# 作图
plt.figure(3)
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['font.size'] = 16
# 调整matplotlib内部设置使之支持中文,这种方法改变全局设置
plt.bar(r[1:], f_Sr, width=1,edgecolor='red',
    color='white',linewidth=4)
plt.xlabel('半径 $r / um$', fontsize=24)
plt.ylabel('分布函数 f', fontsize=24)
plt.title('多级沉降体系粒度分布图', fontsize=28)

# 出数据
result_data = pd.DataFrame(
    [r,t_r,m_tr,dmdt_r,S_r,dS_r,f_Sr],
    index=['r','t','m_t','dm/dt','S','∆S','f'])
result_data.to_csv('result_cjwh.csv')
# 出图
plt.show()
