#include <iostream>
#include <map>
#include <list>
#include <cstring>

int main() {
  Graph graph;
  Vertex v1 = Vertex("cool");
  Vertex v2 = Vertex("nice");
  Vertex v3 = Vertex("great");
  Vertex v4 = Vertex("yes");
  Vertex v5 = Vertex("chill");

  graph.addEdge(v1, v2, true, 5);
  graph.addEdge(v1, v3, false, 2);
  graph.addEdge(v1, v4, true, 10);
  graph.addVertex(v5);
  graph.addEdge(v5, v2, false, 0);

  graph.printGraphAsAdjacencyList();
}