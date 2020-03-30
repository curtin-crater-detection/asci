import pandas as pd
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d, ConvexHull
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def voronoi_volumes(points):
    v = Voronoi(points)
    vol = np.zeros(v.npoints)
    for i, reg_num in enumerate(v.point_region):
        indices = v.regions[reg_num]
        if -1 in indices:  # some regions can be opened
            vol[i] = np.inf
        else:
            vol[i] = ConvexHull(v.vertices[indices]).volume
    return vol


def moving_average(a, n=5):
    """
    https://stackoverflow.com/questions/14313510/how-to-calculate-moving-average-using-numpy/54628145
    n = 5 modified to match MATLAB `smooth()` implementation
    """
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1 :] / n

def simulate_crater_populations(input):
    area_size = 202.362
    area_pol = input["area"]

    n_craters = len(area_pol)

    max_bin = area_pol.mean() * 4

    nbins_real = np.arange(area_pol.min(), area_pol.max(), area_pol.median() / 10)

    max_plot = area_pol.median() * 10

    edge = np.sqrt(area_size)

    n_it = 50

    all_volumes_bins = np.zeros(shape=(n_it, len(nbins_real) - 1))

    # run a test showing the output plot of `Voronoi()`
    points = 0 + (edge - 0) * np.random.rand(n_craters, 2)
    vor = Voronoi(points)
    voronoi_plot_2d(vor)
    plt.show()



    for k in range(n_it):
        # equivalent to [x, y] in the MATLAB script
        points = 0 + (edge - 0) * np.random.rand(n_craters, 2)
        c = vor.regions
        volumes = voronoi_volumes(points)

        [volumes_binned, _] = np.histogram(volumes, nbins_real)

        all_volumes_bins[k] = volumes_binned
    
    mean_simu = all_volumes_bins.mean(axis=0)
    std_simu_pos = mean_simu + all_volumes_bins.std(axis=0)
    std_simu_neg = mean_simu - all_volumes_bins.std(axis=0)

    [f_real, _] = np.histogram(area_pol, nbins_real)
    sample = np.arange(0, max_plot, 0.0001)
    f_real_smoothed = moving_average(f_real)
    f_real_interp = np.interp(sample, nbins_real[:-5], f_real_smoothed)
    std_simu_pos_interp = np.interp(sample, nbins_real[:-1], std_simu_pos)

    eps = 0.5

    indexes_where_real_equals_simu = np.where(
        np.abs(f_real_interp - std_simu_pos_interp) < 0.5
    )[0]

    # why do we take the second index in MATLAB?
    idx = indexes_where_real_equals_simu[1]
    px = sample[idx]
    py = f_real_interp[idx]


    plt.plot(nbins_real[:-1], mean_simu, label="Mean of random data")
    plt.plot(nbins_real[:-1], std_simu_pos, label="Mean +1STD of random data")
    plt.plot(nbins_real[:-1], std_simu_neg, label="Mean -1STD of random data")
    plt.plot(sample, f_real_interp, label="Data")
    plt.xlim(0, 50)

    plt.scatter(px, py, s=100, marker="o")
    plt.legend(loc="upper right")
    plt.show()

    threshold_area = px

    return threshold_area