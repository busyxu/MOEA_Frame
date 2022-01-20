import numpy as np
# import random


def DTLZ1(m, x):
    n = len(x)
    k = n - m + 1
    s = 0
    for i in x[-k:]:
        s += (i - 0.5) ** 2 - np.cos(20 * np.pi * (i - 0.5))
        pass
    g = 100 * (k + s)

    f = []
    for i in range(m):
        t = 0.5
        for j in x[:m-1-i]:
            t *= j
            pass
        if i > 0:
            t *= (1-x[m-1-i])
            pass

        t *= (1+g)
        f.append(t)
        pass
    return f


x = np.load("E:\\python\\MOEA\\Test_Function\\X.npy")
print(x.shape)

f = DTLZ1(3, x[0])
print(f)
#
# ff = f_fun(3, [0.1, 0.1, 0.5, 0.5])
# print(ff)


def DTLZ2(m, x):
    n = len(x)
    k = n - m + 1

    g = 0
    for i in x[-k:]:
        g += (i - 0.5) ** 2
        pass

    f = []
    for i in range(m):
        t = (1 + g)
        for j in x[:m - 1 - i]:
            t *= np.cos(j*np.pi/2)
            pass
        if i > 0:
            t *= np.sin(x[m-1-i]*np.pi/2)
            pass
        f.append(t)
        pass
    return f


def DTLZ3(m, x):
    n = len(x)
    k = n - m + 1

    s = 0
    for i in x[-k:]:
        s += (i - 0.5) ** 2 - np.cos(20 * np.pi * (i - 0.5))
        pass
    g = 100 * (k + s)

    f = []
    for i in range(m):
        t = (1 + g)
        for j in x[:m - 1 - i]:
            t *= np.cos(j*np.pi/2)
            pass
        if i > 0:
            t *= np.sin(x[m-1-i]*np.pi/2)
            pass
        f.append(t)
        pass
    return f


def DTLZ4(m, x):
    n = len(x)
    k = n - m + 1
    alpha = 100

    s = 0
    for i in x[-k:]:
        s += (i - 0.5) ** 2 - np.cos(20 * np.pi * (i - 0.5))
        pass
    g = 100 * (k + s)

    f = []
    for i in range(m):
        t = (1 + g)
        for j in x[:m - 1 - i]:
            t *= np.cos(j**alpha * np.pi/2)
            pass
        if i > 0:
            t *= np.sin(x[m-1-i]**alpha * np.pi/2)
            pass
        f.append(t)
        pass
    return f


def DTLZ5(m, x):
    n = len(x)
    k = n - m + 1

    g = 0
    for i in x[-k:]:
        g += (i - 0.5) ** 2
        pass

    f = []
    for i in range(m):
        t = (1 + g)
        for j in x[:m - 1 - i]:
            theta = np.pi / (4 * (1 + g)) * (1 + 2 * g * j)
            t *= np.cos(theta * np.pi / 2)
            # if t < 0:
            #     print(t)
            pass
        if i > 0:
            theta = np.pi / (4 * (1 + g)) * (1 + 2 * g * x[m-1-i])
            t *= np.sin(theta * np.pi / 2)
            pass
        f.append(t)
        pass
    return f


def DTLZ6(m, x):
    n = len(x)
    k = n - m + 1

    g = 0
    for i in x[-k:]:
        g += i ** 0.1
        pass

    f = []
    for i in range(m):
        t = (1 + g)
        for j in x[:m - 1 - i]:
            theta = np.pi / (4 * (1 + g)) * (1 + 2 * g * j)
            t *= np.cos(theta * np.pi / 2)
            pass
        if i > 0:
            theta = np.pi / (4 * (1 + g)) * (1 + 2 * g * x[m-1-i])
            t *= np.sin(theta * np.pi / 2)
            pass
        f.append(t)
        pass
    return f


def DTLZ7(m, x):
    n = len(x)
    k = n - m + 1

    t = 0
    for i in x[-k:]:
        t += i
        pass
    g = 1 + 9/k * t

    f = []
    for i in range(m):
        if i < m-1:
            f.append(x[i])
            pass
        else:
            temp = 0
            for f_i in f:  # f的size为m-1
                temp += (f_i/(1+g)*(1+np.sin(3*np.pi*f_i)))
                pass
            h = m - temp
            f.append((1+g)*h)
            pass

        pass
    return f
