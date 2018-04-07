import pygal
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

def pygal_stat():
    x, y = make_blobs(500)
    ypredict = KMeans(n_clusters=3).fit_predict(x)
    scat = pygal.XY(stroke=False)
    for z in np.unique(ypredict):
        scat.add(str(z),filter(lambda n:n[2]==z, np.insert(x, 2, ypredict, axis=1)))
    return scat.render()
