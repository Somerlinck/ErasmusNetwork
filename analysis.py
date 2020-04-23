'''Directed weighted graphs only'''
from igraph import *
import pickle
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#   load data
g = pickle.load(open('networks\\exchange_network_countries.pkl', 'rb'))
names = [vertex.attributes()['name'] for vertex in g.vs]

# vertices / edges
print("Number of vertices:", g.vcount())
print("Number of edges:", g.ecount())

# diameter
print("Graph diameter (Average shortest path length):", g.average_path_length(directed=True))

# strongly connected
components = g.clusters()
print("Connected components:", components)
#print("Density of the graph:", 2*g.ecount()/(g.vcount()*(g.vcount()-1)))

# without considering weights
n_vertices = g.vcount()
degrees_out = []
degrees_in = []

for n in range(n_vertices):
    neighbours_out = g.neighbors(n, mode='OUT')
    neighbours_in = g.neighbors(n, mode='IN')
    degrees_out.append(len(neighbours_out))
    degrees_in.append(len(neighbours_in))

degrees_out = np.array(degrees_out)
degrees_in = np.array(degrees_in)
print("Average degree out:",  mean(degrees_out))
print("Maximum degree out:", max(degrees_out))
print("Vertex with the maximum degree out:", [names[index] for index in np.where(degrees_out == max(degrees_out))[0]])
print("Average degree in:",  mean(degrees_in))
print("Maximum degree in:", max(degrees_in))
print("Vertex with the maximum degree in:", [names[index] for index in np.where(degrees_in == max(degrees_in))[0]])

# considering weights
degrees_out_weight = np.zeros(g.vcount())
degrees_in_weight = np.zeros(g.vcount())
for edge in g.es():
    source = edge.source
    target = edge.target
    weight = edge.attributes()['weight']
    degrees_out_weight[source] += weight
    degrees_in_weight[target] += weight

print("Average degree out (weighted):",  mean(degrees_out_weight))
print("Maximum degree out (weighted):", int(max(degrees_out_weight)))
print("Vertex with the maximum degree out (weighted):", [names[index] for index in np.where(degrees_out_weight == max(degrees_out_weight))[0]])
print("Average degree in (weighted):",  mean(degrees_in_weight))
print("Maximum degree in (weighted):", int(max(degrees_in_weight)))
print("Vertex with the maximum degree in (weighted):", [names[index] for index in np.where(degrees_in_weight == max(degrees_in_weight))[0]])

# normalized closeness centrality : not defined for disconnected graphs
#closeness_centrality = pd.DataFrame(g.closeness(mode='OUT', cutoff=2, weights=None, normalized=True),
#                                    index=names, columns=['Closeness'])

# betweenness centrality
betweeness_centrality = pd.DataFrame(g.betweenness(directed=True, cutoff=2, weights=None), index=names,
                                     columns=['Betweenness'])

# eigenvector centrality
eigenvector_centrality = pd.DataFrame(g.eigenvector_centrality(directed=True, weights=None, scale=True,
                                                               return_eigenvalue=False), index=names,
                                      columns=['EV centrality'])

# authority score
authority_score = pd.DataFrame(g.authority_score(weights=None, scale=True, return_eigenvalue=False), index=names,
                                      columns=['EV centrality'])

# minimal separators
minimal_separators = g.all_minimal_st_separators()
for i in range(len(minimal_separators)):
    for j in range(len(minimal_separators[i])):
        minimal_separators[i][j] = names[minimal_separators[i][j]]

# clique number
print("Clique number:", g.clique_number())

# degree distribution

plt.rcParams.update({'font.size': 25})

x_out = [i for i in range(max(degrees_out)+1)]
degree_counts_out = [0 for _ in x_out]

for i in range(max(degrees_out)+1):
    degree_counts_out[i] += len(np.where(degrees_out == i)[0])

print("Degree having the maximum number of vertices out:", degree_counts_out.index(max(degree_counts_out)))
print("Number of vertices having the most abundant degree out:", max(degree_counts_out))

plt.figure(figsize=(20, 10))
plt.plot(x_out, degree_counts_out, linewidth=3.0)
plt.ylabel('Number of vertices having the given degree out')
plt.xlabel('Degree out')
plt.title('Degree Distribution (out) of Vertices in the Graph')
plt.grid(True)
plt.gca().invert_xaxis()
plt.show()
plt.draw()

x_in = [i for i in range(max(degrees_in)+1)]
degree_counts_in = [0 for _ in x_in]

for i in range(len(degree_counts_in)):
    degree_counts_in[i] += len(np.where(degrees_in == i)[0])

print("Degree having the maximum number of vertices in:", degree_counts_in.index(max(degree_counts_in)))
print("Number of vertices having the most abundant degree in:", max(degree_counts_in))


plt.figure(figsize=(20, 10))
plt.plot(x_in, degree_counts_in, linewidth=3.0)
plt.ylabel('Number of vertices having the given degree in')
plt.xlabel('Degree in')
plt.title('Degree Distribution (in) of Vertices in the Graph')
plt.grid(True)
plt.gca().invert_xaxis()
plt.show()
plt.draw()

# degree distribution weighted: consider binning for countries

x_out_weight = [i for i in range(int(max(degrees_out_weight)+1))]
degree_counts_out_weight = [0 for _ in x_out_weight]

for i in range(int(max(degrees_out_weight)+1)):
    degree_counts_out_weight[i] += len(np.where(degrees_out_weight == i)[0])

print("Degree having the maximum number of vertices out (weighted):", degree_counts_out_weight.index(max(degree_counts_out_weight)))
print("Number of vertices having the most abundant degree out (weighted):", int(max(degree_counts_out_weight)))

plt.figure(figsize=(20, 10))
plt.plot(x_out_weight, degree_counts_out_weight, linewidth=3.0)
plt.ylabel('Number of vertices having the given degree out')
plt.xlabel('Weighted degree out')
plt.title('Weighted Degree Distribution (out) of Vertices in the Graph')
plt.grid(True)
plt.gca().invert_xaxis()
plt.show()
plt.draw()

x_in_weight = [i for i in range(int(max(degrees_in_weight)+1))]
degree_counts_in_weight = [0 for _ in x_in_weight]

for i in range(len(degree_counts_in_weight)):
    degree_counts_in_weight[i] += len(np.where(degrees_in_weight == i)[0])

print("Degree having the maximum number of vertices in (weighted):", degree_counts_in_weight.index(max(degree_counts_in_weight)))
print("Number of vertices having the most abundant degree in (weighted):", int(max(degree_counts_in_weight)))


plt.figure(figsize=(20, 10))
plt.plot(x_in_weight, degree_counts_in_weight, linewidth=3.0)
plt.ylabel('Number of vertices having the given degree in')
plt.xlabel('Weighted Degree in')
plt.title('Weighted Degree Distribution (in) of Vertices in the Graph')
plt.grid(True)
plt.gca().invert_xaxis()
plt.show()
plt.draw()

# number of triangles

# assortivity
