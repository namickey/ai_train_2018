import pygal
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

def pygal_stat():
    cnum = 10
    x, y = make_blobs(n_samples=1000,centers=cnum,cluster_std=1.7)
    ypredict = KMeans(n_clusters=cnum).fit_predict(x)
    scat = pygal.XY(stroke=False, width=1000, height=500)
    for z in np.unique(ypredict):
        scat.add(str(z),filter(lambda n:n[2]==z, np.insert(x, 2, ypredict, axis=1)))
    return scat.render()
