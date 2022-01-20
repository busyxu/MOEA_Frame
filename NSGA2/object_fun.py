from Test_Function import DTLZ


def f_func(gene, m, re):
    if re == 1:
        return DTLZ.DTLZ1(m, gene)
    elif re == 2:
        return DTLZ.DTLZ2(m, gene)
    elif re == 3:
        return DTLZ.DTLZ3(m, gene)
    elif re == 4:
        return DTLZ.DTLZ4(m, gene)
    elif re == 5:
        return DTLZ.DTLZ5(m, gene)
    elif re == 6:
        return DTLZ.DTLZ6(m, gene)
    elif re == 7:
        return DTLZ.DTLZ7(m, gene)
    pass
