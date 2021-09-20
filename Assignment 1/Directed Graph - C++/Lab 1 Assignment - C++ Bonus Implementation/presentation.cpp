//
// Created by VladB on 20-Mar-21.
//

#include <iostream>
#include <string>

#include "presentation.h"
#include "utils.h"
#include "exceptions.h"

UI::UI(DirectedGraph &graph): graph(graph) {}

void UI::ui_get_number_of_vertices() {
    int nr_vertices = this->graph.get_nr_vertices();
    std::cout << "\nThe number of vertices in the graph is " << nr_vertices << "\n";
}

void UI::ui_get_number_of_edges() {
    int nr_edges = this->graph.get_nr_edges();
    std::cout << "\nThe number of edges in the graph is " << nr_edges << "\n";
}

void UI::run_app() {
    int cmd_as_int;
    std::string cmd;
    bool run_app = true;
    while (run_app) {
        UI::print_menu();
        std::cout << "\nPlease give a command: ";
        std::cin >> cmd;
        cmd_as_int = atoi(cmd.c_str());
        try {
            switch (cmd_as_int) {
                case 1:
                    this->ui_get_number_of_vertices();
                    break;
                case 2:
                    this->ui_get_number_of_edges();
                    break;
                case 3:
                    this->ui_get_vertices();
                    break;
                case 4:
                    this->ui_get_edges();
                    break;
                case 5:
                    this->ui_check_vertex();
                    break;
                case 6:
                    this->ui_check_edge();
                    break;
                case 7:
                    this->ui_get_cost_of_edge();
                    break;
                case 8:
                    this->ui_in_degree_of_vertex();
                    break;
                case 9:
                    this->ui_out_degree_of_vertex();
                    break;
                case 10:
                    this->ui_outbound_neighbours();
                    break;
                case 11:
                    this->ui_inbound_neighbours();
                    break;
                case 12:
                    this->ui_change_edge_cost();
                    break;
                case 13:
                    this->ui_add_edge();
                    break;
                case 14:
                    this->ui_remove_edge();
                    break;
                case 15:
                    this->ui_add_vertex();
                    break;
                case 16:
                    this->ui_remove_vertex();
                    break;
                case 17:
                    this->ui_write_graph_to_file();
                    break;
                case 18:
                    run_app = false;
                    break;
                default:
                    std::cout << "\nInvalid command given.\n";
                    break;
            }
        }
        catch (GraphException& ge) {
            std::cout << ge.what();
        }
    }
}

void UI::print_menu() {
    std::cout << "\nGraph operations:\n"
                 "\t1 - Get the number of vertices in the graph\n"
                 "\t2 - Get the number of edges in the graph\n"
                 "\t3 - Get the set of vertices in the graph\n"
                 "\t4 - Get the set of edges in the graph\n"
                 "\t5 - Check if a given vertex is in the graph\n"
                 "\t6 - Check if there is an edge between 2 vertices\n"
                 "\t7 - Get the cost of an edge\n"
                 "\t8 - Get the in degree of a vertex\n"
                 "\t9 - Get the out degree of a vertex\n"
                 "\t10 - Get the outbound neighbours of a vertex\n"
                 "\t11 - Get the inbound neighbours of a vertex\n"
                 "\t12 - Modify the cost of an edge\n"
                 "\t13 - Add an edge\n"
                 "\t14 - Remove an edge\n"
                 "\t15 - Add a vertex\n"
                 "\t16 - Remove a vertex\n"
                 "\t17 - Write the graph to a file\n"
                 "\t18 - Exit\n";
}

void UI::ui_get_vertices() {
    if (this->graph.get_nr_vertices() == 0) {
        std::cout << "\nThere are no vertices in the graph.\n";
        return;
    }
    std::pair<std::map<int, std::set<int>>::iterator, std::map<int, std::set<int>>::iterator> start_end_it;
    start_end_it = this->graph.out_relations();
    auto start_it = start_end_it.first;
    auto end_it = start_end_it.second;
    std::cout << "\nThese are the vertices from the graph: ";
    for (auto it = start_it; it != end_it; it++) {
        std::cout << it->first << " ";
    }
}

void UI::ui_get_edges() {
    if (this->graph.get_nr_edges() == 0) {
        std::cout << "\nThe graph has no edges.\n";
        return;
    }
    std::pair<std::map<std::pair<int, int>, int>::iterator, std::map<std::pair<int, int>, int>::iterator> start_end_it;
    start_end_it = this->graph.get_all_edges();
    auto start_it = start_end_it.first;
    auto end_it = start_end_it.second;
    std::cout << "\nThese are all the edges from the graph:\n";
    for (auto it = start_it; it != end_it; it++) {
        std::cout << it->first.first << "->" << it->first.second << ", cost of " << it->second << "\n";
    }
}

void UI::ui_check_vertex() {
    int vertex;
    std::cout << "\nGive the vertex: ";
    std::cin >> vertex;
    if (this->graph.is_vertex_in_graph(vertex)) {
        std::cout << "\nYes, the vertex " << vertex << " is in the graph.\n";
    }
    else {
        std::cout << "\nNo, the vertex " << vertex << " is NOT in the graph.\n";
    }
}

void UI::ui_check_edge() {
    int from, to;
    std::cout << "\nGive the starting vertex of the graph: ";
    std::cin >> from;
    std::cout << "\nGive the ending vertex of the graph: ";
    std::cin >> to;
    if (this->graph.is_edge_in_graph(from, to)) {
        int cost = this->graph.get_cost_of_edge(from, to);
        std::cout << "\nYes, the edge " << from << "->" << to << " is in the graph(cost of " << cost << ")\n";
    }else {
        std::cout << "\nNo, the edge " << from << "->" << to << " is NOT in the graph\n";
    }
}

void UI::ui_get_cost_of_edge() {
    int from, to;
    std::cout << "\nGive the starting vertex of the edge: ";
    std::cin >> from;
    std::cout << "\nGive the ending vertex of the edge: ";
    std::cin >> to;
    int cost = this->graph.get_cost_of_edge(from, to);
    std::cout << "\nThe cost of the edge " << from << "->" << to << "is " << cost << "\n";
}

void UI::ui_in_degree_of_vertex() {
    int vertex;
    std::cout << "\nGive the vertex number: ";
    std::cin >> vertex;
    int in_degree = this->graph.get_in_degree(vertex);
    std::cout << "\nThe in-degree of the vertex " << vertex << " is " << in_degree << "\n";
}

void UI::ui_out_degree_of_vertex() {
    int vertex;
    std::cout << "\nGive the vertex number: ";
    std::cin >> vertex;
    int out_degree = this->graph.get_out_degree(vertex);
    std::cout << "\nThe out-degree of the vertex " << vertex << " is " << out_degree << "\n";
}

void UI::ui_outbound_neighbours() {
    int vertex;
    std::cout << "\nGive the vertex number: ";
    std::cin >> vertex;
    if (this->graph.get_out_degree(vertex) == 0) {
        std::cout << "\nThe vertex " << vertex << " has no outbound neighbours.\n";
        return;
    }
    std::pair<std::set<int>::iterator, std::set<int>::iterator> start_end_it;
    start_end_it = this->graph.get_outbound_neighbours(vertex);
    auto start_it = start_end_it.first;
    auto end_it = start_end_it.second;
    int neighbour, cost;
    std::cout << "\nThe outbound neighbours of vertex " << vertex << " are:\n";
    for (auto it = start_it; it != end_it; it++) {
        neighbour = *it;
        cost = this->graph.get_cost_of_edge(vertex, neighbour);
        std::cout << neighbour << " (cost of " << cost << ")\n";
    }
}

void UI::ui_inbound_neighbours() {
    int vertex;
    std::cout << "\nGive the vertex number: ";
    std::cin >> vertex;
    if (this->graph.get_in_degree(vertex) == 0) {
        std::cout << "\nThe vertex " << vertex << " has no inbound neighbours.\n";
        return;
    }
    std::pair<std::set<int>::iterator, std::set<int>::iterator> start_end_it;
    start_end_it = this->graph.get_inbound_neighbours(vertex);
    auto start_it = start_end_it.first;
    auto end_it = start_end_it.second;
    int neighbour, cost;
    std::cout << "\nThe inbound neighbours of vertex " << vertex << " are:\n";
    for (auto it = start_it; it != end_it; it++) {
        neighbour = *it;
        cost = this->graph.get_cost_of_edge(neighbour, vertex);
        std::cout << neighbour << " (cost of " << cost << ")\n";
    }
}

void UI::ui_change_edge_cost() {
    int from, to, new_cost;
    std::cout << "\nGive the starting vertex of the edge: ";
    std::cin >> from;
    std::cout << "\nGive the ending vertex of the edge: ";
    std::cin >> to;
    std::cout << "\nGive the new cost of the edge: ";
    std::cin >> new_cost;
    this->graph.change_cost(from, to, new_cost);
    std::cout << "\nThe cost of the edge " << from << "->" << to << " was changed to " << new_cost << "\n";
}

void UI::ui_add_edge() {
    int from, to, cost;
    std::cout << "\nGive the starting vertex of the new edge: ";
    std::cin >> from;
    std::cout << "\nGive the ending vertex of the new edge: ";
    std::cin >> to;
    std::cout << "\nGive the cost of the new edge: ";
    std::cin >> cost;
    this->graph.add_edge(from, to, cost);
    std::cout << "\nThe edge " << from << "->" << to << "(cost of " << cost << ") was added to the graph.\n";
}

void UI::ui_remove_edge() {
    int from, to;
    std::cout << "\nGive the starting vertex of the edge: ";
    std::cin >> from;
    std::cout << "\nGive the ending vertex of the edge: ";
    std::cin >> to;
    this->graph.remove_edge(from, to);
    std::cout << "\nThe edge was removed.\n";
}

void UI::ui_add_vertex() {
    int vertex;
    std::cout << "\nGive the number of the new vertex: ";
    std::cin >> vertex;
    this->graph.add_vertex(vertex);
    std::cout << "\nThe vertex " << vertex << " was added to the graph.\n";
}

void UI::ui_remove_vertex() {
    int vertex;
    std::cout << "\nGive the number of the vertex: ";
    std::cin >> vertex;
    this->graph.remove_vertex(vertex);
    std::cout << "\nThe vertex " << vertex << " was removed from the graph.\n";
}

void UI::ui_write_graph_to_file() {
    char file_name[256];
    std::cout << "\nGive the name of the file (with extension): ";
    getchar();
    std::cin.getline(file_name, sizeof(file_name));
    write_graph_to_file(file_name, this->graph);
    std::cout << "\nThe graph was saved in " << file_name << "\n";
}




