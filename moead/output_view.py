import matplotlib.pyplot as plt


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

    ax.set_title("MOEA\D DTLZ", alpha=0.8, color='b', size=8, weight='bold', backgroundcolor='y')
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
