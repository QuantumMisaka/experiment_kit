# ---   coding utf-8   ---
# 燃烧热实验数据处理与作图,改成文件input_output形式
# JamesBourbon in 20191210
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

# 数据输入
path = os.getcwd() # 获取当前执行路径
input_file = '{}/燃烧热_input.csv'.format(path)
data = pd.read_csv(input_file)
data.fillna(0) # 去NaN
Q_phcooh = np.float64(data['Q_phcooh'][0])
m_phcooh = np.float64(data['m_phcooh'][0])
m_nai = np.float64(data['m_nai'][0])
# 单个数据控制进入的方法如上
n_phcooh = np.array(data['n'], dtype=np.float64)
n_nai = np.array(data['n'], dtype=np.float64)
T_phcooh = np.array(data['T_phcooh'], dtype=np.float64)
T_nai = np.array(data['T_nai'], dtype=np.float64)

M_nai = 128.164 # g/mol,内置参数

T_env = 0 
# 此算法通过计算平均温度求环境温度
# 如果外读环境温度，需要在内部调整

# 对标准样的测定结果进行雷诺拟合并且作图；用类集成
class T_refine_plt():
    def __init__(self, name, n, T_get, T_env,):
        # 基本参数设置
        self.path = os.getcwd()
        self.name = name
        self.T = T_get
        self.n = n
        # 雷诺较正预处理：切线斜率求取
        self.P_linear1 = np.polyfit(
            self.n[0:10], self.T[0:10], 1)
        self.P_linear2 = np.polyfit(
            self.n[20:], self.T[20:], 1)
        # 反向用T拟合n，可以在插值的同时求出较正温度
        # 取n_fin=21,防止其在20处反应不完全
        self.P_in_change = np.polyfit(
            self.T[10:14], self.n[10:14], 3)
        # self.T_mean = T_env  环境温度的提取
        self.T_mean = (self.T[9]+self.T[20]) / 2
        self.n_mean = np.polyval(
            self.P_in_change, self.T_mean)
        # 求平均温度和平均温度对应位置
        
        self.main() # 在创建实例的同时执行所有操作
    
    def plt_setting(self):
        # 实验数据可视化的基本设置与基本图
        plt.rcParams['font.family'] = 'Arial Unicode MS'
        plt.rcParams['font.size'] = 18
        # 调整matplotlib内部设置使之支持中文,这种方法改变全局设置
        label_ex = '实验数据线'
        title_ex = '{}燃烧热测定过程的温度-时间图'.format(
            self.name)
        # 文本配置
        lw_exp = 5
        ms_exp = 12
        self.fig = plt.figure(figsize=(25,16))
        plt.plot(self.n, self.T, 'ro-',
                 linewidth = lw_exp, markersize = ms_exp, label = label_ex)
        plt.xlabel(u'n', fontsize=22)
        plt.ylabel(u'T / ℃', fontsize=22)
        plt.title(title_ex, fontsize=28)
        plt.grid(True)
        # 作图基本操作
    
    def linear_get_annotate(self):
        # 雷诺较正之后的结果可视化
        x_T1 = np.arange(self.n[8], self.n[-5], 1)
        x_T2 = np.arange(self.n[5], self.n[-7], 1)
        y_T1 = np.polyval(self.P_linear1, x_T1)
        y_T2 = np.polyval(self.P_linear2, x_T2)
        ord_A = np.array(
            [self.n_mean, np.polyval(self.P_linear1, self.n_mean)])
        ord_B = np.array(
            [self.n_mean, np.polyval(self.P_linear2, self.n_mean)])
        ord_text1 = np.array([self.n_mean, self.T_mean])
        # 写温差的位置
        ord_text2 = np.array([self.n[23], self.T[11]])
        # 写信息的位置
        self.delta_T = ord_B[1] - ord_A[1]
        # 较正温差求取
        lw_fit = 3
        label_math = '拟合较正线'
        plt.plot(x_T1, y_T1, 'b:', linewidth=lw_fit, )
        plt.plot(x_T2, y_T2, 'b:', linewidth=lw_fit, label=label_math)
        x_T_mean = [0, self.n_mean]
        y_T_mean = [self.T_mean, self.T_mean]
        plt.plot(x_T_mean, y_T_mean, 'b:', linewidth=lw_fit)
        # 温差与箭头标注
        tick_size = 24
        mes_AB = u'    ∆T = {:.4f}℃'.format(self.delta_T)
        plt.annotate(mes_AB, xy=ord_A, xytext=ord_text1, fontsize=tick_size,
                    arrowprops=dict(facecolor='black', shrink=2, width=1))
        plt.annotate('', xy=ord_B, xytext=ord_text1-np.array([0,0.4]),
             arrowprops=dict(facecolor='black', shrink=2, width=1))
        # -(0, 0.4)目的在于消去作图时arrow的起点间隔
        
        plt.legend(loc='best')
    
    def plt_tick(self):
        # 设置坐标轴范围，模拟坐标纸效果
        # 同时也可以保证有效数字和精度
        # 这个设置是对该project普适的
        x_blank = 1
        y_blank = 0.1
        x_min = self.n[0] - x_blank
        y_min = self.T[0] - y_blank
        x_max = self.n[-1] + x_blank
        y_max = self.T[-1] + y_blank
        x_delta = 1.00
        y_delta = 0.10
        plt.xlim((x_min, x_max))
        plt.ylim((y_min, y_max))
        # 设置坐标轴刻度
        my_x_ticks = np.arange(x_min, x_max, x_delta)
        my_y_ticks = np.arange(y_min, y_max, y_delta)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        
    def main(self):
        # 执行程序
        self.plt_setting()
        self.linear_get_annotate()
        self.plt_tick()
        plt.savefig('{}/{}燃烧热.png'.format(self.path, self.name))
        # 对象程序执行同时就保存图片

# 创建数据处理的实例，同时执行实例中全部操作
do_phcooh = T_refine_plt('苯甲酸', n_phcooh, T_phcooh, T_env)
do_nai = T_refine_plt('萘', n_nai, T_nai, T_env)

# 所得数据的处理
C_env = -Q_phcooh * m_phcooh/do_phcooh.delta_T
Q_nai = -C_env * (M_nai/m_nai) * do_nai.delta_T * 1E-3
Qp = Q_nai + (5-7) * 8.3145 * (T_nai[9]+273.15) * 1E-3 # 计算恒压反应热  

# 出数据
msg1 = '苯甲酸燃烧较正温差: ∆T1 = {} K\n'.format(do_phcooh.delta_T)
msg2 = '萘燃烧较正温差: ∆T2 = {} K\n'.format(do_nai.delta_T)
msg3 = '体系热容值: C = {} J/K\n'.format(C_env)
msg4 = '测得萘的恒容燃烧热: Qv = {} kJ/mol\n'.format(Q_nai)
msg5 = '燃烧反应: C10H8(s) + 7O2(g) --> 5CO2(g) + 4H2O(l)\n'
msg6 = '萘的恒压燃烧热: Qp = {} kJ/mol\n'.format(Qp)
msg = msg1 + msg2 + msg3 + msg4 + msg5 + msg6
with open('燃烧热_output.txt', 'w') as f:
    f.write(msg)
print('数据文件和作图结果均已保存在当前目录')
# plt.show()
print('done! ')
