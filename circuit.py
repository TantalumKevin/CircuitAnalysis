import numpy, colorama, time, os
from PIL import Image


b = []
path = __file__.replace("circuit.py","")
para_name = ['Us','Z','Is','Id']
im1 = Image.open(path + 'circuit.jpg')
im2 = Image.open(path + 'branch.jpg')
colorama.init(autoreset=True)

class valuerror(RuntimeError):#自定义错误类型，辅助构建受控源输入
    def __init__(self):
        pass


class branch(): #支路类定义

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
        self.para = []

        print("现在开始初始化第" + self.focus(index) + "号支路参数！\n" + self.focus("本程序独立源请使用相量输入"))
        print("当前支路为第" + self.focus(index) + "号支路")
        print("请按" + self.focus("一般支路关联参考方向定义",47) + "顺序输入当前第" + self.focus(index) + "号支路参数")
        print("如果当前支路中不存在该参数，请输入0")
        print("注意:如果忘记支路编号，请输入circuit获取详情")
        print("注意:如果不是很了解一般支路，请输入branch获取详情\n")
        for j in range(4):
            print(para_name[j] + str(index) + "=")
            if j <= 2:#阻抗+独立源
            #a+bj
                while True:
                    print('请严格按照"1+2j"的形式输入' + para_name[j] + str(index))
                    temp = input(">>>")
                    if temp == 'circuit':
                        im1.show()
                    elif temp == "branch":
                        im2.show()
                    else:
                        try:
                            temp = complex(temp)
                        except ValueError :
                            print("请正确输入参数或获取帮助！")
                        else:
                            break
                print('\n' + para_name[j] + str(index) + " = " + str(temp) + '\n')

            else:#受控源
                temp = []
                para_temp = ['类型\n0--不存在   1--VCCS   2--CCCS', '控制量所在支路（数字）', '控制系数']
                if self.index == 1:
                    im2.show()
                print(self.focus("请注意，受控源控制量仅能来自于Uek或Iek(参考方向如图)",47))
                for k in range(3):
                    try:
                        if temp[0] == 0:
                            print(temp[0])
                            raise valuerror
                    except valuerror:
                        break
                    except IndexError:
                        pass
                    else:
                        pass
                    print('请输入受控源Id'+ str(index) + '的' + para_temp[int(k)])
                    while True:
                        Z_temp = input(">>>")
                        if Z_temp == 'circuit':
                            im1.show()
                        elif Z_temp == "branch":
                            im2.show()
                        else:
                            try:
                                Z_temp = float(Z_temp)
                                if int(k) == 0 and Z_temp not in [0.0,1.0,2.0] :
                                    raise ValueError
                            except ValueError :
                                print("请正确输入参数或获取帮助！")
                            else:
                                if Z_temp == 0:
                                    temp = [0, 0]
                                else:
                                    temp.append(Z_temp)
                                break
            
                if temp[0] != 0:
                    output = '\nId' + str(self.index) + ' = ' + str(temp[2]) + ['Uek',"Iek"][int(temp[0] - 1)].replace('k', str(int(temp[1])) + '\n')
                    print(output)
            
            self.para.append(temp)

    def show(self):
        print('\n')
        for j in range(4):
            if j <= 2:#阻抗+独立源
                print(para_name[j] + str(self.index) + " = " + str(self.para[j]))
            else:
                if len(self.para[j]) == 2:
                    print(para_name[j] + str(self.index) + " = 0")
                else:
                    output = 'Id' + str(self.index) + ' = ' + str(self.para[j][2]) + ['Uek',"Iek"][int(self.para[j][0] - 1)].replace('k', str(int(self.para[j][1])) + '\n')
                    print(output)
        print('\n')


def mag_ind():#是否有耦合电感

    print('支路间是否含有耦合电感？')
    print('1--没有\t 2--有')
    while True:
        cmd = input(">>>")
        try:
            cmd = int(cmd)
            if cmd != 1 and cmd !=2:
                raise ValueError
        except ValueError :
            print("请正确输入指令！")
        else:
            break
    if cmd - 1:
        print("请输入当前电路输入频率(单位：Hz)")
        f = input(">>>")
        w = float(f) / 2 / 3.1415926535
        print("请输入耦合电感数量（单位：对）")
        num = input(">>>")
        L_list = []
        for i in range(int(num)):
            print("请输入第i对耦合电感所在支路及互感系数：".replace('i',str(i+1)))
            print("输入示例：-2 4 0.2")
            print("前两个数字表示支路所在标号，负号表示同名端\033[0;30;47m非\033[0m电源流入端\n第三个数字表示互感系数\033[0;30;47m(请注意用空格隔开三个数字)\033[0m\n（电流参考方向请输入‘branch’查看）")
            temp = []
            in_str = ''
            while True:
                temstr = input(">>>")
                if temstr == '':
                    print(1)
                    in_str = ''
                else:
                    in_str = in_str + temstr

                if in_str == 'circuit':
                    im1.show()
                elif in_str == "branch":
                    im2.show()
                else:
                    str_list = in_str.split(" ")

                    if len(str_list) < 3:
                        in_str += ' '
                        print('参数输入缺失，请按顺序继续输入！\n如需重新输入请直接按下回车键清零当前数据')
                        continue
                    elif len(str_list) > 3:
                        print('参数输入溢出，请重新输入！')
                        in_str = ''
                        continue

                    try:
                        for j in range(2):
                            temp.append(int(str_list[j]))
                        temp .append(float(str_list[2]))
                    except ValueError :
                        print("请正确输入参数或获取帮助！")
                    else:
                        L_list.append(temp)
                        break
        print(L_list)
        return int(num), w, L_list
    else:
        return 0, 0, []
