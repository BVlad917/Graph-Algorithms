import random

from copy import deepcopy

import graphviz
import numpy

from errors import GraphException
from queue import PriorityQueue

MAX_GRAPH_COST = 100  # We use this for the costs of the randomly generated graphs
INFINITY = 999999999999999  # We use this to define the default value used as infinity


class UndirectedGraph:
    def __init__(self, no_vertices=0):
        """
        Creates a graph represented by 3 dictionaries with <no_vertices> vertices (optional argument).
        """
        self.__neighbours = {}
        self.__cost = {}
        for i in range(no_vertices):
            self.__neighbours[i] = []

    def get_no_vertices(self):
        """
        Returns the number of vertices in the graph.
        """
        return len(self.__neighbours.keys())

    def get_no_edges(self):
        """
        Returns the number of edges in the graph.
        """
        return len(self.__cost.keys())

    def get_all_vertices(self):
        """
        Returns all the vertices from the graph using an iterator.
        """
        for vertex in self.__neighbours.keys():
            yield vertex

    def get_all_edges(self):
        """
        Using a generator, returns all the edges in the graph as triples in the following format (_from, _to, cost):
        <_from> - starting vertex,
        <_to> - ending index
        <cost> - the weight of the edge.
        """
        for key, value in self.__cost.items():
            yield key[0], key[1], value

    def get_cost_of_edge(self, _from, _to):
        """
        Returns the weight of a given edge (given by the starting and ending vertices). If the given edge does not
        exist an exception is thrown (GraphException).
        :param _from: The starting vertex of the edge; integer
        :param _to: The ending vertex of the edge; integer
        :return: The cost of the edge <_from> -> <_to>
        :preconditions: The edge <_from> -> <_to> is in the graph
        """
        if (_from, _to) in self.__cost.keys():
            return self.__cost[(_from, _to)]
        elif (_to, _from) in self.__cost.keys():
            return self.__cost[(_to, _from)]
        else:
            raise GraphException("The given edge does not exist.")

    def is_edge_in_graph(self, _from, _to):
        """
        Returns True if there exists an edge between the 2 given vertices in the graph; False otherwise. If one of
        the given vertices does not exist in the graph an exception is thrown (GraphException).
        :param _from: The starting vertex of the edge; integer
        :param _to: The ending vertex of the edge; integer
        :return: True if the given edge exists; False otherwise
        """
        if not self.is_vertex_in_graph(_from):
            raise GraphException(f"The vertex {_from} does not exist in the graph.")
        if not self.is_vertex_in_graph(_to):
            raise GraphException(f"The vertex {_to} does not exist in the graph.")
        return _from in self.__neighbours[_to] and _to in self.__neighbours[_from]

    def is_vertex_in_graph(self, vertex):
        """
        Checks if the given vertex exists in the graph or not
        :param vertex: The vertex we want to check; integer
        :return: True if the vertex is in the graph; False otherwise
        """
        return vertex in self.__neighbours.keys()

    def get_degree(self, vertex):
        """
        Returns the degree of a given vertex. If the given vertex does not exist in the graph an exception is
        thrown (GraphException).
        :param vertex: The vertex whose degree we want; integer
        :return: The degree of <vertex>
        :preconditions: The vertex exists in the graph
        """
        if not self.is_vertex_in_graph(vertex):
            raise GraphException(f"The vertex {vertex} does not exist in the graph.")
        return len(self.__neighbours[vertex])

    def get_neighbours(self, vertex):
        """
        Returns the neighbours of a given vertex. If the given vertex does not exist in the graph an
        exception is thrown (GraphException).
        :param vertex: The vertex whose neighbours we want; integer
        :return: A generator with the neighbours of the given vertex
        :preconditions: The vertex exists in the graph
        """
        if not self.is_vertex_in_graph(vertex):
            raise GraphException(f"The vertex {vertex} does not exist in the graph.")
        for neighbour in self.__neighbours[vertex]:
            yield neighbour

    def get_neighbours_with_cost(self, vertex):
        """
        Using a generator, returns all of the neighbours of a vertex, along with the cost of the edge from
        the given vertex to its neighbour.
        :param vertex: The vertex whose neighbours we want; integer
        :return: A generator with (neighbour, cost) type pairs
        """
        if not self.is_vertex_in_graph(vertex):
            raise GraphException(f"The vertex {vertex} does not exist in the graph.")
        for neighbour in self.__neighbours[vertex]:
            yield neighbour, self.get_cost_of_edge(vertex, neighbour)

    def change_edge_cost(self, _from, _to, new_cost):
        """
        Changes the cost of an edge given by its starting and ending vertices. If the edge does not exist in the
        graph an exception is thrown (GraphException).
        :param _from: The starting vertex of the edge; integer
        :param _to: The ending vertex of the edge; integer
        :param new_cost: The new cost of the edge; integer
        :return: -
        :preconditions: Both vertices are in the graph and there exists an edge between these 2 vertices.
        """
        if not self.is_edge_in_graph(_from, _to):
            raise GraphException("The edge does not exist in the graph.")
        self.__cost[(_from, _to)] = new_cost
        self.__cost[(_to, _from)] = new_cost

    def add_edge(self, _from, _to, cost):
        """
        Adds an edge between 2 given vertices. If there already exists an edge between those 2 vertices in the graph
        or one of the 2 given vertices is not present in the graph an exception is thrown (GraphException).
        :param _from: The starting vertex of the edge; integer
        :param _to: The ending vertex of the edge; integer
        :param cost: The cost of the vertex; integer
        :return: -
        :preconditions: The edge does not already exist in the graph and both vertices are in the graph.
        """
        if self.is_edge_in_graph(_from, _to) or self.is_edge_in_graph(_to, _from):
            raise GraphException("The edge already exists.")
        if not self.is_vertex_in_graph(_from):
            raise GraphException(f"The vertex {_from} does not exist in the graph.")
        if not self.is_vertex_in_graph(_to):
            raise GraphException(f"The vertex {_to} does not exist in the graph.")
        self.__neighbours[_to].append(_from)
        if _to != _from: self.__neighbours[_from].append(_to)
        self.__cost[(_from, _to)] = cost

    def remove_edge(self, _from, _to):
        """
        Removes the edge between the 2 given vertices in the graph. If an edge does not exist between these 2 vertices
        or one of the 2 given vertices is not present in the graph an exception is thrown (GraphException).
        :param _from: The starting vertex of the edge; integer
        :param _to: The ending vertex of the edge; integer
        :return: -
        :preconditions: The edge exists in the graph
        """
        if not self.is_edge_in_graph(_from, _to):
            raise GraphException("The edge does not exist, so it cannot be removed.")
        if not self.is_vertex_in_graph(_from):
            raise GraphException(f"The vertex {_from} does not exist in the graph.")
        if not self.is_vertex_in_graph(_to):
            raise GraphException(f"The vertex {_to} does not exist in the graph.")
        if _from != _to:
            self.__neighbours[_to].remove(_from)
            self.__neighbours[_from].remove(_to)
            if (_from, _to) in self.__cost.keys(): del self.__cost[(_from, _to)]
            if (_to, _from) in self.__cost.keys(): del self.__cost[(_to, _from)]
        else:
            self.__neighbours[_to].remove(_from)
            del self.__cost[(_from, _to)]

    def add_vertex(self, vertex):
        """
        Adds a vertex in the graph. If the vertex is already present in the graph an exception is thrown.
        :param vertex: The number of the vertex we want to add; integer
        :return: -
        :preconditions: The vertex does not already exist in the graph
        """
        if self.is_vertex_in_graph(vertex):
            raise GraphException("The vertex already exists.")
        self.__neighbours[vertex] = []

    def remove_vertex(self, vertex):
        """
        Removes a vertex from the graph. If the given vertex is not present in the graph an exception is thrown.
        :param vertex: The number of the vertex we want to remove; integer
        :return: -
        :preconditions: The vertex exists in the graph
        """
        if not self.is_vertex_in_graph(vertex):
            raise GraphException("The vertex does not exist, so it cannot be removed.")
        # First delete the list related to <vertex> in <dict_in> and delete all appearances of <vertex> from <dict_in>
        del self.__neighbours[vertex]
        for v in self.get_all_vertices():
            if vertex in self.__neighbours[v]:
                self.__neighbours[v] = [node for node in self.__neighbours[v] if node != vertex]
        # Now delete every edge which has the vertex <vertex> in it from <dict_cost>
        self.__cost = {key: value for (key, value) in self.__cost.items() if key[0] != vertex and key[1] != vertex}

    def get_copy_of_graph(self):
        """
        Returns a copy of the graph.
        """
        return deepcopy(self)

    def get_graph_drawing(self):
        """
        Creates a Graphviz graph drawing and returns it. In order to see this drawing, the user must render the
        output of this function with the parameter <view> set to True.
        :return: The drawing of the graph; Graphviz drawing
        """
        graph_drawing = graphviz.Digraph(comment="Directed Graph", format="png")
        for vertex in self.get_all_vertices():
            graph_drawing.node(str(vertex))
        for _from, _to, _cost in self.get_all_edges():
            graph_drawing.edge(str(_from), str(_to), label=str(_cost))
        return graph_drawing

############################################################################
# ##### THE BELOW CODE WAS IMPLEMENTED FOR ASSIGNMENT 4 - COMPULSORY ##### #
############################################################################

    def prim_algorithm(self, start):
        """
        Find the minimum spanning tree (MST) of the graph starting from the given vertex <start> using
        Prim's Algorithm.
        :param start: The vertex where we want Prim's Algorithm to start from; integer
        :return: The edges from the minimum spanning tree; list of pairs representing the edges: (_from, _to)
        """
        if not self.is_vertex_in_graph(start):
            raise GraphException(f"The vertex {start} does not exist in the graph.")
        q = PriorityQueue()
        prev = {node: None for node in self.get_all_vertices()}
        dist = {node: numpy.inf for node in self.get_all_vertices()}
        processed = {node: False for node in self.get_all_vertices()}
        tree_edges = []

        dist[start] = 0
        processed[start] = True

        for neighbour in self.get_neighbours(start):
            dist[neighbour] = self.get_cost_of_edge(start, neighbour)
            prev[neighbour] = start
            q.put((dist[neighbour], neighbour))
        while not q.empty():
            top = q.get()
            top_vertex = top[1]
            if not processed[top_vertex]:
                tree_edges.append((prev[top_vertex], top_vertex))
                processed[top_vertex] = True
                for neighbour in self.get_neighbours(top_vertex):
                    if not processed[neighbour] and self.get_cost_of_edge(top_vertex, neighbour) < dist[neighbour]:
                        dist[neighbour] = self.get_cost_of_edge(top_vertex, neighbour)
                        q.put((dist[neighbour], neighbour))
                        prev[neighbour] = top_vertex
        return tree_edges


def read_graph(file_name):
    """
    Reads a graph from a given file, builds this graph and returns it.
    :param file_name: The name of the file where the graph is stored (should be given with extension i.e., 'txt')
    :return: An instance of UndirectedGraph; the randomly generated graph
    """
    with open(file_name, 'r') as f:
        lines = f.readlines()
    first_line = lines[0].strip().split()
    no_vertices = int(first_line[0])
    new_graph = UndirectedGraph(no_vertices)
    for line in lines[1:]:
        if line == "":
            continue
        line = line.strip().split()
        _from, _to, _cost = int(line[0]), int(line[1]), int(line[2])
        new_graph.add_edge(_from, _to, _cost)
    return new_graph


def write_graph(graph, file_name):
    """
    Writes the given graph in a file.
    :param graph: The graph we want to save; an instance of UndirectedGraph
    :param file_name: The name of the file where we want to save the graph (should be given with extension i.e., 'txt')
    :return: -
    """
    all_vertices = graph.get_all_vertices()
    written_edges = []
    with open(file_name, 'w') as f:
        first_line = str(graph.get_no_vertices()) + ' ' + str(graph.get_no_edges()) + '\n'
        f.write(first_line)
        for vertex in all_vertices:
            if graph.get_degree(vertex) == 0:
                line = str(vertex) + '\n'
                f.write(line)
            else:
                for neighbour in graph.get_neighbours(vertex):
                    if (vertex, neighbour) not in written_edges and (neighbour, vertex) not in written_edges:
                        cost = graph.get_cost_of_edge(vertex, neighbour)
                        written_edges.append((vertex, neighbour))
                        line = str(vertex) + ' ' + str(neighbour) + ' ' + str(cost) + '\n'
                        f.write(line)


def create_random_graph(no_vertices, no_edges):
    """
    Creates a random graph with <no_vertices> vertices and <no_edges> edges.
    :param no_vertices: The number of vertices the graph should have; integer
    :param no_edges: The number of edges the graph should have; integer
    :return: An instance of UndirectedGraph; the randomly generated graph
    """
    if no_vertices < 0 or no_edges < 0:
        raise GraphException("Error! The number of edges and number of vertices must be non-negative.")
    if no_edges > no_vertices * (no_vertices - 1):
        raise GraphException("Error! Too many edges given.")
    random_graph = UndirectedGraph(no_vertices)
    while no_edges:
        _from = random.randrange(0, no_vertices)
        _to = random.randrange(0, no_vertices)
        cost = random.randrange(0, MAX_GRAPH_COST + 1)  # The costs will be in [0, MAX_COST]
        if not random_graph.is_edge_in_graph(_from, _to):
            random_graph.add_edge(_from, _to, cost)
            no_edges = no_edges - 1
    return random_graph
