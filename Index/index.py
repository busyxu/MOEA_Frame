import numpy as np
import xlrd
import sys
import copy


def GET_PF():
    data = xlrd.open_workbook(r"../Index/data.xls")
    # data = xlrd.open_workbook(r"data1.xls")
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    front_true = np.zeros((nrows, ncols))
    # front_true = []
    for i in range(nrows):
        # print(table.row_values(i))
        # front_true.append(individual.Individual(func=table.row_values(i)))
        for j in range(ncols):
            front_true[i][j] = table.cell_value(i, j)
            pass
        pass
    return front_true


# front_true = GET_PF()


def GD(front_current, front_true):
    m = len(front_current[0].func)
    gd = 0
    for i, p1 in enumerate(front_current):
        min_dt = sys.maxsize
        for j, p2 in enumerate(front_true):
            dt = 0
            for k in range(m):
                dt += (p1.func[k] - p2[k]) ** 2
                pass
            if dt < min_dt:
                min_dt = dt
                pass
            pass
        p1.dt = min_dt
        gd += min_dt
        pass
    return gd/len(front_current)


def IGD(front_current, front_true):
    m = len(front_current[0].func)
    igd = 0
    for i, p1 in enumerate(front_true):
        min_dt = sys.maxsize
        for j, p2 in enumerate(front_current):
            dt = 0
            for k in range(m):
                dt += (p1[k] - p2.func[k]) ** 2
                pass
            if dt < min_dt:
                min_dt = dt
                pass
            pass
        # p1.dt = min_dt
        igd += min_dt
        pass
    return igd/len(front_true)


def jude_dominated(p, q):
    m = len(p.func)
    # 最小化问题
    i = 0
    flag = True
    cnt = 0
    while i < m:
        if p.func[i] > q.func[i]:
            flag = False
            break
            pass
        elif p.func[i] == q.func[i]:
            cnt += 1
            pass
        i += 1
        pass
    if flag:
        if cnt < m:  # 不能所有目标相等
            return True
        else:
            return False
        pass
    else:  # 存在一个目标不小于则不支配
        return False

    pass


def HV(front_current):
    m = len(front_current[0].func)
    max_func = [i for i in front_current[0].func]
    no_domination = []
    for p in front_current:
        flag = True
        for q in front_current:
            if jude_dominated(q, p):
                flag = False
                break
            pass
        if flag:
            # 相同的就不加进去了
            flag1 = True
            for pop in no_domination:
                for k in range(m):
                    if p.func[k] != pop.func[k]:
                        break
                    pass
                if k == m-1:
                    flag1 = False
                    break
                pass
            if flag1:
                no_domination.append(p)
                pass
            pass

        for j in range(m):
            if p.func[j] > max_func[j]:
                max_func[j] = p.func[j]
                pass
            pass
        pass
    #  --------------------最小化问题（限制三维）-----------------------------
    # 按第一维排序
    # no_domination_sort = sorted(no_domination, key=lambda individual: individual.func[0])
    # 有效点(个体)
    # num = copy.deepcopy(no_domination)  # 假设有len(no_domination_sort)个不同投影点
    delete_idex = []
    for i, p in enumerate(no_domination):
        for j, q in enumerate(no_domination):
            if p == q:
                continue
            if p.func[1] == q.func[1] and p.func[2] == q.func[2]:
                # # q点在p点后面，所以q点比p点大，因此保留较小的点(为了在第0维上找最小的)，最小的点离参考点远。
                if p.func[0] > q.func[0]:
                    delete_idex.append(p)
                    break
                pass
            pass
        pass
    for pop in delete_idex:
        no_domination.remove(pop)
        pass
    hv = 0
    #  这样算有问题
    for pop in no_domination:
        hv += np.abs(1.1-pop.func[0]/max_func[0]) * np.abs(1.1-pop.func[1]/max_func[1]) * np.abs(1.1-pop.func[2]/max_func[2])
        pass

    return hv


def check(p, q):
    m = len(p.func)
    # 最小化问题
    i = 0
    flag = True
    cnt = 0
    while i < m:
        if p.func[i] > q.func[i]:
            flag = False
            break
            pass
        elif p.func[i] == q.func[i]:
            cnt += 1
            pass
        i += 1
        pass
    if flag:
        if cnt < m:  # 不能所有目标相等
            return True
        else:
            return False
        pass
    else:  # 存在一个目标不小于则不支配
        return False
#
# n = 10
# m = 3
# front_current = np.random.randint(0, 10, (n, m))
# print('front_current')
# print(front_current)
# sort_front = front_current[np.lexsort(front_current[:, ::-1].T)]  # 每行排序，按每行的第一列比较。
# print('sort_front')
# print(sort_front)
# # print('sdf')
# # delete_front = np.delete(sort_front, [1,3,9], 0)
# # print(delete_front)
# delete_index = []
# for i in range(n):
#     for j in range(i+1, n):
#         # print(j)
#         if sort_front[i][0] <= sort_front[j][0] and sort_front[i][1] <= sort_front[j][1] and sort_front[i][2] <= sort_front[j][2]:
#             break
#     if j < n-1:  # 被支配了
#         delete_index.append(i)
# # print(delete_index)
# delete_front = np.delete(sort_front, delete_index, 0)
# print('delete_front')
# print(delete_front)
# max_point = np.amax(delete_front, axis=0)
# print('max_point')
# print(max_point)
# differ_area = max_point - delete_front
# print('differ_area')
# print(differ_area)
# HV = np.prod(differ_area[0])
# # print(delete_front[1:])
# for i in range(1, differ_area.shape[0]):
#     # 按第一个目标排序遍历，说明后面的点在第一个目标上越来越差，同时与参考点的差值在该目标值上面越来越小
#     sum_area = np.prod(differ_area[i])
#     # 判断第二个目标是否比上一个点优
#     if differ_area[i][1] > differ_area[i-1][1]:
#         if differ_area[i][2] > differ_area[i-1][2]:
#             # 谁小将谁乘积
#             repeat_area = np.prod([differ_area[i][0], differ_area[i-1][1], differ_area[i-1][2]])
#             # HV += sum_area - repeat_area
#         else:
#             # 谁小将谁乘积
#             repeat_area = np.prod([differ_area[i][0], differ_area[i-1][1], differ_area[i][2]])
#             # HV += sum_area - repeat_area
#     else:
#         if differ_area[i][2] > differ_area[i-1][2]:
#             # 谁小将谁乘积
#             repeat_area = np.prod([differ_area[i][0], differ_area[i][1], differ_area[i-1][2]])
#     HV += sum_area - repeat_area
