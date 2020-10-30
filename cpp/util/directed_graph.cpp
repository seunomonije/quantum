#include <iostream>
#include <map>
#include <list>
#include <cstring>

using namespace std;

class Vertex {
  public:
    string name;
    Vertex(string nameInput)
      : name(nameInput)
      { }

    /**
     * Overloading to allow use as a key in std::map.
     * Need to compare names of each object so that
     * keys are always unique.
     * 
     * Will this affect adding? Need to test and find out.
     */
    bool operator<(const Vertex& vertexObj) const {
      if (vertexObj.name < this->name){
        return true;
      }
      return false;
    }
};

class Graph {
  std::map< Vertex, list< pair<Vertex, int> > > vertexList;

  public:
    /**
     * Adds a vertex with an empty list to the directed graph.
     */
    void addVertex(Vertex vertex) {
      // Create the map entry with the vertex and an empty list
      list< pair<Vertex, int> > emptyList = {};
      pair<Vertex, list< pair<Vertex, int> > > mapEntry (vertex, emptyList);
      
      vertexList.insert(mapEntry);
    }

    /**
     * Adds an edge to the directed graph given a source, destination, twoWay flag
     * and weight.
     * 
     * twoWay flag signifies if the edge should be bi-directional or not. True = bi-directional.
     */
    void addEdge(Vertex source, Vertex destination, bool twoWay, int weight) {
      pair<Vertex, int> weightedLocation = make_pair(destination, weight);
      vertexList[source].push_back(weightedLocation);

      if (twoWay) {
        pair<Vertex, int> weightedLocation = make_pair(source, weight);
        vertexList[destination].push_back(weightedLocation);
      }
    }

    /**
     * Prints the graph as an adjacency list.
     * 
     */
    void printGraphAsAdjacencyList() {
      for (auto const& [key, value]: vertexList) {
        string vertexName = key.name;
        list< pair<Vertex, int> > destinationList = value;

        cout << vertexName << " --> ";
        // Iterate over every destination pair in the destination list
        for (pair<Vertex,int> destinationPair: destinationList) {
          Vertex vertex = destinationPair.first;
          string vertexName = vertex.name;
          int weight = destinationPair.second;

          cout << vertexName << ":" << weight << " ";
        }
        cout << "\n";
      }
    }
};

int main() {
  cout << "Hello!";
}