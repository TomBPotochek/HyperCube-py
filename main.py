from matplotlib import animation
import numpy as np


dimensions = 4
precision = np.float32

from math import comb, cos, sin
#number_sides_cube = 2**(dimensions-1)*comb(dimensions,1)

from itertools import product, takewhile, count



vertices = np.array([(-1, -1, -1, -1), #0
                     
                     (-1, -1, -1,  1), #1
                     (-1, -1,  1, -1), #2
                     (-1,  1, -1, -1), #3
                     ( 1, -1, -1, -1), #4

                     ( 1, -1, -1,  1), #5
                     ( 1, -1,  1, -1), #6
                     ( 1,  1, -1, -1), #7
                     (-1,  1, -1,  1), #8
                     (-1,  1,  1, -1), #9
                     (-1, -1,  1,  1), #10
                     
                     ( 1,  1, -1,  1), #11
                     ( 1,  1,  1, -1), #12
                     ( 1, -1,  1,  1), #13
                     (-1,  1,  1,  1), #14

                     ( 1,  1,  1,  1)], dtype=precision #15
                    ) 

sides = {
    (0,1), (0,2),
    (0,3), (0,4),
    (1,5), (1,8),
    (1,10), (2,6),
    (2,9), (2,10),
    (3, 7), (3,8),
    (3,9), (4,5),
    (4,6), (4,7),
    (5,11), (5,13),
    (6,12), (6,13),
    (7,11), (7,12),
    (8,11), (8,14),
    (9,12), (9,14),
    (10,13), (10,14),
    (11,15), (12,15),
    (13,15), (14,15)
}

light = np.empty([len(vertices), dimensions], dtype=precision)
light[:] = [0,0,0,3]

hyperplane = np.empty([len(vertices), dimensions], dtype=precision)
hyperplane[:] = [0,0,0,-3]


def gen_cube_verts(dimension: int, precision):
    r = [-1, 1]
    vertexGen = product(r, repeat=dimensions)
    return np.array(list(vertexGen), dtype=precision)


def gen_cube_sides(vertices: np.ndarray):
    ones = np.sum(vertices, axis=1) 
    sorted_ind = ones.argsort()
    ones = ones[sorted_ind[::]]
    vertices = vertices[sorted_ind[::]]
    
    sides = set()
    dim = vertices.shape[1]
    maxIndex = len(vertices)-1
    for i, group in enumerate(ones):
        try:
            firstDifferent = np.where(ones==group+2)[0][0]
        except IndexError:
            firstDifferent = maxIndex
        for j in takewhile((lambda x: ones[x] - group <= 2),
                             range(firstDifferent, maxIndex+1)):
            diff = np.sum(np.abs(vertices[i] - vertices[j]))
            if diff == 2:
                sides.add((sorted_ind[i],sorted_ind[j]))
    return sides


def get_rot(t: float):
    c = cos(t)
    s = sin(t)
    return np.array([
        [1,0,0,0],
        [0, c, 0, -s],
        [0,0,1,0],
        [0, s, 0, c]
    ])


def npsumdot(x, y):
    return np.sum(x*y, axis=1)[:, np.newaxis]

def calculate_3dCoords(coords_4d: np.ndarray, rotation_angle: float = 0):
    global light, hyperplane

    mat = get_rot(rotation_angle)
    v = np.dot(mat, coords_4d.T).T
    r = v - light
    #r /= np.linalg.norm(r, axis=1)[:, np.newaxis]

    n = np.copy(hyperplane)
    n[:,3] = 1
    t = npsumdot(n,hyperplane)
    temp = npsumdot(r,n)
    t = t/temp
    
    projectedVerts = r * t

    return projectedVerts[:,:3]

def display(verts_4d: np.ndarray):
    import matplotlib as mpl
    from matplotlib import pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.animation as animation

    fig= plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_aspect("auto")
    ax.grid(False)
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    plt.tight_layout()

    nframes = 24
    t = np.linspace(0, np.pi/2, nframes)

    sides = gen_cube_sides(verts_4d)


    def update(frame):
        ax.clear()
        ax.set_xlim([-1.5,1.5])
        ax.set_ylim([-1.5,1.5])
        ax.set_zlim([-1.5,1.5])
        coords3d = calculate_3dCoords(verts_4d, t[frame])
        for side in sides:
            a, b = coords3d[side[0]], coords3d[side[1]]
            xdata, ydata, zdata = list(zip(a, b))
            ax.plot3D(xdata, ydata, zdata)

    ani = animation.FuncAnimation(
            fig, update, len(t), interval=1000/nframes, repeat=True)

    
    plt.show()
    
    animation.writer = animation.writers['ffmpeg']
    plt.ioff()
   # ani.save("4d_cube.mp4") #descomentar para guardar el video
    plt.ion()




def main():
    global precision, dimensions
#    global vertices, sides

    coords_4d = gen_cube_verts(dimensions, precision)
    display(coords_4d)





if __name__ == '__main__':
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        main()
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    #stats.print_stats(10)
    stats.dump_stats(filename='profiling_stats.prof')
