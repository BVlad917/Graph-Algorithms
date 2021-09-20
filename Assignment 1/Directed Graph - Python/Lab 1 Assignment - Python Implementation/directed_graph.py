import random
from copy import deepcopy

from errors import GraphException

MAX_GRAPH_COST = 100  # We use this for the costs of the randomly generated graphs


class TripleDictGraph:
    def __init__(self, no_vertices=0):
        """
        Creates a graph represented by 3 dictionaries with <no_vertices> vertices (optional argument).
        """
        self.__dict_in = {}
        self.__dict_out = {}
        self.__cost = {}
        for i in range(no_vertices):
            self.__dict_in[i] = []
            self.__dict_out[i] = []

    def get_no_vertices(self):
        """
        Returns the number of vertices in the graph.
        """
        return len(self.__dict_in.keys())

    def get_no_edges(self):
        """
        Returns the number of edges in the graph.
        """
        return len(self.__cost.keys())

    def get_all_vertices(self):
        """
        Returns all the vertices from the graph using an iterator.
        """
        for vertex in self.__dict_in.keys():
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
        if (_from, _to) not in self.__cost:
            raise GraphException("The given edge does not exist.")
        return self.__cost[(_from, _to)]

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
        return _from in self.__dict_in[_to]

    def is_vertex_in_graph(self, vertex):
        """
        Checks if the given vertex exists in the graph or not
        :param vertex: The vertex we want to check; integer
        :return: True if the vertex is in the graph; False otherwise
        """
        return vertex in self.__dict_in.keys()

    def get_in_degree(self, vertex):
        """
        Returns the in degree of a given vertex. If the given vertex does not exist in the graph an exception is
        thrown (GraphException).
        :param vertex: The vertex whose in-degree we want; integer
        :return: The in-degree of <vertex>
        :preconditions: The vertex exists in the graph
        """
        if not self.is_vertex_in_graph(vertex):
            raise GraphException(f"The vertex {vertex} does not exist in the graph.")
        return len(self.__dict_in[vertex])

    def get_out_degree(self, vertex):
        """
        Returns the out degree of a given vertex. If the given vertex does not exist in the graph an exception is
        thrown (GraphException).
        :param vertex: The vertex whose out-degree we want; integer
        :return: The out-degree of <vertex>
        :preconditions: The vertex exists in the graph
        """
        if not self.is_vertex_in_graph(vertex):
            raise GraphException(f"The vertex {vertex} does not exist in the graph")
        return len(self.__dict_out[vertex])

    def get_outbound_neighbours(self, vertex):
        """
        Returns the outbound neighbours of a given vertex. If the given vertex does not exist in the graph an
        exception is thrown (GraphException).
        :param vertex: The vertex whose outbound neighbours we want; integer
        :return: A generator with the outbound neighbours of the given vertex
        :preconditions: The vertex exists in the graph
        """
        if not self.is_vertex_in_graph(vertex):
            raise GraphException(f"The vertex {vertex} does not exist in the graph.")
        for out_neighbour in self.__dict_out[vertex]:
            yield out_neighbour

    def get_inbound_neighbours(self, vertex):
        """
        Returns the inbound neighbours of a given vertex. If the given vertex does not exist in the graph an
        exception is thrown (GraphException).
        :param vertex: The vertex whose inbound neighbours we want; integer
        :return: A generator with the inbound neighbours of the given vertex
        :preconditions: The vertex exists in the graph
        """
        if not self.is_vertex_in_graph(vertex):
            raise GraphException(f"The vertex {vertex} does not exist in the graph.")
        for in_neighbour in self.__dict_in[vertex]:
            yield in_neighbour

    def get_outbound_neighbours_with_cost(self, vertex):
        """
        Using a generator, returns all of the outbound neighbours of a vertex, along with the cost of the edge from
        the given vertex to its outbound neighbour.
        :param vertex: The vertex whose outbound neighbours we want; integer
        :return: A generator with (neighbour, cost) type pairs
        """
        if not self.is_vertex_in_graph(vertex):
            raise GraphException(f"The vertex {vertex} does not exist in the graph.")
        for neighbour in self.__dict_out[vertex]:
            yield neighbour, self.get_cost_of_edge(vertex, neighbour)

    def get_inbound_neighbours_with_cost(self, vertex):
        """
        Using a generator, returns all of the inbound neighbours of a vertex, along with the cost of the edge from
        the outbound neighbour to the given vertex.
        :param vertex: The vertex whose inbound neighbours we want; integer
        :return: A generator with (neighbour, cost) type pairs
        """
        if not self.is_vertex_in_graph(vertex):
            raise GraphException(f"The vertex {vertex} does not exist in the graph.")
        for neighbour in self.__dict_in[vertex]:
            yield neighbour, self.get_cost_of_edge(neighbour, vertex)

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
        if self.is_edge_in_graph(_from, _to):
            raise GraphException("The edge already exists.")
        if not self.is_vertex_in_graph(_from):
            raise GraphException(f"The vertex {_from} does not exist in the graph.")
        if not self.is_vertex_in_graph(_to):
            raise GraphException(f"The vertex {_to} does not exist in the graph.")
        self.__dict_in[_to].append(_from)
        self.__dict_out[_from].append(_to)
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
        self.__dict_in[_to].remove(_from)
        self.__dict_out[_from].remove(_to)
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
        self.__dict_in[vertex] = []
        self.__dict_out[vertex] = []

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
        del self.__dict_in[vertex]
        for v in self.get_all_vertices():
            if vertex in self.__dict_in[v]:
                self.__dict_in[v] = [node for node in self.__dict_in[v] if node != vertex]
        # Now do the same thing, but for <dict_out>
        del self.__dict_out[vertex]
        for v in self.get_all_vertices():
            if vertex in self.__dict_out[v]:
                self.__dict_out[v] = [node for node in self.__dict_out[v] if node != vertex]
        # Now delete every edge which has the vertex <vertex> in it from <dict_cost>
        self.__cost = {key: value for (key, value) in self.__cost.items() if key[0] != vertex and key[1] != vertex}
        # All that is left is to decrease the count of vertices

    def get_copy_of_graph(self):
        """
        Returns a copy of the graph.
        """
        return deepcopy(self)


def read_graph(file_name):
    """
    Reads a graph from a given file, builds this graph and returns it.
    :param file_name: The name of the file where the graph is stored (should be given with extension i.e., 'txt')
    :return: An instance of TripleDictGraph; the randomly generated graph
    """
    with open(file_name, 'r') as f:
        lines = f.readlines()
    first_line = lines[0].strip().split()
    no_vertices = int(first_line[0])
    no_edges = int(first_line[1])
    new_graph = TripleDictGraph()
    for line in lines[1:]:
        line = line.strip()
        if line == "":
            continue
        line = line.split()
        if len(line) == 1:
            vertex = int(line[0])
            if not new_graph.is_vertex_in_graph(vertex): new_graph.add_vertex(vertex)
        elif len(line) == 3:
            _from, _to, _cost = int(line[0]), int(line[1]), int(line[2])
            if not new_graph.is_vertex_in_graph(_from): new_graph.add_vertex(_from)
            if not new_graph.is_vertex_in_graph(_to): new_graph.add_vertex(_to)
            new_graph.add_edge(_from, _to, _cost)
    return new_graph


def write_graph(graph, file_name):
    """
    Writes the given graph in a file.
    :param graph: The graph we want to save; an instance of TripleDictGraph
    :param file_name: The name of the file where we want to save the graph (should be given with extension i.e., 'txt')
    :return: -
    """
    all_vertices = graph.get_all_vertices()
    with open(file_name, 'w') as f:
        first_line = str(graph.get_no_vertices()) + ' ' + str(graph.get_no_edges()) + '\n'
        f.write(first_line)
        for vertex in all_vertices:
            if graph.get_out_degree(vertex) == 0:
                line = str(vertex) + '\n'
                f.write(line)
            else:
                for neighbour in graph.get_outbound_neighbours(vertex):
                    cost = graph.get_cost_of_edge(vertex, neighbour)
                    line = str(vertex) + ' ' + str(neighbour) + ' ' + str(cost) + '\n'
                    f.write(line)


def create_random_graph(no_vertices, no_edges):
    """
    Creates a random graph with <no_vertices> vertices and <no_edges> edges.
    :param no_vertices: The number of vertices the graph should have; integer
    :param no_edges: The number of edges the graph should have; integer
    :return: An instance of TripleDictGraph; the randomly generated graph
    """
    if no_vertices < 0 or no_edges < 0:
        raise GraphException("Error! The number of edges and number of vertices must be non-negative.")
    if no_edges > no_vertices * (no_vertices - 1):
        raise GraphException("Error! Too many edges given.")
    random_graph = TripleDictGraph(no_vertices)
    while no_edges:
        _from = random.randrange(0, no_vertices)
        _to = random.randrange(0, no_vertices)
        cost = random.randrange(0, MAX_GRAPH_COST + 1)  # The costs will be in [0, MAX_COST]
        if not random_graph.is_edge_in_graph(_from, _to):
            random_graph.add_edge(_from, _to, cost)
            no_edges = no_edges - 1
    return random_graph
