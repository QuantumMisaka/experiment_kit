#--*-- coding utf-8 --*--
# experiment_kit的主调用函数
# JamesBourbon in 20191211

import os

class Main():
    def __init__(self):
        self.welcome()
        self.control_count = 0 # 控制容错次数
        self.key_main = input('\n') # 控制流参数
        self.main_control()
        self.end_message()
        
        super().__init__()
        
    def welcome(self):
        self.msg1 = '''
-------Welcome to experiment_kit v0.10------
------Let's get great experiment results------
------just passing some simple steps------
------under the help of our Python program!------

    When using this program, be sure that
--  YOU ARE AWARE THAT WHAT YOU ARE DOING.  --
--  AND FOLLOW THE TIPS IN Readme.md  ----
    otherwise, you will get negative result.
'''
        self.msg2 = '''
Please enter the processing mode:
1. 大物实验数据处理
2. 物化实验数据处理
3. 单组数据统计的与不确定度计算
4. 两组数据的线性拟合和作图

输入q可以退出程序
'''
        print(self.msg1 + self.msg2)
        
    def main_control(self):
        if self.key_main == '1':
            self.physical_experiment()
        elif self.key_main == '2':
            self.phy_chem_experiment()
        elif self.key_main == '3':
            self.uncertainty()
        elif self.key_main == '4':
            self.linear()
        elif self.key_main == 'q':
            return
        else:
            self.control_count += 1
            if self.control_count >= 3:
                print('请思考清楚再运行这个程序!谢谢！')
                return
            else:
                print('请正确输入处理模块代号!')
                print(self.msg2)
                self.key_main = input('请输入您想运行的模块代号:')
                self.main_control()
        # next = Main()                
                
    def physical_experiment(self):
        Go = PhysicalExperiment()
    
    def phy_chem_experiment(self):
        Go = PhyChem()
    
    def linear(self):
        print('-----数据的线性拟合模块------')
        print('            --- by JamesBourbon')
        os.system('python statistic_model.py')
    
    def uncertainty(self):
        print('-----不确定度统计计算模块------')
        print('            --- by JamesBourbon')
        os.system('python uncertainty.py')
        
    def end_message(self):
        msg = '''
此projects原作者: JamesBourbon's team
转载请注明出处
有各种意见建议欢迎mail: ff6757442@163.com
祝您使用愉快!    
''' 
        print(msg)
    
    
class PhysicalExperiment():
    def __init__(self):
        self.count = 0
        self.msg_start = '''
-------大学物理实验-------
目前可用功能选择:
1. 拉伸法求杨氏模量的实验数据处理
2. 波尔共振的实验数据处理
3. 扭摆法验证平行轴定理的线性拟合
4. 开尔文电桥线性拟合求电阻率

注意：在使用以上功能前需要提前在运行目录下准备好输入文件
具体要求参见Readme文件

输入q可以退出程序        
'''
        print(self.msg_start)
        self.main_control()
        
    def main_control(self):
        self.mode = input('请输入功能代号: ')
        if self.mode == '1':
            self.lsys()
        elif self.mode == '2':
            self.begz()
        elif self.mode == '3':
            self.niubai()
        elif self.mode == '4':
            self.dianqiao()
        elif self.mode == 'q':
            return
        else:
            self.count += 1
            print('请您输入正确的功能代号!')
            if self.count <= 3:
                self.main_control()
            else:
                print('Keep your mind next time!')
                return
        
    def lsys(self):
        msg = '''
请按Readme.md的要求
在当前目录下准备好两个文件名分别为
拉伸杨氏_input_1.csv, 拉伸杨氏_input_2.csv
的输入文件。准备好之后请输入go

'''
        preparation = input(msg)
        if preparation == 'go':
            os.system('python lsys.py')
        else:
            print('请在阅读Readme.md后运行程序, 谢谢合作!')
    
    def begz(self):
        msg = '''
请按Readme.md的要求
在当前目录下准备好文件名为
波尔共振_input_1.csv, 波尔共振_input_2.csv
的输入文件。准备好之后请输入go
'''
        preparation = input(msg)
        if preparation == 'go':
            os.system('python begz.py')
            print('运行错误！\n请在阅读Readme.md后运行程序, 谢谢合作!')
        else:
            print('请在阅读Readme.md后运行程序, 谢谢合作!')

    def dianqiao(self):
        msg = '''
请按Readme.md的要求
在当前目录下准备好文件名为
电桥_input.csv
的输入文件。准备好之后请输入go
'''
        preparation = input(msg)
        if preparation == 'go':
            os.system('python dianqiao.py')
        else:
            print('请在阅读Readme.md后运行程序, 谢谢合作!')
            
    def niubai(self):
        msg = '''
请按Readme.md的要求
在当前目录下分别准备好文件名为
扭摆_input_1.csv, 扭摆_input_2.csv
的输入文件。准备好之后请输入go
'''
        preparation = input(msg)
        if preparation == 'go':
            os.system('python niubai.py')
        else:
            print('请在阅读Readme.md后运行程序, 谢谢合作!')


class PhyChem():
    def __init__(self):
        self.count = 0
        self.msg_start = '''
-------物理化学实验-------
目前可用功能选择:
1. 燃烧热实验的雷诺拟合作图
2. 环己烷-乙醇恒压汽液平衡相图的测绘
（其他各功能陆续上线中）

注意：在使用以上功能前需要提前在运行目录下准备好输入文件
具体要求参见Readme文件

输入q可以退出程序        
'''
        print(self.msg_start)
        self.main_control()

    def main_control(self):
        self.mode = input('请输入功能代号: ')
        if self.mode == '1':
            self.rsr()
        elif self.mode == '2':
            self.cy_al()
        elif self.mode == 'q':
            return
        else:
            self.count += 1
            print('请您输入正确的功能代号!')
            if self.count <= 3:
                self.main_control()
            else:
                print('Keep your mind next time!')
                return
    
    def rsr(self):
        msg = '''
请按Readme.md的要求
在当前目录下准备好文件名为
燃烧热_input.csv
的输入文件。准备好之后请输入go

'''
        preparation = input(msg)
        if preparation == 'go':
            os.system('python rsr.py')                
        else:
            print('请在阅读Readme.md后运行程序, 谢谢合作!')
            
    def cy_al(self):
        msg = '''
请按Readme.md的要求
在当前目录下准备好文件名为
cy_al_input.csv
的输入文件。准备好之后请输入go

'''
        preparation = input(msg)
        if preparation == 'go':
            os.system('python cy_al.py')                
        else:
            print('请在阅读Readme.md后运行程序, 谢谢合作!')

        

if __name__ == "__main__":
    start = Main() # 执行main函数！
                
                
            


        
    
