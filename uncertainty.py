import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Uncertainty():
    
    def __init__(self, name, data_raw, d_out, d_type='u'):
        # d_out 仪器误差; name为物理量名
        self.name = name
        self.data_raw = np.array(data_raw)
        self.n = len(data_raw)
        if self.n > 1:
            self.data_pro = pd.Series(data_raw).describe()
            print('\n物理量{}数据基本处理:\n{}'.format(self.name, self.data_pro))
            self.data_mean = self.data_pro['mean']
            self.data_std = self.data_pro['std']
            self.data_mean_std = np.divide(self.data_std, np.sqrt(self.n))
            print('平均值的标准偏差: {:.5e}'.format(self.data_mean_std))
            self.Si = self.deviation_A()
        if self.n == 1:
            self.data_mean = self.data_raw
            self.data_mean_std = 0
            self.Si = 0
        self.uj = self.deviation_B(d_out=d_out, d_type=d_type)
        self.data_U = np.sqrt(
            np.add(np.power(self.Si, 2), np.power(self.uj, 2)))
        # 上式即不确定度的A,B分量合成
        self.data_E = np.divide(self.data_U, self.data_mean)
        # 相对不确定度 = 不确定度/样本均值 类似于相对标准偏差

    def __str__(self):
        # 用data_ex类存储实验结果最终的数据处理信息，包括平均值和不确定度
        result = '物理量{}测量结果:\n平均值:{}\n不确定度:{:4g}\n相对不确定度:{:4g}%\n'.format(
            self.name, self.data_mean, self.data_U, 100*self.data_E)
        msg = '''注意有效数字: 不确定度只进不舍，首位数字 >=3 取一位，否则取两位\n以上计算基于90%的置信度\n'''
        return result+msg

    def deviation_A(self):
        self.tpn_dir = {1: 0, 2: 1.84, 3: 1.32, 4: 1.20,
                        5: 1.14, 6: 1.11, 7: 1.09,
                        8: 1.08, 9: 1.07, 10: 1.06, }
        # 置信度因子tp(n-1)的表格值，注意n-1才是计算所用的统计自由度
        Si = np.multiply(self.tpn_dir[self.n], self.data_mean_std)
        return Si
        # 此处的Si即为不确定度的A分量，指可以通过统计确定的标准偏差值
        # A类分量即为可用统计方法计算出来的标准误差

    def deviation_B(self, d_out, d_type='u'):
        # d_out指仪器误差，此处计算不确定度的B分量
        # 不确定度的B类分量即其他方法估计的"等价标准误差",用仪器误差限近似
        if d_type == 'n':
            uj = d_out/3
            # 正态分布的B类分量计算
        else:
            uj = 0.683*d_out
            # 均匀分布的B类分量计算
        return uj

    def data_output(self):
        # 返回结果的平均值,各类不确定度和总不确定度
        ls = np.array([
            np.float64(self.data_mean), np.float64(self.data_U), 
            np.float64(self.data_E), np.float64(self.Si), 
            np.float64(self.uj),
                ],dtype=np.float64)
        # 需要做一次变量类型转换，把值从ndarray里面取出来
        out = pd.Series(ls, index=['mean', 'U', 'E', 'Si', 'uj'])
        out = out.fillna(0) # 再次去掉可能的nan值
        return out

if __name__ == "__main__":
    name = input('请输入物理量名称: ')
    x_str = input('请输入需要求不确定度的各值[空格隔开]:\n')
    d_out = eval(input('请输入仪器误差值: '))
    try:
        x_str = x_str.strip()
        x_dir = x_str.split()
        x = np.array(x_dir, dtype=np.float64)
    except:
        print('输入错误！请重新再来!')
    else:
        x_cal = Uncertainty(name, x, d_out=d_out)
        print('不确定度处理结果')
        x_data = x_cal.data_output()
        print(x_data)
        

