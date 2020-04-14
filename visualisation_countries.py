from igraph import *
import pickle
import numpy as np
import geopandas as gpd
import pandas as pd

#   load data
g = pickle.load(open('networks\\exchange_network_countries.pkl', 'rb'))
countries_data = pd.read_csv("data\\Student_Mobility_NodesListCountries.csv")

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


def get_x_coordinates(country):
    if country == 'France':
        return 2.2137489
    try:
        return world[world.name == country]['geometry'].centroid.x.values[0]
    except IndexError:
        if country == 'Malta':
            return 14.409943
        elif country == 'Liechtenstein':
            return 9.553635
        else:
            raise Exception('Country name not found')


def get_y_coordinates(country):
    if country == 'France':
        return 46.2276382
    try:
        return world[world.name == country]['geometry'].centroid.y.values[0]
    except IndexError:
        if country == 'Malta':
            return 35.917973
        elif country == 'Liechtenstein':
            return 47.1594184
        else:
            raise Exception('Country name not found')


countries_data['x_coordinate'] = countries_data['name'].map(get_x_coordinates)
countries_data['y_coordinate'] = -countries_data['name'].map(get_y_coordinates)
countries_data.drop('name', axis=1, inplace=True)

weights = np.array([edge.attributes()['weight'] for edge in g.es])
visual_style = {}

# Set bbox and margin
visual_style["bbox"] = (15000, 15000)
visual_style["margin"] = 400

# Set vertex colours
visual_style["vertex_color"] = 'firebrick'

# Set vertex size
visual_style["vertex_size"] = 300

# Set vertex lable size
visual_style["vertex_label"] = [vertex.attributes()['name'] for vertex in g.vs]
visual_style["vertex_label_size"] = 100
visual_style["vertex_label_color"] = 'white'

# Set edge width
visual_style["edge_width"] = 10

# Set edge colour:
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

# Set arrow size
for edge in g.es:
    edge["arrow_size"] = 3

# Set arrow width
for edge in g.es:
    edge["arrow_width"] = 1

# Don't curve the edges
visual_style["edge_curved"] = True

# Set the layout
index = [vertex.attributes()['name'] for vertex in g.vs]
countries_data.set_index('code', inplace=True)
countries_data = countries_data.reindex(index)

my_layout = [tuple(x) for x in countries_data.values]
my_layout = Layout(my_layout)
my_layout.fit_into(visual_style['bbox'], keep_aspect_ratio=True)
visual_style['layout'] = my_layout

# Plot the graph
plot(g, "images\\graph_countries.png", **visual_style)
plot(g, "images\\graph_countries.eps", **visual_style)
