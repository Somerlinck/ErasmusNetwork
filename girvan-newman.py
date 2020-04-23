from igraph import *
import pickle


g_countries = pickle.load(open('networks\\exchange_network_countries.pkl', 'rb'))
dendogram_countries = g_countries.community_edge_betweenness(directed=True, weights='weight')

names_countries = [vertex.attributes()['name'] for vertex in g_countries.vs]


def replace(text, names):
    index = text.split("\n")[2]
    for i in reversed(range(len(names))):
        index = index.replace(str(i), names[i])
    index += "\n"
    return index + text.split("\n\n")[1]


with open("results\\girvannewman_dendrogram_countries.txt", 'w') as f:
   f.write(replace(str(dendogram_countries), names_countries))
