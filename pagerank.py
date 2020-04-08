import pickle
import numpy as np

g = pickle.load(open('networks\\exchange_network.pkl', 'rb'))
vect = g.pagerank(directed=True, vertices=None, damping=0.85, weights='weight',
                  arpack_options=None, implementation='prpack', niter=5000, eps=0.0001)

# N = number of best results schools wanted
N = 30
index = np.argpartition(vect, -N)[-N:]
top_schools = [g.vs[i].attributes()['name'] for i in reversed(index)]
print(top_schools)
