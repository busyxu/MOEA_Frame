import random
from NSGA2 import object_fun


def crossover_near(population, crossover_probability, re):
    m = len(population[0].func)
    size = len(population)
    flag = True
    for i in range(size):
        p = random.uniform(0, 1)
        if p < crossover_probability:
            if flag:
                flag = False
                fa_idx = i
                pass
            else:
                flag = True
                ma_idx = i
                for idx, g in enumerate(population[fa_idx].gene):
                    p = random.uniform(0, 1)
                    if p < 0.5:
                        t = g
                        population[fa_idx].gene[idx] = population[ma_idx].gene[idx]
                        population[ma_idx].gene[idx] = t
                        pass
                    pass
                population[fa_idx].func = object_fun.f_func(population[fa_idx].gene, m, re)
                population[ma_idx].func = object_fun.f_func(population[ma_idx].gene, m, re)
                # population[fa_idx].dt = index.determine_distance(population[fa_idx].func, front_true)
                # population[ma_idx].dt = index.determine_distance(population[ma_idx].func, front_true)
                pass

            pass
        pass
    pass


def crossover_random(population, crossover_pro, re):
    m = len(population[0].func)
    size = len(population)
    for fa_idx in range(size):
        p = random.uniform(0, 1)
        if p < crossover_pro:
            ma_idx = random.randint(0, size-1)
            for idx, g in enumerate(population[fa_idx].gene):
                p = random.uniform(0, 1)
                if p < 0.5:
                    t = g
                    population[fa_idx].gene[idx] = population[ma_idx].gene[idx]
                    population[ma_idx].gene[idx] = t
                    pass
                pass
            population[fa_idx].func = object_fun.f_func(population[fa_idx].gene, m, re)
            population[ma_idx].func = object_fun.f_func(population[ma_idx].gene, m, re)
            pass
        pass
    pass


def crossover_sbx(population, crossover_pro, eta, re):
    m = len(population[0].func)
    size = len(population)
    for fa_idx in range(size):
        p = random.uniform(0, 1)
        if p < crossover_pro:
            ma_idx = random.randint(0, size-1)

            u = random.uniform(0, 1)
            if u <= 0.5:
                gamma = (2*u)**(1/(eta+1))
                pass
            else:
                gamma = (1/(2*(1-u)))**(1/(eta+1))
                pass
            fa = population[fa_idx]
            ma = population[ma_idx]
            for j in range(len(fa.gene)):
                off1 = 0.5*((1+gamma)*fa.gene[j] + (1-gamma)*ma.gene[j])
                # 基因判断上下限
                # if off1 < 0:
                #     off1 = 0
                #     pass
                # if off1 > 1:
                #     off1 = 1
                #     pass
                off2 = 0.5*((1-gamma)*fa.gene[j] + (1+gamma)*ma.gene[j])
                # 基因判断上下限
                # if off2 < 0:
                #     off2 = 0
                #     pass
                # if off2 > 1:
                #     off2 = 1
                #     pass
                if off1 < 0 or off1 > 1 or off2 < 0 or off2 > 1:
                    continue
                population[fa_idx].gene[j] = off1
                population[ma_idx].gene[j] = off2
                pass
            population[fa_idx].func = object_fun.f_func(population[fa_idx].gene, m, re)
            population[ma_idx].func = object_fun.f_func(population[ma_idx].gene, m, re)
            # population[fa_idx].dt = index.determine_distance(population[fa_idx].func, front_true)
            # population[ma_idx].dt = index.determine_distance(population[ma_idx].func, front_true)
            pass
        pass
    pass
