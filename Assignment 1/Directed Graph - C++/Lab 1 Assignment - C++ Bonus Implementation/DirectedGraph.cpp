//
// Created by VladB on 18-Mar-21.
//

#include "DirectedGraph.h"
#include "exceptions.h"

DirectedGraph::DirectedGraph(int nr_vertices) {
    for (int i = 0; i < nr_vertices; i++) {
        this->dict_out[i] = std::set<int>();
        this->dict_in[i] = std::set<int>();
    }
}

int DirectedGraph::get_nr_vertices() const {
    return this->dict_out.size();
}

int DirectedGraph::get_nr_edges() const {
    return this->costs.size();
}

std::pair<std::map<int, std::set<int>>::iterator, std::map<int, std::set<int>>::iterator>
DirectedGraph::out_relations() {
    return std::make_pair(this->dict_out.begin(), this->dict_out.end());
}

std::pair<std::map<std::pair<int, int>, int>::iterator, std::map<std::pair<int, int>, int>::iterator>
DirectedGraph::get_all_edges() {
    return std::make_pair(this->costs.begin(), this->costs.end());
}

bool DirectedGraph::is_edge_in_graph(int _from, int _to) {
    return this->costs.find(std::make_pair(_from, _to)) != this->costs.end();
//    return std::find(this->dict_out[_from].begin(), this->dict_out[_from].end(), _to) != this->dict_out[_from].end();
}

int DirectedGraph::get_cost_of_edge(int _from, int _to) {
    if (!this->is_edge_in_graph(_from, _to)) {
        throw GraphException("\nError! The edge is not in the graph.\n");
    }
    return this->costs[std::make_pair(_from, _to)];
}

bool DirectedGraph::is_vertex_in_graph(int vertex) {
    return this->dict_out.find(vertex) != this->dict_out.end();
}

int DirectedGraph::get_in_degree(int vertex) {
    if (!this->is_vertex_in_graph(vertex)) {
        throw GraphException("\nError! The vertex is not in the graph.\n");
    }
    return this->dict_in[vertex].size();
}

int DirectedGraph::get_out_degree(int vertex) {
    if (!this->is_vertex_in_graph(vertex)) {
        throw GraphException("\nError! The vertex is not in the graph.\n");
    }
    return this->dict_out[vertex].size();
}

std::pair<std::set<int>::iterator, std::set<int>::iterator>
DirectedGraph::get_outbound_neighbours(int vertex) {
    if (!this->is_vertex_in_graph(vertex)) {
        throw GraphException("\nError! The vertex is not in the graph.\n");
    }
    return std::make_pair(this->dict_out[vertex].begin(), this->dict_out[vertex].end());
}

int DirectedGraph::get_nr_outbound_neighbours(int vertex) {
    if (!this->is_vertex_in_graph(vertex)) {
        throw GraphException("\nError! The vertex is not in the graph.\n");
    }
    return this->dict_out[vertex].size();
}

std::pair<std::set<int>::iterator, std::set<int>::iterator>
DirectedGraph::get_inbound_neighbours(int vertex) {
    if (!this->is_vertex_in_graph(vertex)) {
        throw GraphException("\nError! The vertex is not in the graph.\n");
    }
    return std::make_pair(this->dict_in[vertex].begin(), this->dict_in[vertex].end());
}

int DirectedGraph::get_nr_inbound_neighbours(int vertex) {
    if (!this->is_vertex_in_graph(vertex)) {
        throw GraphException("\nError! The vertex is not in the graph.\n");
    }
    return this->dict_in[vertex].size();
}

void DirectedGraph::add_vertex(int vertex) {
    if (this->is_vertex_in_graph(vertex)) {
        throw GraphException("\nError! The vertex is already in the graph.\n");
    }
    this->dict_out[vertex] = std::set<int>();
    this->dict_in[vertex] = std::set<int>();
}

void DirectedGraph::remove_vertex(int vertex) {
    // If the vertex is not in the graph throw an exception
    if (!this->is_vertex_in_graph(vertex)) {
        throw GraphException("\nError! The vertex is not in the graph.\n");
    }
    // First, remove the sets of neighbours (inbound and outbound) of the vertex
    this->dict_out.erase(vertex);
    this->dict_in.erase(vertex);
    // Now remove any appearance of vertex in the outbound neighbours and the inbound neighbours
    for (auto &it : this->dict_out) {
        it.second.erase(vertex);
    }
    for (auto &it: this->dict_in) {
        it.second.erase(vertex);
    }
    // Now remove any key-value pair in <costs> if any of the edge vertices in the key are the given vertex
    auto it = this->costs.begin();
    while (it != this->costs.end()) {
        if (it->first.first == vertex || it->first.second == vertex) {
            it = this->costs.erase(it);
        } else {
            it++;
        }
    }

}

void DirectedGraph::add_edge(int _from, int _to, int _cost) {
    // If one of the vertices of the given edge is not in the graph throw an exception
    if (!this->is_vertex_in_graph(_from) || !this->is_vertex_in_graph(_to)) {
        throw GraphException("\nError! Both vertices must be in the graph.\n");
    }
    // If the edge already exists throw an exception
    if (this->is_edge_in_graph(_from, _to)) {
        throw GraphException("\nError! The edge is already in the graph.\n");
    }
    // Now add the element:
    // Add the vertex <_to> in the <dict_out> set of <_from>
    // Add the vertex <_from> in the <dict_in> set of <_to>
    // Add the edge in <costs>
    this->dict_in[_to].insert(_from);
    this->dict_out[_from].insert(_to);
    this->costs[std::make_pair(_from, _to)] = _cost;
}

void DirectedGraph::remove_edge(int _from, int _to) {
    // If one of the vertices of the given edge is not in the graph throw an exception
    if (!this->is_vertex_in_graph(_from) || !this->is_vertex_in_graph(_to)) {
        throw GraphException("\nError! Both vertices must be in the graph.\n");
    }
    // If the edge is not in the graph => throw an exception
    if (!this->is_edge_in_graph(_from, _to)) {
        throw GraphException("\nError! The edge is not in the graph.\n");
    }
    // Remove <_from> from <dict_in[_to]>, <_to> from <dict_out[from]>, and the element with key <_from, _to>
    // from <costs>
    this->dict_in[_to].erase(_from);
    this->dict_out[_from].erase(_to);
    this->costs.erase(std::make_pair(_from, _to));
}

void DirectedGraph::change_cost(int _from, int _to, int _new_cost) {
    // If one of the vertices of the given edge is not in the graph throw an exception
    if (!this->is_vertex_in_graph(_from) || !this->is_vertex_in_graph(_to)) {
        throw GraphException("\nError! Both vertices must be in the graph.\n");
    }
    // If the edge is not in the graph => throw an exception
    if (!this->is_edge_in_graph(_from, _to)) {
        throw GraphException("\nError! The edge is not in the graph.\n");
    }
    this->costs[std::make_pair(_from, _to)] = _new_cost;
}

DirectedGraph DirectedGraph::copy_graph() {
    DirectedGraph new_graph = DirectedGraph(this->get_nr_vertices());
    // First we copy all the costs
    for (auto & cost : this->costs) {
        new_graph.costs[std::make_pair(cost.first.first, cost.first.second)] = cost.second;
    }
    // Now copy all the elements from <dict_in>
    for (auto & map_it : this->dict_in) {
        for (auto set_it = map_it.second.begin(); set_it != map_it.second.end(); set_it++) {
            new_graph.dict_in[map_it.first].insert(*set_it);
        }
    }
    // Now copy all the elements from <dict_out>
    for (auto & map_it : this->dict_out) {
        for (auto set_it = map_it.second.begin(); set_it != map_it.second.end(); set_it++) {
            new_graph.dict_out[map_it.first].insert(*set_it);
        }
    }
    // All the information related to the graph was copied. Now return the copy of the graph
    return new_graph;
}

