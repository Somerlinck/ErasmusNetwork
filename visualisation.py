from igraph import *
import pickle
import numpy as np

#   load data
g = pickle.load(open('networks\\exchange_network.pkl', 'rb'))
weights = np.array([edge.attributes()['weight'] for edge in g.es])
visual_style = {}
# pg = g.pagerank(directed=True, vertices=None, damping=0.85, weights='weight',
#                   arpack_options=None, implementation='prpack', niter=5000, eps=0.0001)

# Set bbox and margin
visual_style["bbox"] = (15000, 15000)
visual_style["margin"] = 17

# Set vertex colours
visual_style["vertex_color"] = 'firebrick'
# visual_style["vertex_color"] = ['gray40' if rank >= np.percentile(pg, 99)
#                                else 'gray60' for rank in pg]

# Set vertex size
visual_style["vertex_size"] = 30
# visual_style["vertex_size"] = [round(20*(max(pg) - rank)/(max(pg) - min(pg)))+1 for rank in pg]
# visual_style["vertex_size"] = [200 if rank >= np.percentile(pg, 99)
#                               else 20 for rank in pg]

# Set vertex lable size
# visual_style["vertex_label"] = [vertex.attributes()['name'] for vertex in g.vs]
# visual_style["vertex_label_size"] = 10

# Set edge width
# visual_style["edge_width"] = [5 if weight >= np.percentile(weights, 80) else
#                              1 for weight in weights]
visual_style["edge_width"] = 1

# Set edge colour:
# visual_style["edge_color"] = ['dim gray' if weight >= np.percentile(weights, 80) else
#                              'gray' for weight in weights]
max = max(weights)
min = min(weights)


def myround(x, base=5):
    if x >= 80:
        return 80
    elif x <= 30:
        return 30
    else:
        return base * round(float(x) / base)


visual_style["edge_color"] = ['gray{}'.format(int(myround(100*(max - weight)/(max-min))))
                              for weight in weights]
print(visual_style['edge_color'])

# Set arrow size
for edge in g.es:
    edge["arrow_size"] = 1

# Set arrow width
for edge in g.es:
    edge["arrow_width"] = 1

# Don't curve the edges
visual_style["edge_curved"] = True


# Set the layout
my_layout = g.layout_drl()
visual_style["layout"] = my_layout


# Plot the graph
plot(g, "images\\graph_shools_drl.png", **visual_style)
plot(g, "images\\graph_shools_drl.eps", **visual_style)
