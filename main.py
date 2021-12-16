import numpy as np, colorama, time, circuit, os


b = []
colorama.init(autoreset=True)
#para_name = ['Us','Z','Is','Id']
print("请注意本程序\033[0;30;47m仅\033[0m可处理如图所示拓扑结构电路（支路编号、方向及结点编号已给出）")
time.sleep(2)
circuit.im1.show()


for i in range(1,7):
    #初始化支路类
    b.append(circuit.branch(int(i)))
    b[i-1].show()


num, w, ml = circuit.mag_ind()#检测是否有耦合电感

#电路分析
#Z矩阵、Y矩阵
#Z


z = []#list
for i in range(6):
    temp = [0, 0, 0, 0, 0, 0]
    temp[i] = b[i].para[1]
    z.append(temp) 
Z = np.array(z, dtype = complex)
for i in range(num):
    Z[abs(ml[i][0]), abs(ml[i][1])] = 0 + w*ml[i][2]*1j
    Z[abs(ml[i][1]), abs(ml[i][0])] = 0 + w*ml[i][2]*1j

#Y
Y = np.linalg.inv(Z)
#受控源
for i in range(6):
    if b[i].para[3][0] == 0:
        continue
    elif b[i].para[3][0] == 1:
        #VCCS
        Y[i, int(b[i].para[3][1] - 1)] = b[i].para[3][2]
    else:#CCCS
        Y[i, int(b[i].para[3][1] - 1)] = Y[int(b[i].para[3][1] - 1),int(b[i].para[3][1] - 1)] * b[i].para[3][2]

#VCR
print("VCR 矩阵如下")
print("Ik = Y( Uk + Us) - Is")
print('┏    ┓   ┏                                           ┓ ╭ ┏    ┓   ┏        ┓ ╮   ┏        ┓')

for i in range(1, 7):
    a = str(np.around(Y[i-1,...],decimals=0)).replace('[','').replace(']','')#.replace('  ','')
    out_str = '┃ Ik ┃ = ┃ ' + a + ' ┃ │ ┃ Uk ┃ + ┃ Us ┃ │ - ┃ Is ┃'.replace('Us',str(np.around(b[i-1].para[0],decimals=0))).replace('Is',str(np.around(b[i-1].para[2],decimals=0)))
    print(out_str.replace('k',str(i)))#6

print('┗    ┛   ┗                                           ┛ ╰ ┗    ┛   ┗        ┛ ╯   ┗        ┛')
Us = np.zeros([6,1], dtype = complex)
Is = np.zeros([6,1], dtype = complex)
for i in range(6):
    Us[i] = b[i].para[0]
    Is[i] = b[i].para[2]

#节点电压
A = np.array([[1, 0, 1, 1, 0, 0], [-1, 1, 0, 0, 0, 1], [0, -1, 0, -1, 1, 0]])
Yn = np.matmul(np.matmul(A,Y),A.T)
Jn = np.matmul(A,Is)-np.matmul(np.matmul(A,Y),Us)
print("以④号节点列写节点电压方程\n其矩阵如下")
print('┏                                                       ┓ ┏     ┓   ┏            ┓ ')
for i in range(3):
    a = str(np.around(Yn[i,...],decimals=0)).replace('[','').replace(']','')#.replace('  ','')for i in range(6):
    c = str(np.around(Jn[i,...],decimals=0)).replace('[','').replace(']','')#.replace('  ','')
    out_str = '┃ ' + a + ' ┃ ┃ Unk ┃ = ┃ ' + c + ' ┃'
    print(out_str.replace('k',str(i)))#6
print('┗                                                       ┛ ┗     ┛   ┗            ┛ ')

#解方程
Un = np.matmul(np.linalg.inv(Yn),Jn)
print('┏     ┓   ┏                     ┓')
for i in range(3):
    un = str(np.around(Un[i,...],decimals=4)).replace('[','').replace(']','')
    print('┃ Unk ┃ = ┃\t' + un + '\t┃'.replace('k',str(i)))
print('┗     ┛   ┗                     ┛')

os.system("pause")