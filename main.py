import numpy, colorama, time, circuit


b = []
colorama.init(autoreset=True)


print("请注意本程序\033[0;30;47m仅\033[0m可处理如图所示拓扑结构电路（支路编号、方向及结点编号已给出）")
time.sleep(2)
#circuit.im1.show()


for i in range(1,7):
    #初始化支路类
    b.append(circuit.branch(int(i)))
    b[i-1].show()


num, ml = circuit.mag_ind()#检测是否有耦合电感

#电路分析

