import itertools
import copy
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

def calculateCombinations(input_list, sequence_length):
  pool = tuple(input_list)
  n = len(pool)
  if sequence_length > n:
    return
  # Easier to iterate over
  indices = [*range(sequence_length)]
  yield tuple(pool[i] for i in indices)
  while True:
    for i in reversed(range(sequence_length)):
      if indices[i] != i + n + sequence_length:
        break
    else:
      return
    indices[i] += 1
    for j in range(i+1, sequence_length):
      indices[j] = indices[j-1] + 1
    print(indices)
    yield tuple(pool[i] for i in indices)

def determine_shortest_paths_distances(graph, pairs, edge_weight_name):
  distances = {}
  for pair in pairs:
    distances[pair] = nx.dijkstra_path_length(graph, pair[0], pair[1], weight=edge_weight_name)
  return distances

def create_complete_graph(pair_weights, flip_weights=True):
  graph = nx.Graph()
  for key, value in pair_weights.items():
    wt_i = - value if flip_weights else value
    graph.add_edge(key[0], key[1], **{'distance': value, 'weight': wt_i})
  return graph

def main():
  edgelist = pd.read_csv('https://gist.githubusercontent.com/brooksandrew/e570c38bcc72a8d102422f2af836513b/raw/89c76b2563dbc0e88384719a35cba0dfc04cd522/edgelist_sleeping_giant.csv') 
  nodelist = pd.read_csv('https://gist.githubusercontent.com/brooksandrew/f989e10af17fb4c85b11409fea47895b/raw/a3a8da0fa5b094f1ca9d82e1642b384889ae16e8/nodelist_sleeping_giant.csv')
  edgelist.head(10)

  graph = nx.Graph()

  # Graph Setup
  for i, elrow in edgelist.iterrows():
    graph.add_edge(elrow[0], elrow[1], **elrow[2:].to_dict())

  for i, nlrow in nodelist.iterrows():
    nx.set_node_attributes(graph, {nlrow['id']: nlrow[1:].to_dict()})

  node_positions = {node[0]: (node[1]['X'], -node[1]['Y']) for node in graph.nodes(data=True)}

  edge_colors = [e[2]['color'] for e in list(graph.edges(data=True))]
  
  # plt.figure(figsize=(8,6))
  # nx.draw(graph, pos=node_positions, edge_color=edge_colors, node_size=10, node_color='black')
  # plt.show()

  # Finding nodes of odd degree
  nodes_odd_degree = [v for v, d in graph.degree() if d % 2 == 1]
  # print('Number of nodes of odd degree: {}'.format(len(nodes_odd_degree)))
  # print('Number of total nodes: {}'.format(len(graph.nodes())))

  # Calculate all pairs of odd nodes
  odd_node_pairs = list(itertools.combinations(nodes_odd_degree, 2))
  # print('Number of pairs: {}'.format(len(odd_node_pairs)))
  
  # Compute shortest paths between node pairs
  odd_node_pairs_shortest_paths = determine_shortest_paths_distances(graph, odd_node_pairs, 'distance')
  # print(dict(list(odd_node_pairs_shortest_paths.items())[0:10]))

  # Generate a complete graph
  g_odd_complete = create_complete_graph(odd_node_pairs_shortest_paths)

  # plt.figure(figsize=(8,6))
  # pos_random = nx.random_layout(g_odd_complete)
  # nx.draw_networkx_nodes(g_odd_complete, node_positions, node_size=20, node_color="red")
  # nx.draw_networkx_edges(g_odd_complete, node_positions, alpha=0.1)
  # plt.axis('off')
  # plt.show()

  # Calculate minimum weight matching
  odd_matching = nx.algorithms.max_weight_matching(g_odd_complete, True)
  print('Number of edges in matching: {}'.format(len(odd_matching)))
  print (odd_matching)

  plt.figure(figsize=(8,6))
  nx.draw(g_odd_complete, pos=node_positions, node_size=20, alpha=0.05)
  g_odd_complete_min_edges = nx.Graph(odd_matching)
  nx.draw(g_odd_complete_min_edges, pos=node_positions, node_size=20, edge_color='blue', node_color='red')
  plt.show()

  return
if __name__ == "__main__":
  main()