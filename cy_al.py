# 环己烷乙醇恒压汽液平衡相图绘制
# JamesBourbon in 20191111
import numpy as np
import matplotlib.pyplot as plt
import sqlite3 # 数据库应用
import pandas as pd
import os
from scipy import interpolate  # 插值

path = os.getcwd()
input_file = "{}/cy_al_input.csv".format(path)
# 实验数据读入(两组)
data = pd.read_csv(input_file, index_col=0)
# 气相部分的折射率平均值
zsl_g = str(data['values']['zsl_g'])
# 液相部分的折射率平均值
zsl_l = str(data['values']['zsl_l'])
# 沸点读数值
t_bp_obs = np.float64(data['values']['t_bp_obs'])
# 外温度计对应测出的环境温度
t_env = np.float64(data['values']['t_env'])
t_0 = np.float64(data['values']['t_0']) 
# 橡胶管处的温度值
p_env = np.float64(data['values']['p_env'])
# 由气压计读出的环境大气压
t_p = np.float64(data['values']['t_p'])
# 由气压计读出的温度值
delta_t_1 = np.float64(data['values']['delta_t_1'])
# 温度计示值较正值

# 导入温度较正和压力较正函数
# 此处所有的p用kpa作单位
def p_refine(pt, t0, delta_2=0.01):
    # pt 为大气压值
    delta_1=(0.0001631 * t0 * pt) / (1 + 0.0001815 * t0)
    print("\n压力较正值: {}".format(delta_1))
    p_real = pt - delta_1 - delta_2
    return p_real

def t_refine(t_obs, t_env, t0, delta_1=delta_t_1):
    # t0为橡胶口处温度,直接读出, t_obs-t0为露茎长度值 
    # delta_1 为示值较正温度
    # t_obs, t_env为np.array数组
    delta_2 = 0.00016 * (t_obs-t0) * (t_obs - t_env)
    # 露茎较正项
    print('\n露茎较正值(对应各组数据):\n {}'.format(delta_2))
    t_real = t_obs + delta_1 + delta_2
    return t_real

def t_1atm(t_real, p0_real, xb_g):
    # 将温度较正到101.325kpa下温度，输入的p以kpa为单位
    # 计算时再将p转化为Pa
    p0 = p0_real * 1E3
    t_1atm = t_real + (0.0712+0.0234*xb_g)*(t_real+273)*(101325-p0)/p0
    print('平衡温度较正值:{}'.format(t_1atm))
    return t_1atm

# 用折射率数据和书后附录表格来确定环己烷的摩尔分数的函数
# 这个方法已经不用了，只是留着它，作为一个数字分离的样本
def xb_point(data_zsl):
    xb = []
    with open('cy_al_bal.csv', 'r') as f:
        data_xb = f.readlines()    
    for i in data_zsl:
        ia = round(i-5E-4, 3)
        ib = round((i - ia) * 1E4)      
        for line in data_xb[1:]:
            line = line.strip()
            line = line.split(',')
            if line[0] == str(ia):
                xb.append(float(line[ib+1]))
    return np.array(xb, dtype=np.float64)

def xb_get(str_zsl):
    # 用数据库的方法来读入附录
    # 针对单个折射率换算到组成的函数，输入为数字字符串
    index_column = str_zsl[-1]
    index_raw = str_zsl[0:-1]
    # 分开两值
    db_name = 'cy_al_bal.db'
    conn = sqlite3.connect(db_name)
    SQL = 'select "{}" from main where 折射率={}'.format(index_column, index_raw)
    # 此处单引号和双引号别乱用，我们写的是SQL语句
    x_get = list(conn.execute(SQL))
    x_get = np.array(x_get, dtype=np.float64)
    x_get = np.float64(x_get)
    # 连续转化，确保最后return的是个数
    # 这是numpy相比matlab的一大缺陷
    return x_get

def point_tick(ord_point, position_d=(0, 0)):
    # position_d标注点相对于该点的坐标偏差
    ord_point = np.array(ord_point)
    position_d = np.array(position_d)
    msg = '({:.3f},{:.2f})'.format(ord_point[0], ord_point[1])
    plt.annotate(msg, xy=ord_point, xytext=ord_point + position_d)
    
# 开始数据处理
# xb_g = xb_point(data_zsl=zsl_g)
xb_g = xb_get(str_zsl = zsl_g) # 懒得用yb替换了
print('气相环己烷摩尔分数:{}'.format(xb_g))
# xb_l = xb_point(data_zsl=zsl_l)
xb_l = xb_get(str_zsl = zsl_l)
print('液相环己烷摩尔分数:{}'.format(xb_l))
t_real = t_refine(t_bp_obs, t_env, t_0)
p0 = p_refine(p_env, t_p)
t_use = t_1atm(t_real, p0, xb_g)

# 标准曲线的数据读取：用数据库实现
conn_std = sqlite3.connect('cy_al_std.db')
SQL_std = 'select * from std'
std_list = list(conn_std.execute(SQL_std))
std_data = np.array(std_list, dtype=np.float64)
xb_l_std = std_data[:,0]
xb_g_std = std_data[:,1]
t_use_std= std_data[:,2]

# 对标准曲线进行平滑化:二阶样条曲线插值
xb_l_stds = np.linspace(np.min(xb_l_std), np.max(xb_l_std), 100)
f = interpolate.interp1d(xb_l_std, t_use_std, kind='quadratic')
t_use_std_l = f(xb_l_stds)
xb_g_stds = np.linspace(np.min(xb_g_std), np.max(xb_g_std), 100)
f = interpolate.interp1d(xb_g_std, t_use_std, kind='quadratic')
t_use_std_g = f(xb_g_stds)

# 作图
plt.figure(figsize=(25,16))
plt.rcParams['font.family'] = 'Arial Unicode MS'
plt.rcParams['font.size'] = 18
# 调整matplotlib内部设置使之支持中文,这种方法改变全局设置


# 设置坐标轴范围
x_min = -0.05
y_min = 63.50
x_max = 1.05
y_max = 82.50
x_delta = 0.05
y_delta = 1.00
plt.xlim((x_min, x_max))
plt.ylim((y_min, y_max))
# 设置坐标轴刻度
my_x_ticks = np.arange(x_min, x_max, x_delta)
my_y_ticks = np.arange(y_min, y_max, y_delta)
plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)

plt.plot(xb_l, t_use, 'g>', label='液相数据点', markersize=14)
plt.plot(xb_l_stds, t_use_std_l, 'b-', label='液相标准线', linewidth=3,)
plt.plot(xb_l_std, t_use_std, 'bo', label='液相标准点', markersize=14,)
plt.plot(xb_g ,t_use, 'gs', label='气相数据点', markersize=14)
plt.plot(xb_g_stds, t_use_std_g, 'r-.', label='气相标准线', linewidth=3,)
plt.plot(xb_g_std, t_use_std, 'ro', label='气相标准点', markersize=14,)
plt.xlabel(u'x_(环)[y_(环)]', fontsize=20)
plt.ylabel(u't_常 / ℃', fontsize=20)
plt.title('环己烷-乙醇恒压汽液平衡相图', fontsize=26)

x0 = [xb_l, xb_g]
y0 = np.array([t_use, t_use], dtype=np.float64)
for i in range(len(x0)):
    ord_point = (float(x0[i]), float(y0[i]))
    point_tick(ord_point,position_d=(-0.109, -0.15))
# 对每个点标注图例

msg = 'P = 101.325 kPa'
msg_point = [xb_g_std[-4], t_use_std[-1]]
plt.annotate(msg, xy=msg_point, xytext=msg_point, fontsize=22)


plt.legend()
plt.grid()
plt.savefig('{}/环己烷乙醇.png'.format(path))
# plt.show()
