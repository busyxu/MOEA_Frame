from moead import output_view, update, select, initialization
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
from Index import index

if __name__ == '__main__':
    fig = plt.figure(figsize=(10, 7))
    ax = p3.Axes3D(fig)
    # ax2 = p3.Axes3D(fig)
    plt.ion()

    # 种群大小
    individual_size = 200
    # 进化次数
    max_evolve = 100
    # 领域大小
    # field_size = int(individual_size/10)
    field_size = 10
    # 决策变量数量
    n = 10
    # 目标数
    m = 3
    # 分布指数
    eta = 5
    # 惩罚系数
    theta = 1
    # 变异概率
    mutation_pro = 0.3
    # 测试函数
    re = 1
    # step 1
    # 获得front_true
    front_true = index.GET_PF()
    # 初始化权重向量
    weight, individual_size = initialization.random_lambda(m, individual_size)
    # print(individual_size)
    # print('初始化权重')
    # print(weight)
    # np_weight = np.array(weight)
    # x = np_weight[:, 0]
    # y = np_weight[:, 1]
    # z = np_weight[:, 2]
    # ax.scatter(x, y, z)
    # ax.invert_yaxis()
    # plt.show()

    # print(weight)
    # np_weight = np.array(weight)
    # z_start = np.array([0,0.2,0.3])
    # x = np_weight[:, 0] - z_start[0]
    # y = np_weight[:, 1] - z_start[1]
    # z = np_weight[:, 2] - z_start[2]
    # ax.scatter(x, y, z)
    # ax.invert_yaxis()
    # plt.show()

    # for w in weight:
    #     print(w)
    # 计算权重向量之间的距离
    field = initialization.compute_weight_vector_distance(weight, m, field_size)
    # print('计算权重向量之间的距离')
    # for fd in field:
    #     print(fd)
    #     pass
    # 初始化种群
    population = initialization.init_population(weight, individual_size, n, m, re)
    # print('初始化种群')
    # print(population)
    # 初始化参考点
    z = initialization.init_reference_point(population, m)
    # print('初始化参考点')
    # print(z)
    # 设置 外部种群ep = []
    ep = []
    ca = 0
    while ca < max_evolve:

        # if ca % 20 == 0:
        #     print('****************第', ca, '代******************')
        #     print(len(ep))
        #     # for pop in population:
        #     #     print(ep)
        #     #     # print(sorted(pop.gene))
        #     #     pass
        #     pass

        # step 2 更新
        for i in range(individual_size):
            # 基因重组
            off_string = update.recombination_sbx(population, field[i], eta, re)
            # off_string = update.recombination(n, population, field[i], re)
            # print('基因重组')
            # print(off_string)
            off_string = update.improvement(off_string, mutation_pro, eta, re)
            # 更新参考点z
            update.update_reference_point(off_string, z, m)
            # print('更新参考点z')
            # print(z)
            # 更新领域（方法切比雪夫）
            # update.tchebycheff_approach(population, off_string, weight, field, i, z)
            # 权重求和方法
            # update.weighted_sum_approach(population, off_string, weight, field, i)
            # 边界交叉聚合方法
            update.boundary_intersection_approach(population, off_string, weight, field, i, z, theta)
            # print('更新领域')
            # print(population)
            # 更新外部种群ep
            # update.update_ep(off_string, ep, m)
            # print('更新外部种群ep')
            # print(ep)
            pass
        print('************************第', ca, '代***************************')
        output_view.view(population, ca, ax, max_evolve)
        # output_view.view(ep, ca, ax)
        gd = index.GD(population, front_true)
        print('GD:', gd)
        igd = index.IGD(population, front_true)
        print('IGD:', igd)
        # hv = index.HV(population)
        # print('HV:', hv)
        ca += 1
        pass
    best = select.best_individual(population)
    print('***************最优解**************')
    print(best)
