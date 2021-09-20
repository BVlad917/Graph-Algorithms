//
// Created by VladB on 19-Mar-21.
//

#include <iostream>
#include <cassert>
#include <exception>

#include "tests.h"
#include "utils.h"

using namespace std;

void test_read_graph() {
    // read from file
    char file_name[] = "test_in_graph.txt";
    DirectedGraph graph = read_graph_from_file(file_name);
    // test some getters
    assert(graph.get_nr_vertices() == 5);
    assert(graph.get_nr_edges() == 6);
    // see if is_edge_in_graph() works
    assert(graph.is_edge_in_graph(0, 0) == true);
    assert(graph.is_edge_in_graph(2, 1) == true);
    assert(graph.is_edge_in_graph(1, 2) == true);
    assert(graph.is_edge_in_graph(1, 4) == false);
    // see if is_vertex_in_graph() works
    assert(graph.is_vertex_in_graph(0) == true);
    assert(graph.is_vertex_in_graph(2) == true);
    assert(graph.is_vertex_in_graph(4) == true);
    assert(graph.is_vertex_in_graph(5) == false);
    // more getters
    assert(graph.get_cost_of_edge(0, 0) == 1);
    assert(graph.get_cost_of_edge(1, 2) == 2);
    // see that an exception is raised if we get the cost of a non-existing edge
    bool exception_raised = false;
    try {
        graph.get_cost_of_edge(1, 4);
    }
    catch (exception&) {
        exception_raised = true;
    }
    assert(exception_raised == true);
    // test in_degree() and that it throws an exception in the case of non-existing vertex
    assert(graph.get_in_degree(1) == 2);
    assert(graph.get_in_degree(4) == 0);
    exception_raised = false;
    try {
        graph.get_in_degree(13);
    }
    catch (exception&) {
        exception_raised = true;
    }
    assert(exception_raised == true);
    // test out_degree() and that it throws an exception in the case of non-existing vertex
    assert(graph.get_out_degree(2) == 2);
    assert(graph.get_out_degree(1) == 2);
    exception_raised = false;
    try {
        graph.get_out_degree(13);
    }
    catch (exception&) {
        exception_raised = true;
    }
    assert(exception_raised == true);
}

void test_add_vertex_and_edge() {
    char file_name[] = "test_in_graph.txt";
    DirectedGraph graph = read_graph_from_file(file_name);
    assert(graph.get_nr_vertices() == 5);
    assert(graph.get_nr_edges() == 6);
    // add vertex
    graph.add_vertex(10);
    assert(graph.get_nr_vertices() == 6);
    assert(graph.is_vertex_in_graph(10) == true);
    bool exc = false;
    try {
        graph.add_vertex(10);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
    // add edge
    graph.add_edge(1, 4, 20);
    assert(graph.get_nr_edges() == 7);
    assert(graph.get_nr_vertices() == 6);
    assert(graph.is_edge_in_graph(1, 4) == true);
    // throw exception if an already existing edge is added
    exc = false;
    try {
        graph.add_edge(1, 2, 100);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
    // throw exception if an edge with non-existing vertices is added
    exc = false;
    try {
        graph.add_edge(1, 27, 101);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
}

void test_remove_edge() {
    char file_name[] = "test_in_graph.txt";
    DirectedGraph graph = read_graph_from_file(file_name);
    assert(graph.get_nr_vertices() == 5);
    assert(graph.get_nr_edges() == 6);
    // remove edge
    graph.remove_edge(1, 3);
    assert(graph.get_nr_vertices() == 5);
    assert(graph.get_nr_edges() == 5);
    bool exc = false;
    try {
        graph.remove_edge(1, 10);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
}

void test_remove_vertex() {
    char file_name[] = "test_in_graph.txt";
    DirectedGraph graph = read_graph_from_file(file_name);
    assert(graph.get_nr_vertices() == 5);
    assert(graph.get_nr_edges() == 6);
    // remove vertex
    graph.remove_vertex(2);
    assert(graph.get_nr_vertices() == 4);
    assert(graph.get_nr_edges() == 3);
    assert(graph.is_edge_in_graph(0, 0) == true);
    assert(graph.is_edge_in_graph(0, 1) == true);
    assert(graph.is_edge_in_graph(1, 2) == false);
    assert(graph.is_edge_in_graph(2, 1) == false);
    assert(graph.is_edge_in_graph(1, 3) == true);
    assert(graph.is_edge_in_graph(2, 3) == false);
    // remove a non-existing vertex => throw exception
    bool exc = false;
    try {
        graph.remove_vertex(13);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
    // get_in_degree of vertex AFTER that vertex was remove => exception
    exc = false;
    try {
        graph.get_in_degree(2);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
    // get_out_degree of vertex AFTER that vertex was remove => exception
    exc = false;
    try {
        graph.get_out_degree(2);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
}

void test_change_edge_cost() {
    char file_name[] = "test_in_graph.txt";
    DirectedGraph graph = read_graph_from_file(file_name);
    assert(graph.get_nr_vertices() == 5);
    assert(graph.get_nr_edges() == 6);
    assert(graph.get_cost_of_edge(1, 3) == 8);
    graph.change_cost(1, 3, 20);
    assert(graph.get_cost_of_edge(1, 3) == 20);
    assert(graph.get_nr_vertices() == 5);
    assert(graph.get_nr_edges() == 6);
    // Change cost of non-existing edge => exception
    bool exc = false;
    try {
        graph.change_cost(1, 4, 10);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
    // Change cost with vertices that are NOT in the graph => exception
    exc = false;
    try {
        graph.change_cost(20, 30, 7);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
}

void test_get_outbound_neighbours() {
    char file_name[] = "test_in_graph.txt";
    DirectedGraph graph = read_graph_from_file(file_name);
    assert(graph.get_nr_vertices() == 5);
    assert(graph.get_nr_edges() == 6);
    pair<set<int>::iterator, set<int>::iterator> start_end_iter = graph.get_outbound_neighbours(2);
    auto it_start = start_end_iter.first, it_end = start_end_iter.second;
    int i = 0, expected[10] = {1, 3};
    for (auto it = it_start; it != it_end; it++) {
        assert(*it == expected[i]);
        i += 1;
    }
    assert(i == 2);
    start_end_iter = graph.get_outbound_neighbours(3);
    it_start = start_end_iter.first, it_end = start_end_iter.second;
    i = 0;
    for (auto it = it_start; it != it_end; it++) {
        assert(*it == expected[i]);
        i += 1;
    }
    // vertex 3 has no outbound neighbours => i does not increase
    assert(i == 0);
    bool exc = false;
    try {
        graph.get_outbound_neighbours(13);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
}

void test_get_inbound_neighbours() {
    char file_name[] = "test_in_graph.txt";
    DirectedGraph graph = read_graph_from_file(file_name);
    assert(graph.get_nr_vertices() == 5);
    assert(graph.get_nr_edges() == 6);
    graph.remove_vertex(2);
    assert(graph.get_nr_vertices() == 4);
    assert(graph.get_nr_edges() == 3);
    pair<set<int>::iterator, set<int>::iterator> start_end_iter = graph.get_inbound_neighbours(1);
    auto it_start = start_end_iter.first, it_end = start_end_iter.second;
    int i = 0, expected = 0;
    for (auto it = it_start; it != it_end; it++) {
        assert(*it == expected);
        i += 1;
    }
    assert(i == 1);
    assert(graph.is_edge_in_graph(0, 1) == true);
    bool exc = false;
    try {
        graph.get_inbound_neighbours(2);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
    exc = false;
    try {
        graph.get_outbound_neighbours(13);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
}

void test_out_relations() {
    char file_name[] = "test_in_graph.txt";
    DirectedGraph graph = read_graph_from_file(file_name);
    assert(graph.get_nr_vertices() == 5);
    assert(graph.get_nr_edges() == 6);
    std::pair<std::map<int, std::set<int>>::iterator, std::map<int, std::set<int>>::iterator> it_start_and_end;
    // We can use <graph.out_relations()> to get all the vertices from the graph
    it_start_and_end = graph.out_relations();
    auto it_start = it_start_and_end.first, it_end = it_start_and_end.second;
    int i = 0, expected[] = {0, 1, 2, 3, 4};
    for (auto it=it_start; it!=it_end; it++) {
        assert(it->first == expected[i]);
        i += 1;
    }
    assert(i == 5);
}

void test_copy_graph() {
    char file_name[] = "test_in_graph.txt";
    DirectedGraph graph = read_graph_from_file(file_name);
    assert(graph.get_nr_vertices() == 5);
    assert(graph.get_nr_edges() == 6);

//    DirectedGraph copy = graph;   <- This works equally well; Default C++ copy constructor is enough in this context
    DirectedGraph copy = graph.copy_graph();
    assert(copy.get_nr_vertices() == 5);
    assert(copy.get_nr_edges() == 6);
    // test that changing one graph does not change the other
    // first remove an edge from one and not from the other
    copy.remove_edge(1, 3);
    assert(copy.get_nr_edges() == 5);
    assert(copy.get_nr_vertices() == 5);
    assert(graph.get_nr_edges() == 6);
    assert(graph.get_nr_vertices() == 5);
    assert(copy.is_edge_in_graph(1, 3) == false);
    assert(graph.is_edge_in_graph(1, 3) == true);
    // now remove a vertex from one and not from the other
    graph.remove_vertex(2);
    assert(graph.get_nr_edges() == 3);
    assert(graph.get_nr_vertices() == 4);
    assert(copy.get_nr_edges() == 5);
    assert(copy.get_nr_vertices() == 5);
}

void test_nr_neighbours() {
    char file_name[] = "test_in_graph.txt";
    DirectedGraph graph = read_graph_from_file(file_name);
    assert(graph.get_nr_vertices() == 5);
    assert(graph.get_nr_edges() == 6);
    // test number of outbound neighbours
    assert(graph.get_nr_outbound_neighbours(2) == 2);
    assert(graph.get_nr_outbound_neighbours(3) == 0);
    bool exc = false;
    try {
        graph.get_nr_outbound_neighbours(13);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
    // test number of inbound neighbours
    assert(graph.get_nr_inbound_neighbours(2) == 1);
    assert(graph.get_nr_inbound_neighbours(3) == 2);
    exc = false;
    try {
        graph.get_nr_inbound_neighbours(13);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
    // remove a vertex and then test the number of inbound/outbound neighbours
    // test the number of inbound neighbours first
    graph.remove_vertex(2);
    assert(graph.get_nr_inbound_neighbours(0) == 1);
    assert(graph.get_nr_inbound_neighbours(1) == 1);
    assert(graph.get_nr_inbound_neighbours(3) == 1);
    assert(graph.get_nr_inbound_neighbours(4) == 0);
    // vertex 2 is no longer in the graph => trying to get its number of neighbours throws an exception
    exc = false;
    try {
        graph.get_nr_inbound_neighbours(2);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
    // test the number of outbound neighbours now
    assert(graph.get_nr_outbound_neighbours(0) == 2);
    assert(graph.get_nr_outbound_neighbours(1) == 1);
    assert(graph.get_nr_outbound_neighbours(3) == 0);
    assert(graph.get_nr_outbound_neighbours(4) == 0);
    exc = false;
    try {
        graph.get_nr_outbound_neighbours(2);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
}

void test_random_graph_generator() {
    DirectedGraph random_graph = generate_random_graph(5, 6);
    assert(random_graph.get_nr_vertices() == 5);
    assert(random_graph.get_nr_edges() == 6);
    // if negative values are given for nr_vertices/nr_edges => exception thrown
    bool exc = false;
    try {
        generate_random_graph(-7, -8);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
    // if nr_edges > nr_vertices * (nr_vertices - 1) => impossible to build graph => exception thrown
    exc = false;
    try {
        generate_random_graph(5, 25);
    }
    catch (exception&) {
        exc = true;
    }
    assert(exc == true);
}

void test_write_graph_to_file() {
    char file_name[] = "test_in_graph.txt";
    DirectedGraph graph = read_graph_from_file(file_name);
    assert(graph.get_nr_vertices() == 5);
    assert(graph.get_nr_edges() == 6);
//    graph.remove_vertex(2);
//    graph.add_vertex(5);
//    graph.add_vertex(6);
//    graph.add_edge(0, 4, 10);
//    graph.add_edge(5, 6, 15);
//    graph.add_edge(4, 0, -2);
//    assert(graph.get_nr_vertices() == 6);
//    assert(graph.get_nr_edges() == 6);
    char output_file_name[] = "test_out_graph.txt";
    write_graph_to_file(output_file_name, graph);
}

void run_all_tests() {
    test_read_graph();
    test_add_vertex_and_edge();
    test_remove_edge();
    test_remove_vertex();
    test_change_edge_cost();
    test_get_outbound_neighbours();
    test_get_inbound_neighbours();
    test_out_relations();
    test_copy_graph();
    test_nr_neighbours();
    test_random_graph_generator();
    test_write_graph_to_file();
}