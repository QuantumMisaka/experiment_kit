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

if __name__ == "__main__":
    x_str = input('请输入需要拟合的x值[空格隔开]:\n')
    y_str = input('请输入需要拟合的y值[空格隔开]:\n')
    try:
        x_str = x_str.strip()
        x_dir = x_str.split()
        x = np.array(x_dir, dtype=np.float64)
        y_str = y_str.strip()
        y_dir = y_str.split()
        y = np.array(y_dir, dtype=np.float64)
    except:
        print('输入错误！请重新再来!')
    else:
        P_linear, R2 = linear(x, y)
        xx = np.linspace(np.min(x), np.min(y),100)
        yy = np.polyval(P_linear, xx)
        # 作图
        plt.rcParams['font.family'] = 'Arial Unicode MS'
        plt.rcParams['font.size'] = 16
        # 调整matplotlib内部设置使之支持中文,这种方法改变全局设置
        plt.plot(x, y, 'bo', label='实验数据点', markersize=12)
        plt.plot(xx, yy, 'r-.', label='拟合曲线', linewidth=3)
        plt.xlabel(r'x^2 / cm^2', fontsize=20)
        plt.ylabel(r'I / Kg·m^2', fontsize=20)
        plt.title('平行轴定理验证实验曲线图', fontsize=26)

        # 拟合线描述图例
        txt_point = (np.mean(x), np.mean(y[y>=np.mean(y)]))
        # 相对点法
        msg = '拟合方程: y = {:g} x + {:g}\n     R2 = {:.4f}'.format(
            P_linear[0], P_linear[1], R2)
        plt.annotate(msg, xy=txt_point, xytext=txt_point)

        # 出图设置
        plt.grid()
        plt.legend()
        plt.show()
        
