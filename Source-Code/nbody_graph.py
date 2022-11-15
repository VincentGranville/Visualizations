# collision history for star # 138 in set # 7

import networkx as nx
# https://www.python-graph-gallery.com/322-network-layout-possibilities
# graph layouts: https://networkx.org/documentation/stable/auto_examples/index.html
 
# importing matplotlib.pyplot
import matplotlib.pyplot as plt

G = nx.DiGraph(directed=True)

#G = nx.Graph() 
#E = [(‘A’, ‘B’, 2), (‘A’, ‘C’, 1), (‘B’, ‘D’, 5), (‘B’, ‘E’, 3), (‘C’, ‘E’, 2)]
#G.add_weighted_edges_from(E)

E =[(809, 138, 232,),
    (987, 138, 239),
    (213, 138, 295),
    (685, 138, 270),
    (786, 685, 150),
    (980, 685, 151),
    (796, 685, 166),
    (784, 685, 219),
    (908, 685, 127),
    (749, 685, 70),
    (903, 786, 31),
    (826, 784, 174),
    (840, 784, 55)]


#options = {
#    'node_color': 'pink',
#    'node_size': 500,
#    'width': 3,
#    'arrowstyle': '-|>',
#    'arrowsize': 0.1,
#}

options = {
    'node_color': 'pink',
    'node_size': 700,
    'width': 3,
    #'arrowstyle': '-|>',
    #'arrowsize': 0.1,
}

#nx.draw(G, arrows=True, with_labels = True, **options)
G.add_weighted_edges_from(E)

#pos=nx.random_layout(G, seed=2119)
#pos=nx.fruchterman_reingold_layout(G)

pos={138:(0.76,4.00),
     213:(1.50,3.70),
     685:(0.76,3.00),
     749:(0.50,1.00),
     784:(1.70,2.50),
     786:(0.20,2.00),
     796:(1.40,2.00),
     809:(1.50,3.30),
     826:(1.60,1.30),
     840:(2.00,1.30),
     903:(0.00,1.00),
     908:(0.00,2.70),
     980:(1.05,1.00),
     987:(0.00,3.70)
}   
nx.set_node_attributes(G, pos, 'coord')

nx.draw(G, pos, with_labels=True, node_size=700, node_color='pink') ### , font_weight="bold")
edge_weight = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight)
plt.savefig("graph.png")
plt.show()

