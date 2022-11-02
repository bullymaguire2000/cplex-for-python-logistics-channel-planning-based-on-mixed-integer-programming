import docplex.mp.model as cpx
opt_model = cpx.Model(name="MIP Model")
import pandas as pd

B=2236                         #原料：2类企业
A =2481                        #产品：1类企业
m = 22

set_A=range(A)                 ##定义有几个1类企业
set_B=range(B)                 ##定义有几个2类企业
set_m=range(m)                 ##定义有几个备选点


def set_num(a=0):
    return a

#参数定义
def set_cost(c1,c2):                                                       ##费用
    C={'C1':c1,'C2':c2}
    return C

def demand(df=None):                                                       ##需求
    D={(i): df.loc[i] for i in range(len(df))}
    return D



def distance3(df=None):
    n=len(df)
    m=len(df.columns)
    set_n=range(n)
    set_m=range(m)
    D = {(j, i): df.loc[j,i] for j in set_n for i in set_m}
    return D

def B(df=None):                                                            ##建立一个库的成本
    B={(j):df.loc[j] for j in range(len(df))}
    return B

def V(v1,v2):                                                              ##每个仓库的容量
    V1={'V1':v1,'V2':v2}
    return V1

def R(df=None):                                                            ##地皮价格
    R1={(j):df.loc[j] for j in set_J}
    return R1


##读取数据

df_beixuandian=pd.read_csv('location.csv')

df_distance_11=pd.read_excel('Distance_产品公路.xlsx',header=None)
df_distance_12=pd.read_excel('Distance_产品铁路.xlsx',header=None)
df_distance_13=pd.read_excel('Distance_产品水运.xlsx',header=None)
df_distance_21=pd.read_excel('Distance_原料公路.xlsx',header=None)
df_distance_22=pd.read_excel('Distance_原料铁路.xlsx',header=None)
df_distance_23=pd.read_excel('Distance_原料水运.xlsx',header=None)


df_distance_L1=pd.read_excel('公路出口距离.xlsx',header=None)
df_distance_L2=pd.read_excel('铁路出口距离.xlsx',header=None)
df_distance_L3=pd.read_excel('水路出口距离.xlsx',header=None)

df_demand_11=pd.read_csv('产品公路.csv').loc[:,'需求量']
df_demand_12=pd.read_csv('产品铁路.csv').loc[:,'需求量']
df_demand_13=pd.read_csv('产品水运.csv').loc[:,'需求量']
df_demand_21=pd.read_csv('原料公路.csv').loc[:,'需求量']
df_demand_22=pd.read_csv('原料铁路.csv').loc[:,'需求量']
df_demand_23=pd.read_csv('原料水运.csv').loc[:,'需求量']

##企业标
set_I11=range(set_num(len(df_demand_11)))

set_I12=range(set_num(len(df_demand_12)))
set_I13=range(set_num(len(df_demand_13)))
set_I21=range(set_num(len(df_demand_21)))
set_I22=range(set_num(len(df_demand_22)))
set_I23=range(set_num(len(df_demand_23)))
##备选点标
set_J=range(set_num(len(df_beixuandian)))
set_t1=range(set_num(len(df_distance_L1.columns)))               ##出口
set_t2=range(set_num(len(df_distance_L2.columns)))
set_t3=range(set_num(len(df_distance_L3.columns)))
label_set=[set_I11,set_I12,set_I13,set_I21,set_I22,set_I23]
exit_set=[set_t1,set_t2,set_t3]

D11=demand(df_demand_11)
D12=demand(df_demand_12)
D13=demand(df_demand_13)
D21=demand(df_demand_21)
D22=demand(df_demand_22)
D23=demand(df_demand_23)
deamnd_set=[D11,D12,D13,D21,D22,D23]

BJ=B(df_beixuandian.loc[:,'备选点单个仓库建设成本（万元）'])
RJ=R(df_beixuandian.loc[:,'备选点单个仓库地价（万元）'])

l1=distance3(df_distance_11)
l2=distance3(df_distance_12)
l3=distance3(df_distance_13)
l4=distance3(df_distance_21)
l5=distance3(df_distance_22)
l6=distance3(df_distance_23)
l_set_for_qiye=[l1,l2,l3,l4,l5,l6]

L1=distance3(df_distance_L1)
L2=distance3(df_distance_L2)
L3=distance3(df_distance_L3)

l_set=[L1,L2,L3]

##定义变量

#备选点是否被选择
beixuan_dian = {(j): opt_model.binary_var(name="beixuan_dian_{0}".format(j)) for j in set_J}
#企业是否选择某个备选点
y11j_qiye={(j,i): opt_model.binary_var(name="y11j_qiye_{0}_{1}".format(j,i)) for i in set_I11 for j in set_J}
y12j_qiye={(j,i): opt_model.binary_var(name="y12j_qiye_{0}_{1}".format(j,i)) for i in set_I12 for j in set_J}
y13j_qiye={(j,i): opt_model.binary_var(name="y13j_qiye_{0}_{1}".format(j,i)) for i in set_I13 for j in set_J}
y21j_qiye={(j,i): opt_model.binary_var(name="y21j_qiye_{0}_{1}".format(j,i)) for i in set_I21 for j in set_J}
y22j_qiye={(j,i): opt_model.binary_var(name="y22j_qiye_{0}_{1}".format(j,i)) for i in set_I22 for j in set_J}
y23j_qiye={(j,i): opt_model.binary_var(name="y23j_qiye_{0}_{1}".format(j,i)) for i in set_I23 for j in set_J}
y_set=[y11j_qiye,y12j_qiye,y13j_qiye,y21j_qiye,y22j_qiye,y23j_qiye]
##基地里面有几个仓库
##1类仓库
n1_warehouse={(j): opt_model.integer_var(name="n1_warehouse_{0}".format(j)) for j in set_J}
##2类仓库
n2_warehouse={(j): opt_model.integer_var(name="n2_warehouse_{0}".format(j)) for j in set_J}

##每个出口是否被选择


#每个企业只能选择一个基地
for m in range(len(y_set)):
    for i in label_set[m]:
        for j in set_J:
            opt_model.add_constraint(y_set[m][j,i] <= beixuan_dian[j])
for m in range(len(y_set)):
    for i in label_set[m]:
        ct = opt_model.sum(y_set[m][j,i] for j in set_J)
        opt_model.add_constraint(ct == 1)

##仓库加起来不能超过10
for j in set_J:
    opt_model.add_constraint(n1_warehouse[j]>=0)
for j in set_J:
    opt_model.add_constraint(n2_warehouse[j]>=0)
for j in set_J:
    opt_model.add_constraint(n1_warehouse[j]+n2_warehouse[j]<=10)

##如果不选基地，那么仓库也没了
for j in set_J:
    opt_model.add_constraint(n1_warehouse[j] <= 10*beixuan_dian[j])
for j in set_J:
    opt_model.add_constraint(n2_warehouse[j] <= 10*beixuan_dian[j])

##不能超过总容量
sum=0
for j in set_J:
    for m in range(int((len(y_set)/2))):
        sum+=opt_model.sum(deamnd_set[m][i]*y_set[m][j,i] for i in label_set[m])
    opt_model.add_constraint(5*sum<=n1_warehouse[j]*25000)

sum1=0
for j in set_J:
    for m in range(int(len(y_set)/2)):
        sum += opt_model.sum(deamnd_set[m+3][i] * y_set[m+3][j, i] for i in label_set[m+3])
    opt_model.add_constraint(5*sum <= n2_warehouse[j] * 25000)







##目标函数
sum2=0
for m in range(int(len(y_set)/2)):
    sum2+=opt_model.sum(0.38*l_set_for_qiye[m][j,i]*365*deamnd_set[m][i]*y_set[m][j,i] for i in label_set[m] for j in set_J)
part1=sum2

sum3=0
for m in range(int(len(y_set) / 2)):
    sum3 += opt_model.sum(0.3*l_set_for_qiye[m][j,i]*365* deamnd_set[m + 3][i] * y_set[m + 3][j, i] for i in label_set[m + 3] for j in set_J)
part2=sum3

part3=opt_model.sum((n1_warehouse[j]+n2_warehouse[j])*BJ[j]*10000 for j in set_J)      ##建设成本
part4=opt_model.sum(10000*RJ[j]*(n1_warehouse[j]+n2_warehouse[j]) for j in set_J)      ##地皮成本

sum4=0
for j in set_J:
    for m in range(int(len(y_set)/2)):
        sum4+=opt_model.sum(l_set[m][j,t]*deamnd_set[m][i]*y_set[m][j,i]*0.38 for i in label_set[m] for t in exit_set[m])

sum5=0
for j in set_J:
    for m in range(int(len(y_set)/2)):
        sum5+=opt_model.sum(l_set[m][j,t]*deamnd_set[m+3][i]/5*y_set[m+3][j,i]*0.3 for i in label_set[m+3] for t in exit_set[m])
part5=sum4+sum5

objective=part5+part3+part4+part2+part1
opt_model.minimize(objective)
sol=opt_model.solve()
print(sol)

'''
opt_df = pd.DataFrame.from_dict(x_exit1, orient="index", columns = ["variable_object"])
opt_df.index =pd.MultiIndex.from_tuples(opt_df.index, names=["column_i", "column_j"])
opt_df.reset_index(inplace=True)
opt_df["solution_value"] = opt_df["variable_object"].apply(lambda item: item.solution_value)
opt_df.drop(columns=["variable_object"], inplace=True)
opt_df.to_csv("optimization_solution1.csv")

opt_df = pd.DataFrame.from_dict(x_exit2, orient="index", columns = ["variable_object"])
opt_df.index =pd.MultiIndex.from_tuples(opt_df.index, names=["column_i", "column_j"])
opt_df.reset_index(inplace=True)
opt_df["solution_value"] = opt_df["variable_object"].apply(lambda item: item.solution_value)
opt_df.drop(columns=["variable_object"], inplace=True)
opt_df.to_csv("optimization_solution2.csv")

opt_df = pd.DataFrame.from_dict(x_exit3, orient="index", columns = ["variable_object"])
opt_df.index =pd.MultiIndex.from_tuples(opt_df.index, names=["column_i", "column_j"])
opt_df.reset_index(inplace=True)
opt_df["solution_value"] = opt_df["variable_object"].apply(lambda item: item.solution_value)
opt_df.drop(columns=["variable_object"], inplace=True)
opt_df.to_csv("optimization_solution3.csv")
'''














