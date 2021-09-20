import random
from copy import deepcopy

from errors import GraphException


class UndirectedGraph:
    def __init__(self, no_vertices=0):
        """
        Creates a graph represented by 3 dictionaries with <no_vertices> vertices (optional argument).
        """
        self.__neighbours = {}
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
        edges = []
        for key, value in self.__neighbours.items():
            edges += [(key, neighbour) for neighbour in value if key <= neighbour]
        return len(edges)

    def get_all_vertices(self):
        """
        Returns all the vertices from the graph using an iterator.
        """
        for vertex in self.__neighbours.keys():
            yield vertex

    def get_all_edges(self):
        """
        Using a generator, returns all the edges in the graph as triples in the following format (_from, _to, cost):
        <_from> - starting vertex
        <_to> - ending index
        Note: This order doesn't matter in this case, since this is an undirected graph. The edges will be returned
        such that the first element of the tuple will be smaller than (or equal) to the second
        """
        edges = []
        for key, value in self.__neighbours.items():
            edges += [(key, neighbour) for neighbour in value if key <= neighbour]
        for edge in edges:
            yield edge

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

    def add_edge(self, _from, _to):
        """
        Adds an edge between 2 given vertices. If there already exists an edge between those 2 vertices in the graph
        or one of the 2 given vertices is not present in the graph an exception is thrown (GraphException).
        :param _from: The starting vertex of the edge; integer
        :param _to: The ending vertex of the edge; integer
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
        # If we don't have to add an edge like (2, 2), then we also need to add a neighbour to the second
        # element of the tuple
        if _to != _from:
            self.__neighbours[_from].append(_to)

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
        self.__neighbours[_to].remove(_from)
        if _from != _to:
            self.__neighbours[_from].remove(_to)

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
                self.__neighbours[v].remove(vertex)
                # self.__neighbours[v] = [node for node in self.__neighbours[v] if node != vertex]

    def get_copy_of_graph(self):
        """
        Returns a copy of the graph.
        """
        return deepcopy(self)

    ##########################################################################################
    # ############ THE BELOW CODE WAS IMPLEMENTED FOR ASSIGNMENT 5 - COMPULSORY ############ #
    # HAMILTONIAN CYCLE = CYCLE IN WHICH EVERY VERTEX FROM THE GRAPH IS VISITED EXACTLY ONCE #
    ##########################################################################################

    def __hamiltonian_cycle_is_new_vertex_safe(self, new_vertex, new_vertex_position, path):
        """
        Checks if the vertex we want to add next is a valid vertex for the Hamiltonian cycle we are building.
        A new vertex is valid in the path of the Hamiltonian cycle if there is an edge between this new vertex
        and the last vertex in the path AND if this new vertex is not already anywhere in the path.
        :param new_vertex: The new vertex we want to add to the path; integer
        :param new_vertex_position: The position where the new vertex WILL be added (so it's not added yet); integer
        :param path: The current path we built so far; list of integers
        :return: True if the new vertex we want to add is valid; False otherwise
        """
        # If there is no edge between the vertex we want to add and the last vertex in the path, then return False
        if not self.is_edge_in_graph(path[new_vertex_position - 1], new_vertex):
            return False
        # Loop over all the vertices that have been put in the path (are different from -1) and
        # if the vertex we want to add is already in the path, then return False. Otherwise return True
        for vertex in path:
            if vertex == -1:
                break
            if vertex == new_vertex:
                return False
        return True

    def __find_hamiltonian_cycle_util(self, path, position):
        """
        Recursive function used for searching the solution space (backtracking). It will try to fill the new
        positions in the path with valid vertices (valid vertex = vertex which is not already in the path and
        which has an edge with the last vertex in the path). If we get to the case where we filled the last position,
        we check to see if there is an edge between the last and first vertices in the path (cycle). If there is,
        then we found our Hamiltonian cycle.
        :param path: The path built so far; list of integers
        :param position: The position in the path which we currently want to fill; integer
        :return: True if the current position <position> was filled; False if no valid vertex was found for the
        current position
        """
        # If we filled all the positions in the path (i.e., we visited all the vertices), check if we can close
        # the cycle (i.e., there's an edge between the first and last vertices)
        if position == self.get_no_vertices():
            if self.is_edge_in_graph(path[position - 1], path[0]):
                return True
            else:
                return False
        # Loop over the vertices in the graph, but skip the first one since we already placed the first vertex in
        # the path (we did this in the main function, not here)
        all_vertices = self.get_all_vertices()
        next(all_vertices)
        for vertex in all_vertices:
            # Check if the current vertex can be safely added to the empty position in the path
            # If it is, then add it and try to fill the next position as well
            # After returning from the recursive calls, re-mark the filled position as empty to try different vertices
            if self.__hamiltonian_cycle_is_new_vertex_safe(vertex, position, path):
                path[position] = vertex
                if self.__find_hamiltonian_cycle_util(path, position + 1):
                    return True
                path[position] = -1
        return False

    def find_hamiltonian_cycle(self):
        """
        Find a Hamiltonian cycle in the graph, if one exists. This function is meant to pick the first vertex
        in the path and kickstart the whole algorithm by making the first call to the recursive function
        <__find_hamiltonian_cycle_util>.
        :return: The hamiltonian cycle in a list if it exists; Otherwise returns None
        """
        path = [-1] * self.get_no_vertices()
        # We need to pick the starting vertex; We take the first vertex returned in the generator <get_all_vertices()>
        first_vertex = -1
        for vertex in self.get_all_vertices():
            if first_vertex == -1:
                first_vertex = vertex
                break
        # The path will start from the chosen first vertex
        path[0] = first_vertex
        # Start the search for a Hamiltonian cycle from position 1, since we already have a vertex on position 0
        if not self.__find_hamiltonian_cycle_util(path, 1):
            return None
        # Append to the path the first vertex, since we have a cycle
        return path + [path[0]]


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
        _from, _to = int(line[0]), int(line[1])
        new_graph.add_edge(_from, _to)
    return new_graph


def write_graph(graph, file_name):
    """
    Writes the given graph in a file.
    :param graph: The graph we want to save; an instance of UndirectedGraph
    :param file_name: The name of the file where we want to save the graph (should be given with extension i.e., 'txt')
    :return: -
    """
    all_vertices = graph.get_all_vertices()
    # written_edges = []
    with open(file_name, 'w') as f:
        first_line = str(graph.get_no_vertices()) + ' ' + str(graph.get_no_edges()) + '\n'
        f.write(first_line)
        for vertex in all_vertices:
            if graph.get_degree(vertex) == 0:
                line = str(vertex) + '\n'
                f.write(line)
            else:
                for neighbour in graph.get_neighbours(vertex):
                    if vertex <= neighbour:
                        line = str(vertex) + ' ' + str(neighbour) + '\n'
                        f.write(line)
                    # if (vertex, neighbour) not in written_edges and (neighbour, vertex) not in written_edges:
                    #     written_edges.append((vertex, neighbour))
                    #     line = str(vertex) + ' ' + str(neighbour) + '\n'
                    #     f.write(line)


def create_random_graph(no_vertices, no_edges):
    """
    Creates a random graph with <no_vertices> vertices and <no_edges> edges.
    :param no_vertices: The number of vertices the graph should have; integer
    :param no_edges: The number of edges the graph should have; integer
    :return: An instance of UndirectedGraph; the randomly generated graph
    """
    if no_vertices < 0 or no_edges < 0:
        raise GraphException("Error! The number of edges and number of vertices must be non-negative.")
    if no_edges > (no_vertices * (no_vertices - 1)) / 2:
        raise GraphException("Error! Too many edges given.")
    random_graph = UndirectedGraph(no_vertices)
    while no_edges:
        _from = random.randrange(0, no_vertices)
        _to = random.randrange(0, no_vertices)
        # Since we have an undirected graph, we won't add edges like (2, 2) in the <create_random_graph>
        # function since those type of edges are not interesting
        if not random_graph.is_edge_in_graph(_from, _to) and _from != _to:
            random_graph.add_edge(_from, _to)
            no_edges = no_edges - 1
    return random_graph
