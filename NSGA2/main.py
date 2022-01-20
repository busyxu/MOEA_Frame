import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from NSGA2 import Initialization, select, mutation
from NSGA2 import crossover
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

    ax.set_title("NSGA-II DTLZ", alpha=0.6, color='b', size=8, weight='bold', backgroundcolor='y')
    ax.legend(loc='upper left')
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.set_zlabel("Z axis")
    ax.invert_yaxis()
    plt.show()
    if evolve == maxEvolve-1:
        plt.pause(10)
    else:
        plt.pause(0.001)
    pass


if __name__ == '__main__':

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
    # 目标数
    m = 3
    # 决策变量数
    n = 10
    # 分布指数eta
    eta = 1

    # 获得PF面
    front_true = index.GET_PF()
    # 测试函数
    re = 1
    # 初始化种群
    P = Initialization.initialization(population_size, n, m, re)

    # 开始进化
    t = 0
    while t < maxEvolve:
        print('************************第', t, '代***************************')
        view(P, t, ax, maxEvolve)
        GD = index.GD(P, front_true)
        print('GD:', GD)
        IGD = index.IGD(P, front_true)
        print('IGD:', IGD)
        # hv = index.HV(P)
        # print('HV:', hv)
        # 选择
        Q = select.select_population(P, population_size)
        # 交叉
        # crossover.crossover_near(Q, crossover_pro, re)
        # 从这里开始
        # crossover.crossover_random(Q, crossover_pro, re)
        crossover.crossover_sbx(Q, crossover_pro, eta, re)
        # 变异
        # mutation.mutation(Q, mutation_pro, re)
        mutation.mutation_pm(Q, mutation_pro, eta, re)
        # 将父种群和子种群加在一起
        R = P + Q
        # 快速非支配集排序
        # F = select.nd_sort(np.array(R))
        F = select.fast_sort(R)

        P = []
        i = 0
        while len(P) + len(F[i]) <= population_size:
            # 计算拥挤距离
            select.crowding_distance_assigment(F[i])
            # 一层一层的加
            P = P + F[i]
            i += 1
            pass
        # 最后一层
        F[i] = sorted(F[i], key=lambda individual: individual.crowd_dt, reverse=True)
        P = P + F[i][:population_size - len(P)]
        t += 1

    best = select.best_individual(P)
    print('***************最优解**************')
    print(best)
