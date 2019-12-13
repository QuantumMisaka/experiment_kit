# 拉伸法测定杨氏模量的数据处理
# JamesBourbon in 20191208

import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
from uncertainty import Uncertainty # 引入不确定度计算库
from statistic_model import linear # 引入线性拟合包
import os

# 数据读入以及初步处理
path = os.getcwd()
data_F_x = pd.read_csv('{}/拉伸杨氏_input_1.csv'.format(path))
data_other = pd.read_csv('{}/拉伸杨氏_input_2.csv'.format(path))
F = np.array(data_F_x['F']) * 9.8 # 直接化单位
x_a = np.array(data_F_x['x_a'])
x_d = np.array(data_F_x['x_d'])
x_mean = (x_a + x_d) / 2 # 求前后两次平均
data_F_x['x_mean'] = x_mean # 加到DataFrame内，之后直接to_csv

d_dx = np.array(data_other['数值'][data_other['物理量'] 
                                 == 'd_dx'], dtype=np.float64)
d_dF = np.array(data_other['数值'][data_other['物理量']
                                 == 'd_dF'], dtype=np.float64)
D = np.array(data_other['数值'][data_other['物理量']
                               == 'D'], dtype=np.float64)
d_D = np.array(data_other['数值'][data_other['物理量']
                                 == 'd_D'], dtype=np.float64)
L = np.array(data_other['数值'][data_other['物理量'] 
                              == 'L'], dtype=np.float64)
d_L = np.array(data_other['数值'][data_other['物理量'] 
                                == 'd_L'], dtype=np.float64)
d_d = np.array(data_other['数值'][data_other['物理量']
                                 == 'd_d'], dtype=np.float64)
d0 = np.array(data_other['数值'][data_other['物理量']
                                == 'd0'], dtype=np.float64)
b = np.array(data_other['数值'][data_other['物理量'] 
                              == 'b'], dtype=np.float64)
d_b = np.array(data_other['数值'][data_other['物理量']
                                 == 'd_b'], dtype=np.float64)
d_array = np.array(data_other['数值'][data_other['物理量']
                                     == 'd'], dtype=np.float64)


# 逐差法测杨氏模量并求其不确定度
n = len(x_mean) // 2
dx = [(x_mean[i+n] - x_mean[i]) for i in range(n)] # 逐差
dx = np.array(dx)
dx_cal = Uncertainty('dx', dx, d_out=d_dx)
dx_data = dx_cal.data_output()
dF = [(F[i+n] - F[i]) for i in range(n)] 
# 与处理x同样方法处理F，但F的Si应当是0
dF_cal = Uncertainty('dF', np.array(dF), d_out=d_dF)
# 计算同时把单位转换到牛顿
dF_data = dF_cal.data_output()
# 其他物理量的数据处理,对于单次测量Si=0但uj存在
D_cal = Uncertainty('D', D, d_out=d_D)
D_data = D_cal.data_output()
L_cal = Uncertainty('L', L, d_out=d_L)
L_data = L_cal.data_output()
d = d_array - d0
d_cal = Uncertainty('d', d, d_out=d_d)
d_data = d_cal.data_output()
b_cal = Uncertainty('b', b, d_out=d_b)
b_data = b_cal.data_output()

E = np.divide(8*dF_data['mean']*L_data['mean']*D_data['mean'],
              np.pi * (d_data['mean'])**2 * b_data['mean'] * dx_data['mean'])
# 杨氏模量E的计算公式
E = E * 1E6 # 统一化单位

Er_E = np.sqrt(
    L_data['E']**2 + D_data['E']**2 + b_data['E']**2 
    + 4*d_data['E']**2 + dx_data['E']**2 + dF_data['E']**2)
U_E = E * Er_E
# 杨氏模量E的不确定度计算公式
E_data = pd.Series([E, U_E, Er_E], index=['mean', 'U', 'E'])


# 数据汇总与输出
index_value = ['F', 'L', 'D', 'b', 'd', '∆x']
data_output_1 = pd.DataFrame(
    [dF_data, L_data, D_data,
     b_data, d_data, dx_data],
    index=index_value
)

# 图解法处理杨氏模量
# 线性拟合
P_linear, R2 = linear(F, x_mean)
xx = np.arange(np.min(F), 
               np.max(F), 0.1)
yy = np.polyval(P_linear, xx)

# 作图
plt.figure(1,(25,16))
plt.rcParams['font.family'] = 'Arial Unicode MS'
plt.rcParams['font.size'] = 22
# 调整matplotlib内部设置使之支持中文,这种方法改变全局设置
plt.plot(F, x_mean, 'bo', label='实验数据点', markersize=15)
plt.plot(xx, yy, 'r-.', label='拟合曲线', linewidth=4)
plt.xlabel(u'F / N', fontsize=24)
plt.ylabel(u'x / cm', fontsize=24)
plt.title('钢丝伸长量x随拉力F的变化曲线', fontsize=30)

# 拟合线描述图例
txt_point = (F[7], x_mean[5])
# 相对点法
msg = '拟合方程: y = {:.5g} x + {:.5g}\n     R2 = {:.4f}'.format(
    P_linear[0], P_linear[1], R2)
plt.annotate(msg, xy=txt_point, xytext=txt_point, fontsize=26)

# 数据输出
output_file = '{}/拉伸杨氏_output.txt'.format(path)
sep = '\t'  # 设置to_csv的sep参数

with open(output_file, 'w') as f:
    f.write('{:<26}'.format('拉伸杨氏数据处理结果:'))
    f.write('\n----------------\n')
    f.write('逐差法数据初步处理:\n')
data_F_x.to_csv(output_file, mode='a', sep=sep, float_format="%4.4g")

with open(output_file, 'a') as f:
    f.write('{}组逐差dx的数据如下\n'.format(n))
    for i in dx:
        f.write('{:.8f} cm \n'.format(float(i)))
    f.write('\n逐差法中各测量数据的处理结果:\n')
data_output_1.to_csv(output_file, sep=sep, mode='a', float_format="%8.4g")
# 注意df.to_csv里面也有很多可控参数的

with open(output_file, 'a') as f:
    f.write('\n----------------\n')
    f.write('杨氏模量E及其不确定度U,Er:\n')
E_data.to_csv(output_file, mode='a', sep=':', float_format="%14.6g")

with open(output_file, 'a') as f:
    f.write('\n----------------\n')
    f.write('图解法处理杨氏模量，作x~F图的结果:\n')
    msg1 = '拟合方程:\n   x = {:.6g} F + {:.6g}\n'.format(P_linear[0], P_linear[1])
    msg2 = '拟合系数R2: {:.6f}\n'.format(R2)
    msg3 = '此处斜率单位为cm/9.8N,数据处理后有:\n'
    k = np.divide(8 * L_data['mean'] * D_data['mean'],
                  P_linear[0] * np.pi * d_data['mean']**2 * b_data['mean'])
    # 杨氏模量计算公式 注意k=dx/df
    k = k * 1E6  # 化单位
    msg4 = '杨氏模量值: {:.6g}\n'.format(k)
    msg5 = '未标注单位的均为国际制单位\n'
    f.write(msg1+msg2+msg3+msg4+msg5)

# 出图设置
plt.grid()
plt.legend()
plt.savefig('{}/拉伸杨氏.png'.format(path))
print('数据处理文件和所得图像均已保存')
# plt.show()
print('well done!')
