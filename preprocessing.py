from igraph import *
import pandas as pd
import pickle


def create_network():
    source = 'data\\Student_Mobility_EdgesListCountries.csv'
    df = pd.read_csv(source)
    df.drop(['RowNumber'], axis=1, inplace=True)
    network = Graph.TupleList(df.itertuples(index=False), directed=True, weights=True)
    filename = 'networks\\exchange_network_countries.pkl'
    pickle.dump(network, open(filename, 'wb'))


#   create_network()

g = pickle.load(open('networks\\exchange_network_countries.pkl', 'rb'))
print(max(g.degree(mode='in')))
print(max(g.degree(mode='out')))
print(mean(g.edge_betweenness()))


