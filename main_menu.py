from tkinter import *
from tkinter.messagebox import *
import os

# update in 20191211

#大物实验调用模块
def young_s():
    def yunxing():
        os.system('python lsys.py')
    
    root_young_s = Tk()
    
    root_young_s.title("拉伸杨氏")
    showinfo("Young's",'''
    请按Readme.me的要求
    在当前目录下准备好两个文件名分别为
    拉伸杨氏_input_1.csv, 拉伸杨氏_input_2.csv
    的输入文件。准备好之后请点击确认处理。
    ''')
    btn_y = Button(root_young_s,
                     text = '确认处理',
                     width = 20,
                     height = 5,
                     command = yunxing,
                     state = 'normal'
                     )
    btn_y.pack()
    
        
    root_young_s.mainloop()

def niubai():
    def yunxing():
        os.system('python niubai.py')
    
    root_niubai = Tk()
    
    root_niubai.title("扭摆法")
    showinfo("NiuBai",'''
    请按Readme.me的要求
    在当前目录下准备好两个文件名分别为
    扭摆_input_1.csv, 扭摆_ninput_2.csv
    的输入文件。准备好之后请点击确认处理。
    ''')
    btn_n = Button(root_niubai,
                     text = '确认处理',
                     width = 20,
                     height = 5,
                     command = yunxing,
                     state = 'normal'
                     )
    btn_n.pack()
    
        
    root_niubai.mainloop()

def bohr():
    def yunxing():
        os.system('python begz.py')
    
    root_bohr = Tk()
    
    root_bohr.title("波尔共振")
    showinfo("Bohr",'''
    请按Readme.me的要求
    在当前目录下准备好三个文件名分别为
    受迫震荡_input.csv,自由震荡_input.csv,阻尼震荡_input.csv
    的输入文件。准备好之后请点击确认处理。
    ''')
    btn_b = Button(root_bohr,
                     text = '确认处理',
                     width = 20,
                     height = 5,
                     command = yunxing,
                     state = 'normal'
                     )
    btn_b.pack()   
    root_bohr.mainloop()
    
def kelvins():
    def yunxing():
        os.system('python dianqiao.py')
    
    root_kelvins = Tk()
    
    root_kelvins.title("开尔文电桥")
    showinfo("Kelvins",'''
    请按Readme.me的要求
    在当前目录下准备好文件名为
    电桥_input.csv
    的输入文件。准备好之后请点击确认处理。
    ''')
    btn_k = Button(root_kelvins,
                     text = '确认处理',
                     width = 20,
                     height = 5,
                     command = yunxing,
                     state = 'normal'
                     )
    btn_k.pack()   
    root_kelvins.mainloop()

#物化实验调用模块
def rsr():
    def yunxing():
        os.system('python rsr.py')
    
    root_rsr = Tk()
    
    root_rsr.title("拉伸杨氏")
    showinfo("燃烧热",'''
    请按Readme.me的要求
    在当前目录下分别准备好文件名为
    燃烧热_input_1.csv, 燃烧热_input_2.csv
    的输入文件。准备好之后请点击确认。
    ''')
    btn_r = Button(root_rsr,
                     text = '确认处理',
                     width = 20,
                     height = 5,
                     command = yunxing,
                     state = 'normal'
                     )
    btn_r.pack()
    root_rsr.mainloop()


def cyal():
    def yunxing():
        os.system('python cy_al.py')

    root_rsr = Tk()

    root_rsr.title("拉伸杨氏")
    showinfo("环己烷乙醇", '''
    请按Readme.me的要求
    在当前目录下准备好文件名为
    cy_al_input.csv
    的输入文件。准备好之后请点击确认。
    ''')
    btn_r = Button(root_rsr,
                   text='确认处理',
                   width=20,
                   height=5,
                   command=yunxing,
                   state='normal'
                   )
    btn_r.pack()
    root_rsr.mainloop()

#主界面模块
def physical():
    root_phy = Tk()
    root_phy.title("大学物理实验")
    
    btn_young_s = Button(root_phy,
                     text = '拉伸法求杨氏模量的实验数据处理',
                     width = 40,
                     height = 5,
                     command = young_s,
                     state = 'normal'
                     )
    btn_young_s.pack()
    
    btn_young_s = Button(root_phy,
                     text = '波尔共振的实验数据处理',
                     width = 40,
                     height = 5,
                     command = bohr,
                     state = 'normal'
                     )
    btn_young_s.pack()
    
    btn_young_s = Button(root_phy,
                     text = '扭摆法验证平行轴定理的线性拟合',
                     width = 40,
                     height = 5,
                     command = niubai,
                     state = 'normal'
                     )
    btn_young_s.pack()
    
    btn_young_s = Button(root_phy,
                     text = '开尔文电桥线性拟合求电阻率',
                     width = 40,
                     height = 5,
                     command = kelvins,
                     state = 'normal'
                     )
    btn_young_s.pack()
    
    root_phy.mainloop()
    
def phy_chem():
    root_phy_chem = Tk()
    root_phy_chem.title("物理化学实验")
    
    btn_rsr = Button(root_phy_chem,
                     text = '燃烧热实验的雷诺拟合',
                     width = 40,
                     height = 5,
                     command = rsr,
                     state = 'normal'
                     )
    btn_rsr.pack()
    btn_cyal = Button(root_phy_chem,
                      text='环己烷_乙醇恒压汽液平衡相图的测绘',
                      width=40,
                      height=5,
                      command=cyal,
                      state='normal'
                      )
    btn_cyal.pack()
    root_phy_chem.mainloop()

def linear():
    print('-----数据的线性拟合模块------')
    print('            --- by JamesBourbon')
    os.system('python statistic_model.py')
    
def uncertainty():
    print('-----不确定度统计计算模块------')
    print('            --- by JamesBourbon')
    os.system('python uncertainty.py')

#菜单调用模块
def about():
    showinfo("软件信息",'''
    此projects原作者: JamesBourbon's team
    转载请注明出处
    有各种意见建议欢迎mail: ff6757442@163.com
    祝您使用愉快!    
    ''')

#主窗口
def main():
    root = Tk()
    root.title("Experiment_Kit")

    menubar = Menu(root)

    helpmenu = Menu(menubar,tearoff=0)
    helpmenu.add_command(label="关于",command=about)
    helpmenu.add_separator()
    helpmenu.add_command(label="关闭",command=root.destroy)
    menubar.add_cascade(label="帮助",menu=helpmenu)

    root.config(menu = menubar)

    btn_physical = Button(root,
                        text = '大物实验数据处理',
                        width = 40,
                        height = 5,
                        command = physical,
                        state = 'normal'
                        )
    btn_physical.pack()

    btn_phy_chem = Button(root,
                        text = '物化实验数据处理',
                        width = 40,
                        height = 5,
                        command = phy_chem,
                        state = 'normal'
                        )
    btn_phy_chem.pack()

    btn_linear = Button(root,
                        text = '单组数据统计的与不确定度计算',
                        width = 40,
                        height = 5,
                        command = linear,
                        state = 'normal'
                        )
    btn_linear.pack()

    btn_uncertainty = Button(root,
                        text = '两组数据的线性拟合和作图',
                        width = 40,
                        height = 5,
                        command = uncertainty,
                        state = 'normal'
                        )
    btn_uncertainty.pack()

    showinfo("Welcome",'''
    -------Welcome to experiment_kit v0.10------
    ------Let's get great experiment results------
    ------just passing some simple steps------
    ------under the help of our Python program!------

        When using this program, be sure that
    --  YOU ARE AWARE THAT WHAT YOU ARE DOING.  --
    --  AND FOLLOW THE TIPS IN Readme.md  ----
        otherwise, you will get negative result.
    ''')

    root.mainloop()
    
if __name__ == "__main__":
    start = main() # 执行main函数！
