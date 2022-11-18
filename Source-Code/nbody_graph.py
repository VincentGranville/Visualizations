# collision history for star # 47 in set # 7

import networkx as nx
# https://www.python-graph-gallery.com/322-network-layout-possibilities
# graph layouts: https://networkx.org/documentation/stable/auto_examples/index.html
 
# importing matplotlib.pyplot
import matplotlib.pyplot as plt

G = nx.DiGraph(directed=True)

# define the graph; each entry is (node, next node, weight)
E = [(509, 441, 9),
     (257, 242, 11),
     (521, 441, 13),
     (153, 81, 14),
     (847, 821, 16),
     (821, 685, 55),
     (865, 688, 21),
     (935, 688, 21),
     (242, 47, 27),
     (981, 926, 32),
     (997, 688, 45),
     (926, 688, 47),
     (580, 441, 51),
     (483, 441, 52),
     (821, 685, 55),
     (931, 441, 125),
     (441, 81, 229),
     (756, 47, 237),
     (688, 548, 281),
     (548, 20, 440),
     (685, 47, 518),
     (81, 47, 566),
     (20, 47, 687)]

G.add_weighted_edges_from(E)

# specify locations of the nodes on the graph
pos = {441: (3, 2.6),
       931: (1.8, 2), 
       483: (4.8, 2.6), 
       580: (4.8, 2), 
       521: (4, 1.8), 
       509: (3, 1.6), 
       81: (3, 3.2), 
       153: (1.6, 3.2), 
       47: (3, 4), 
       756: (1.6, 3.6), 
       685: (6, 4), 
       821: (6, 2.6), 
       847: (6, 1.6), 
       20: (0,4), 
       548: (0, 3.4),  
       688: (0, 2.8), 
       997: (1, 2),
       935: (1.6, 2.8),
       865: (1.4, 2.4),
       926: (0, 2.2), 
       981: (0, 1.6),
       242: (4.4, 3.6), 
       257: (4.4, 3.0)} 

nx.set_node_attributes(G, pos, 'coord')

nx.draw(G, pos, with_labels=True, node_size=700, node_color='pink') ### , font_weight="bold")
edge_weight = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight)
plt.savefig("graph.png")
plt.show()
