from igraph import *
import pickle
import numpy as np

#   load data
g = pickle.load(open('networks\\exchange_network_countries.pkl', 'rb'))
weights = np.array([edge.attributes()['weight'] for edge in g.es])
visual_style = {}

# Set bbox and margin
visual_style["bbox"] = (15000, 15000)
visual_style["margin"] = 17

# Set vertex colours
visual_style["vertex_color"] = 'firebrick'

# Set vertex size
visual_style["vertex_size"] = 50

# Set vertex lable size
visual_style["vertex_label"] = [vertex.attributes()['name'] for vertex in g.vs]
visual_style["vertex_label_size"] = 30

# Set edge width
visual_style["edge_width"] = 10

# Set edge colour:
# visual_style["edge_color"] = ['dim gray' if weight >= np.percentile(weights, 80) else
#                              'gray' for weight in weights]
max = max(weights)
min = min(weights)


def myround(x, base=5):
    #if x >= 80:
    #    return 80
    #elif x <= 30:
    if x <= 30:
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
plot(g, "images\\graph_countries_drl.png", **visual_style)
plot(g, "images\\graph_countries_drl.eps", **visual_style)
