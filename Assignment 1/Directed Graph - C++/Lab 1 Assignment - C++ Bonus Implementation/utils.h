//
// Created by VladB on 19-Mar-21.
//

#ifndef LAB_1_ASSIGNMENT___C___BONUS_IMPLEMENTATION_UTILS_H
#define LAB_1_ASSIGNMENT___C___BONUS_IMPLEMENTATION_UTILS_H

#include "DirectedGraph.h"

/*
    Reads the graph from a file, builds that graph, and returns it.
    Input: file_name - pointer to char, the name of the file
    Output: a new instance of the class <DirectedGraph>; the graph from the file
 */
DirectedGraph read_graph_from_file(char *file_name);

/*
    Writes the given graph to a file.
    Input: file_name - pointer to char, the name of the file
           graph - a reference to a graph object
 */
void write_graph_to_file(char *file_name, DirectedGraph& graph);

/*
    Creates a random graph with <nr_vertices> vertices and <nr_edges> edges.
    Input: nr_vertices - integer, the number of vertices
           nr_edges - integer, the number of edges
    Output: a new instance of the class <DirectedGraph>, the randomly generated graph
 */
DirectedGraph generate_random_graph(int nr_vertices, int nr_edges);

#endif //LAB_1_ASSIGNMENT___C___BONUS_IMPLEMENTATION_UTILS_H
