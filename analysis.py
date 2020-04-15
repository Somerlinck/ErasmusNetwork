'''Directed weighted graphs only'''
from igraph import *
import pickle
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

#   load data
g = pickle.load(open('networks\\exchange_network_countries.pkl', 'rb'))

# vertices / edges
print("Number of vertices:", g.vcount())
print("Number of edges:", g.ecount())

# diameter
sum_shortest_path = 0
sum_shortest_path_non_infinite = 0
names = index = [vertex.attributes()['name'] for vertex in g.vs]
for source in names:
    for target in names:
        if source != target:
            shortest_path = g.shortest_paths_dijkstra(source=source, target=target, mode='OUT', weights=None)[0][0]
            if shortest_path != float('inf'):
                sum_shortest_path_non_infinite += shortest_path
            sum_shortest_path += shortest_path

print("Graph diameter (Average path length):", sum_shortest_path/(g.ecount()))
print("Graph diameter (Average path length non infinite):", sum_shortest_path_non_infinite/(g.ecount()))

# strongly connected ?
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

# normalized degree centrality

# normalized closeness centrality

# normalized betweenness centrality

# eigenvector centrality

# look at harmonic centrality

# look at Katz centrality

# clustering coefficient

# degree distribution

plt.rcParams.update({'font.size': 25})

x = [x for x in range(max(degrees_out)+1)]
degree_counts = [0 for _ in x]

for i in range(max(degrees_out)+1):
    degree_counts[i] += len(np.where(degrees_out == i)[0])

print("Degree having the maximum number of vertices out:", degree_counts.index(max(degree_counts)))
print("Number of vertices having the most abundant degree out:", max(degree_counts))

plt.figure(figsize=(20, 10))
plt.plot(x, degree_counts, linewidth=3.0)
plt.ylabel('Number of vertices having the given degree out')
plt.xlabel('Degree out')
plt.title('Degree Distribution (out) of Vertices in the Graph')
plt.grid(True)
plt.savefig('degree_distribution.png', bbox_inches='tight')
plt.gca().invert_xaxis()
plt.show()
plt.draw()

x_in = [x for x in range(max(degrees_in)+1)]
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
plt.savefig('degree_distribution.png', bbox_inches='tight')
plt.gca().invert_xaxis()
plt.show()
plt.draw()


# number of triangles

# assortivity
