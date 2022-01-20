import math
import copy
# import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from SPEA2 import initialization, select, crossover
from SPEA2 import mutation
from Index import index


def view(population, evolve, ax, maxEvolve):
    x = []
    y = []
    z = []
    for pop in population:
        x.append(pop.func[0])
        y.append(pop.func[1])
        z.append(pop.func[2])
        pass
    ax.cla()
    # ax.scatter(x, y, z, s=32)
    ax.plot(x, y, z, markersize=8, linestyle=' ', marker='o', label='evolve: '+str(evolve))

    ax.set_title("SPEA-2 DTLZ", alpha=0.6, color='b', size=8, weight='bold', backgroundcolor='y')
    ax.legend(loc='upper left')
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.set_zlabel("Z axis")
    ax.invert_yaxis()
    plt.show()
    if evolve == maxEvolve - 1:
        plt.pause(10)
    else:
        plt.pause(0.001)
    pass
    pass


if __name__ == "__main__":
    fig = plt.figure(figsize=(10, 7))
    ax = p3.Axes3D(fig)
    plt.ion()
    # 个体数
    population_size = 200
    # 进化次数
    maxEvolve = 100
    # 交叉概率
    crossover_pro = 0.7
    # 变异概率
    mutation_pro = 0.2
    # 归档集大小
    M = 200
    # 目标数
    m = 3
    # 决策变量数
    n = 10
    # 分布指数eta
    eta = 1
    NDSet = []

    # 获得PF面
    front_true = index.GET_PF()
    # k
    k = int(math.sqrt(population_size + M))
    # 测试函数
    re = 7
    # 初始化种群
    P = initialization.initialization(population_size, n, m, re)
    # 初始化归档集
    Q = []
    # # 计算种群的目标函数
    # object_function(P, m)
    # # 适应度分配
    # P_Q = P + Q
    # fitness_assignment(P_Q, k)
    # print(P)
    # print(Q)
    ca = 0
    while True:
        # 适应度分配
        P_Q = P + Q
        select.fitness_assignment(P_Q, k)
        # print("fitness_assignment")
        # 环境选择
        Q = select.environmental_select(P, Q, M)
        # print("environmental_select")
        print('************************第', ca, '代***************************')
        view(Q, ca, ax, maxEvolve)
        GD = index.GD(P, front_true)
        print('GD:', GD)
        IGD = index.IGD(P, front_true)
        print('IGD:', IGD)
        # hv = index.HV(P)
        # print('HV:', hv)
        # print(Q)
        # 结束条件
        if ca >= maxEvolve:
            for pop in Q:
                if pop.fitness < 1:
                    NDSet.append(pop)
                    pass
                pass

            print(NDSet)
            break
        # 配对选择
        mating_pool = select.mating_select(Q, population_size)
        # print("mating_pool")
        # 交叉
        # crossover.crossover_sbx(mating_pool, crossover_pro, eta, re)
        crossover.crossover_random(mating_pool, crossover_pro, re)
        # print("crossover")
        # 变异
        mutation.mutation_pm(mating_pool, mutation_pro, eta, re)
        # print("mutation")
        P = copy.deepcopy(mating_pool)
        ca += 1
        pass

    best = select.best_individual(P)
    print('***************最优解**************')
    print(best)

