# JamesBourbon in 20201109
# [Co(NH3)6]Cl3的表征作图
# 插值法scipy.interpolate初应用

import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
from statistic_model import linear # 引入线性拟合包
from scipy import interpolate # 插值

# 线性拟合求氯离子含量
x1 = np.array([1,2,3]) # 第四个点(4,155)舍弃
y1 = np.array([60,104,142])

P_linear, R2 = linear(x1, y1)
P_reverse, R2_2 = linear(y1, x1)
xx = np.linspace(np.min(x1), np.max(x1), 50)
yy = np.polyval(P_linear, xx)
# 作图
plt.figure(1)
plt.rcParams['font.family'] = 'Arial Unicode MS'
plt.rcParams['font.size'] = 16
# 调整matplotlib内部设置使之支持中文,这种方法改变全局设置
plt.plot(x1, y1, 'bo', label='实验数据点', markersize=12)
plt.plot(xx, yy, 'r-.', label='拟合曲线', linewidth=3)
plt.xlabel(r'pCl', fontsize=24)
plt.ylabel(r'E / mV', fontsize=24)
plt.title('电位分析法测定氯离子含量标准曲线图', fontsize=28)

# 拟合线描述图例
txt_point = (np.mean(x1[x1<=np.mean(x1)]), np.mean(y1[y1 >= np.mean(y1)]))
# 相对点法
msg = '拟合方程: y = {:g} x + {:g}\n     R2 = {:.4f}'.format(
    P_linear[0], P_linear[1], R2)
plt.annotate(msg, xy=txt_point, xytext=txt_point)

# 标注样品对应点,此参数在样品电位已知时直接给出
y_sample = 127
x_sample = np.polyval(P_reverse,y_sample)
test_point = np.array([x_sample,y_sample])
test_txt_point = test_point+np.array([-0.2, -20])
msg_test = f'样品:E={y_sample}mV, pCl={x_sample:.3f}'
plt.plot(test_point[0],test_point[1],'p', markersize=15, color='purple')
plt.annotate(msg_test, xy=test_point, xytext=test_txt_point,
             arrowprops=dict(facecolor='black',width=0.05,shrink=0.02))
plt.grid()
plt.legend()

# 作图表示此物质的最大吸收波长
# 光度计实验数据
x2 = np.array([400,420,440,460,
                465,470,475,480,
                485,490,495,500,
                520,540,560])
y2 = np.array([0.051,0.120,0.246,0.381,
                0.404,0.418,0.422,0.417,
                0.402,0.377,0.347,0.311,
                0.157,0.053,0.013])
# 最大吸收波长位置自动求取
y_max = max(y2)
x_max = x2[np.where(y2==y_max)[0]] #=475

# 尝试spline插值法
xx2 = np.linspace(np.min(x2),np.max(x2),50)
f = interpolate.interp1d(x2,y2,kind='quadratic')
# nearest,zero阶梯插值，slinear线性插值
# quadratic/cubic 2阶/3阶样条曲线插值
# 这个简单图二次样条就够了
# 建议去认真学一下scipy和sympy
yy2 = f(xx2)

# 作图
plt.figure(2)
plt.rcParams['font.family'] = 'Arial Unicode MS'
plt.rcParams['font.size'] = 16
# 调整matplotlib内部设置使之支持中文,这种方法改变全局设置
plt.plot(x2, y2, 'bo', label='实验数据点',markersize=12)
plt.plot(xx2, yy2, 'r:', label='二次插值拟合曲线',linewidth=3.8)
plt.xlabel(r'$\lambda / nm$', fontsize=24)
plt.ylabel(r'$A$', fontsize=24)
plt.title(r'$[Co(NH_3)_6]Cl_3$'+'的吸收曲线图', fontsize=28)

# 标示最大吸收
max_point = np.array([x_max,y_max])
plt.plot(max_point[0],max_point[1],'p',color='purple',markersize=14)
line_x = np.array([max_point[0],max_point[0]])
line_y = np.array([0,max_point[1]+0.075])
plt.plot(line_x,line_y,'k-.',linewidth=2)

# 相对点法
msg = u'$(\lambda_{max}=475,A=0.422)$'
msg = msg.replace('475',f'{x_max[0]}')
msg = msg.replace('0.422',f'{y_max}')
plt.annotate(msg, xy=max_point, xytext=max_point+np.array([-50,0.04]),
               arrowprops=dict(facecolor='black',width=0.05,shrink=0.02))
msg_1 ='$\lambda_{max}=475$'
msg_1 = msg_1.replace('475',f'{x_max[0]}')
plt.annotate(msg_1,xy=(max_point[0]-5, line_y[1]), xytext=(max_point[0]-5, line_y[1]))

# 出图设置
plt.grid()
plt.legend()
plt.show()


