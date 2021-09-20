//
// Created by VladB on 18-Mar-21.
//

#ifndef LAB_1_ASSIGNMENT___C___BONUS_IMPLEMENTATION_DIRECTEDGRAPH_H
#define LAB_1_ASSIGNMENT___C___BONUS_IMPLEMENTATION_DIRECTEDGRAPH_H

#include <map>
#include <set>
#include <iterator>

class DirectedGraph {
private:
    std::map<int, std::set<int>> dict_out;
    std::map<int, std::set<int>> dict_in;
    std::map<std::pair<int, int>, int> costs;
public:
    /*
        Constructor. Builds a graph with <nr_vertices> vertices using a triple map representation.
        Initializes the sets of outbound and inbound neighbours for each vertex of the vertex.
        Input: nr_vertices - Integer
        Output: a new graph is generated
     */
    explicit DirectedGraph(int nr_vertices = 0);    // todo: change to nr_vertices = 0, see if it still works

    /*
        Returns the number of vertices in the graph.
        Output: How many vertices the graph has; Integer
     */
    int get_nr_vertices() const;

    /*
        Returns the number of edges in the graph.
        Output: How many edges the graph has; Integer
     */
    int get_nr_edges() const;

    /*
        Returns 2 iterators in a pair: one at the start of the map which represents the outbound
        relationships (each vertex is mapped to a set of outbound vertices) and another iterator at
        the end of this map. This function can be used for getting all the vertices in the graph (by using
        the <.first> attribute of the iterators)
        Output: A pair of 2 iterators, each being an iterator to a map between an Integer and a Set.
     */
    std::pair<std::map<int, std::set<int>>::iterator, std::map<int, std::set<int>>::iterator> out_relations();

    /*
        Returns 2 iterators in a pair: one at the start of the map which represents the costs of the graph (each
        edge (as a pair of 2 Integers) is mapped to a cost, Integer) and another iterator at the end of this map.
        Output: A pair of 2 iterators, each being an iterator to a map between a pair of Integers and an Integer.
     */
    std::pair<std::map<std::pair<int, int>, int>::iterator, std::map<std::pair<int, int>, int>::iterator> get_all_edges();

    /*
        Checks if a given edge is in the graph.
        Input: _from - Integer, starting vertex of an edge; _to - Integer, ending vertex of an edge
        Output: true - If the given edge is present in the graph; false - Otherwise
     */
    bool is_edge_in_graph(int _from, int _to);

    /*
        Returns the cost of a given edge in the graph if it exists
        Input: _from - Integer, starting vertex of an edge; _to - Integer, ending vertex of an edge
        Output: The cost of the edge in the graph, Integer
        Throws: An exception if the given edge is not in the graph or if one of the vertices is not in the graph
     */
    int get_cost_of_edge(int _from, int _to);

    /*
        Checks if a given vertex is in the graph.
        Input: vertex - Integer
        Output: true - If the given vertex is in the graph; false - Otherwise
     */
    bool is_vertex_in_graph(int vertex);

    /*
        Returns the in-degree of a vertex.
        Input: vertex - Integer
        Output: Integer - The number of vertices which come into <vertex>
        Throws: An exception if the given vertex is not in the graph
     */
    int get_in_degree(int vertex);

    /*
        Returns the out-degree of a vertex.
        Input: vertex - Integer
        Output: Integer - The number of vertices which <vertex> goes into
        Throws: An exception if the given vertex is not in the graph
     */
    int get_out_degree(int vertex);

    /*
        Returns a pair of 2 iterators: one at the start of the set of outbound neighbours of the given vertex
        and one at the end of this same set.
        Input: vertex - Integer
        Output: A pair of 2 iterators, each being an iterator to a set of Integers
        Throws: Exception - if the given vertex is not in the graph
     */
    std::pair<std::set<int>::iterator, std::set<int>::iterator> get_outbound_neighbours(int vertex);

    /*
        Returns the number of outbound neighbours of a vertex.
        Input: vertex - Integer
        Output: Integer, the number of vertices which <vertex> goes into
        Throws: Exception - if the given vertex is not in the graph
     */
    int get_nr_outbound_neighbours(int vertex);

    /*
        Returns a pair of 2 iterators: one at the start of the set of inbound neighbours of the given vertex
        and one at the nd of this same set.
        Input: vertex - Integer
        Output: A pair of 2 iterators, each being an iterator to a set of Integers
     */
    std::pair<std::set<int>::iterator, std::set<int>::iterator> get_inbound_neighbours(int vertex);

    /*
        Returns the number of inbound neighbours of a vertex.
        Input: vertex - Integer
        Output: Integer, the number of vertices which go into <vertex>
        Throws: Exception - if the given vertex is not in the graph.
     */
    int get_nr_inbound_neighbours(int vertex);

    /*
        Adds a new vertex to the graph.
        Input: vertex - Integer
        Throws: Exception - if the vertex is already in the graph
     */
    void add_vertex(int vertex);

    /*
        Removes a vertex from the graph.
        Input: vertex - Integer
        Throws: Exception - if the vertex is not in the graph
     */
    void remove_vertex(int vertex);

    /*
        Adds a new edge in the graph
        Input: _from, _to - Integers, starting and ending vertices of the edge; _cost - Integer, cost of the edge
        Throws: Exception - if the edge is already in the graph, or if one of the vertices is NOT in the graph
     */
    void add_edge(int _from, int _to, int _cost);

    /*
        Removes an edge from the graph.
        Input: _from, _to - Integers, starting and ending vertices of the edge
        Throws: Exception - if the edge is not in the graph, or if of of the vertices is NOT in the graph
     */
    void remove_edge(int _from, int _to);

    /*
        Changes the cost of an edge.
        Input: _from, _to - Integers, starting and ending vertices of the edge
        Throws: Exception - if the edge is not in the graph, or if of of the vertices is NOT in the graph
     */
    void change_cost(int _from, int _to, int _new_cost);

    /*
        Returns a deepcopy of the graph.
     */
    DirectedGraph copy_graph();
};


#endif //LAB_1_ASSIGNMENT___C___BONUS_IMPLEMENTATION_DIRECTEDGRAPH_H
