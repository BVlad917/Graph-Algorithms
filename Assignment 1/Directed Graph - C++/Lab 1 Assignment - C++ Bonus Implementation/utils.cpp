//
// Created by VladB on 19-Mar-21.
//

#include "utils.h"
#include "exceptions.h"

#include <map>
#include <fstream>
#include <sstream>
#include <string>
#include <cassert>

DirectedGraph read_graph_from_file(char *file_name) {
    std::ifstream fin(file_name);
    std::string current_line, word;
    int nr_vertices, nr_edges, _from, _to, _cost, vertex, nr_spaces = 0;
    DirectedGraph graph(0);
    getline(fin, current_line);
    std::istringstream aa(current_line);
    aa >> word;
    nr_vertices = stoi(word);
    aa >> word;
    nr_edges = stoi(word);
//    fin >> nr_vertices >> nr_edges;
    while (getline(fin, current_line)) {
        std::istringstream ss(current_line);
        for (auto s: current_line) {
            if (isspace(s)) nr_spaces += 1;
        }
        if (nr_spaces == 0) {
            ss >> word;
            vertex = stoi(word);
            if (!graph.is_vertex_in_graph(vertex)) graph.add_vertex(vertex);
        } else if (nr_spaces == 2) {
            ss >> word, _from = stoi(word);
            ss >> word, _to = stoi(word);
            ss >> word, _cost = stoi(word);
            if (!graph.is_vertex_in_graph(_from)) graph.add_vertex(_from);
            if (!graph.is_vertex_in_graph(_to)) graph.add_vertex(_to);
            graph.add_edge(_from, _to, _cost);
        }
        nr_spaces = 0;
    }
    assert(graph.get_nr_vertices() == nr_vertices);
    assert(graph.get_nr_edges() == nr_edges);
//    for (int i = 0; i < nr_edges; i++) {
//        fin >> _from >> _to >> _cost;
//        graph.add_edge(_from, _to, _cost);
//    }
    fin.close();
    return graph;
}

void write_graph_to_file(char *file_name, DirectedGraph &graph) {
    int current_vertex, neighbour, cost;
    std::ofstream fout(file_name);
//    std::pair<std::map<std::pair<int, int>, int>::iterator, std::map<std::pair<int, int>, int>::iterator> it;
//    it = graph.get_all_edges();

    std::pair<std::map<int, std::set<int>>::iterator, std::map<int, std::set<int>>::iterator> start_end_it;
    start_end_it = graph.out_relations();
    auto start_it = start_end_it.first;
    auto end_it = start_end_it.second;
    std::string graph_str;
    graph_str += std::to_string(graph.get_nr_vertices()) + " " + std::to_string(graph.get_nr_edges()) + "\n";

    for (auto it = start_it; it != end_it; it++) {
        current_vertex = it->first;
        if (graph.get_out_degree(current_vertex) == 0) {
            graph_str += std::to_string(current_vertex) + "\n";
        }
        else {
            std::pair<std::set<int>::iterator, std::set<int>::iterator> neighbours_start_end_it;
            neighbours_start_end_it = graph.get_outbound_neighbours(current_vertex);
            auto neighbours_start_it = neighbours_start_end_it.first;
            auto neighbours_end_it = neighbours_start_end_it.second;

            for (auto n_it = neighbours_start_it; n_it != neighbours_end_it; n_it++) {
                neighbour = *n_it;
                cost = graph.get_cost_of_edge(current_vertex, neighbour);
                graph_str += std::to_string(current_vertex) + " " + std::to_string(neighbour) + " " + std::to_string(cost) + "\n";
            }

        }
    }
    fout << graph_str;
    fout.close();
//    std::string graph_str;
//    graph_str += std::to_string(graph.get_nr_vertices()) + " " + std::to_string(graph.get_nr_edges()) + "\n";
//    for (auto i = it.first; i != it.second; i++) {
//        graph_str += std::to_string(i->first.first) + " " + std::to_string(i->first.second) + " " +
//                     std::to_string(i->second) + "\n";
//    }
//    fout << graph_str;
//    fout.close();
}

DirectedGraph generate_random_graph(int nr_vertices, int nr_edges) {
    if (nr_vertices < 0 || nr_edges < 0) {
        throw GraphException("\nError! Nr. of edges/vertices must be positive.\n");
    }
    if (nr_edges > nr_vertices * (nr_vertices - 1)) {
        throw GraphException("\nError! Too many edges given.\n");
    }
    DirectedGraph random_graph = DirectedGraph(nr_vertices);
    int _from, _to, _cost;
    while (nr_edges) {
        _from = rand() % nr_vertices;
        _to = rand() % nr_vertices;
        _cost = (rand() % 200) - 100;   // Generate costs in the range [-100, 100)
        if (!random_graph.is_edge_in_graph(_from, _to)) {
            random_graph.add_edge(_from, _to, _cost);
            nr_edges -= 1;
        }
    }
    return random_graph;
}