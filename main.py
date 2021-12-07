import numpy, colorama, cv2, time
from PIL import Image


b = []
para_name = ['Us','Z','Is','Id']
im1 = Image.open(r'D:\\Projects\\Programs\\Python\\circuit-analysis\\circuit.jpg')
im2 = Image.open(r'D:\\Projects\\Programs\\Python\\circuit-analysis\\branch.jpg')
colorama.init(autoreset=True)


class branch():
    """支路"""

    para = []

    def focus(self, index, back = 41):
        #让用户注意的文本/序号
        if isinstance(index,int) and index <= 6 and index >= 0:
            return "\033[1;" + str(29+index) + ";" + str(back+index-1) + "m " + str(index) + " \033[0m"
        else:
            return "\033[0;30;" + str(back) + "m " + str(index) + " \033[0m"

    def check(self,val):
        return isinstance(val,int)

    def __init__(self, index):
        #为支路初始化参数
        self.index = index
        print("现在开始初始化第" + self.focus(index) + "号支路参数！\n" + self.focus("本程序独立源请使用相量输入"))
        print("当前支路为第" + self.focus(index) + "号支路")
        print("请按" + self.focus("一般支路关联参考方向定义",47) + "顺序输入当前第" + self.focus(index) + "号支路参数")
        for j in range(4):
            print("如果当前支路中不存在该参数，请输入0")
            print("注意:如果忘记支路编号，请输入circuit获取详情")
            print("注意:如果不是很了解一般支路，请输入branch获取详情")
            print(para_name[j] + str(index) + "=")
            if j <= 2:#阻抗+独立源
                temp = []#a+bj
                c_l = ['实', '虚' ]
                for  k in range(2):
                    while True:
                        print('请输入' + para_name[j] + str(index) + '的' + c_l[int(k)] + '部')
                        Z_temp = input(">>>")
                        if Z_temp == 'circuit':
                            im1.show()
                        elif Z_temp == "branch":
                            im2.show()
                        else:
                            try:
                                Z_temp = float(Z_temp)
                            except ValueError :
                                print("请正确输入参数或获取帮助！")
                            else:
                                temp.append(Z_temp)
                                break
            else:#受控源
                temp = []
                para_temp = ['类型\n1--VCCS\t2--CCCS', '控制量所在支路（数字）', '控制量所在详细位置', '控制系数']
                for k in range(4):
                    print('请输入受控源Id'+ str(index) + '的' + para_temp[int(k)])
                    while True:
                        
                        
                        if k == 2:
                            im2.show()
                            if temp[0] == 1:
                                print('请注意按照图中给出的参考方向输入！！\n1--Uk\t2--Uek\t3--Usk'.replace('k',str(int(temp[1]))))
                            else:
                                print('请注意按照图中给出的参考方向输入！！\n1--Ik\t2--Iek\t3--Idk'.replace('k',str(int(temp[1]))))
                        Z_temp = input(">>>")
                        if Z_temp == 'circuit':
                            im1.show()
                        elif Z_temp == "branch":
                            im2.show()
                        else:
                            try:
                                Z_temp = float(Z_temp)
                                if Z_temp == 0:
                                    raise ValueError
                            except ValueError :
                                print("请正确输入参数或获取帮助！")
                            else:
                                temp.append(Z_temp)
                                break


print("请注意本程序\033[0;30;47m仅\033[0m可处理如图所示拓扑结构电路（支路编号、方向及结点编号已给出）")
time.sleep(2)
im1.show()

for i in range(1,7):
    #初始化支路类
    b.append(branch(i))
