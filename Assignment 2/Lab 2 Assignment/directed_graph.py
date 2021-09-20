import random
from copy import deepcopy

from errors import GraphException

MAX_GRAPH_COST = 100  # We use this for the costs of the randomly generated graphs
INFINITY = 999999999999999  # We use this to define the default value used as infinity


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

    def bfs(self, start_vertex, end_vertex):
        """
        Performs a modified Breadth First Search from the given starting vertex. Once the search reaches the
        vertex <end_vertex> (that is, if it reaches it), the algorithm stops.
        :param start_vertex: Integer; the vertex where the Breadth First Search starts from
        :param end_vertex: Integer; if the algorithm reaches this vertex, then the function stops
        :returns: dictionary visited - the keys are all the vertices from the graph, the values are truth
        values denoting whether or not that vertex is accessible from the starting vertex
        :returns: dictionary prev - the keys are all the vertices from the graph, the value of each key is the
        previous vertex on the path from the starting vertex to the key vertex
        :returns: dictionary dist - the keys are all the vertices from the graph, the values are the lengths
        of the paths from the starting vertex to that vertex or INFINITY if that vertex is not accessible
        from the starting vertex
        :except: GraphException - if the given <start_vertex> is not in the graph
        """
        if not self.is_vertex_in_graph(start_vertex):
            raise GraphException(f"Error! The vertex {start_vertex} is not in the graph.")
        # Initialize the visited dictionary with False values, the distance dictionary with infinity values
        # and the previous dictionary with None values
        visited = {node: False for node in self.get_all_vertices()}
        dist = {node: INFINITY for node in self.get_all_vertices()}
        prev = {node: None for node in self.get_all_vertices()}
        # We will treat the following list as a queue
        queue = [start_vertex]
        visited[start_vertex] = True
        dist[start_vertex] = 0
        while len(queue):
            # Get the vertex from the top of the queue and pop it from the queue
            top_of_queue = queue[0]
            queue = queue[1:]
            for neighbour in self.get_outbound_neighbours(top_of_queue):
                if not visited[neighbour]:
                    queue.append(neighbour)
                    visited[neighbour] = True
                    dist[neighbour] = dist[top_of_queue] + 1
                    prev[neighbour] = top_of_queue
                    if neighbour == end_vertex:
                        return visited, prev, dist
        return visited, prev, dist

    def lowest_length_path(self, start_vertex, end_vertex):
        """
        Finds the lowest length path between <start_vertex> and <end_vertex> using a forward breadth first
        search starting from <start_vertex>. Note: we are using a modified version of the BFS, stopping it
        once we get to <end_vertex>.
        :param start_vertex: Integer; The vertex where the path (and the BFS) starts
        :param end_vertex: Integer; The vertex where the path ends
        :return: A list containing the lowest length path, the first element in the list will be <start_vertex>, while
        the last element in the list will be <end_vertex>
        :except: GraphException - if one of the given vertices are not in the graph, OR if <end_vertex> is not
        accessible from <start_vertex>
        """
        if not self.is_vertex_in_graph(start_vertex):
            raise GraphException(f"Error! The starting vertex {start_vertex} is not in the graph.")
        if not self.is_vertex_in_graph(end_vertex):
            raise GraphException(f"Error! The ending vertex {end_vertex} is not in the graph.")
        visited, prev, dist = self.bfs(start_vertex, end_vertex)
        if not visited[end_vertex]:
            raise GraphException(f"Error! The node {end_vertex} is not accessible from node {start_vertex}.")
        path = []
        node = end_vertex
        while prev[node] is not None:
            path.append(node)
            node = prev[node]
        path.append(node)
        return path[::-1]

    def kosaraju(self):
        """
        Finds all of the strongly connected components of the graph using the Kosaraju algorithm.
        :return: List of lists where each lists contains all the vertices from a strongly connected component
        """
        nr_vertices = self.get_no_vertices()
        T, L, U = [[] for _ in range(nr_vertices)], [], [False] * nr_vertices
        for u in range(nr_vertices):
            if not U[u]:
                U[u], S = True, [u]
                while S:
                    u, done = S[-1], True
                    for v in self.__dict_out[u]:
                        T[v].append(u)
                        if not U[v]:
                            U[v], done = True, False
                            S.append(v)
                            break
                    if done:
                        S.pop()
                        L.append(u)
        scc = [None] * nr_vertices
        while L:
            r = L.pop()
            S = [r]
            if U[r]:
                U[r], scc[r] = False, r
            while S:
                u, done = S[-1], True
                for v in T[u]:
                    if U[v]:
                        U[v] = done = False
                        S.append(v)
                        scc[v] = r
                        break
                if done:
                    S.pop()
        d = {}
        for vertex in sorted(set(scc)):
            d[vertex] = []
        for index, vertex in enumerate(scc):
            d[vertex].append(index)
        comps = [value for value in d.values()]
        return comps

    def __dfs1(self, vertex, visited, stack):
        """
        Traverses all the vertices from the graph using the Depth First Search algorithm and pushes all the
        vertices on a stack such that the last vertex visited will be the first one pushed on the stack (so the
        first vertex visited will be at the top of the stack after the algorithm finishes). This function is meant
        to be used as the first DFS in The Kosaraju Algorithm.
        :param vertex: The current vertex that is being traversed; Integer
        :param visited: Keeps track of whether or not a vertex was already visited; List of bool values
        :param stack: The stack where we will push the visited vertices; List
        :except GraphException: If the given vertex <vertex> is not in the graph (This can only happen in the
        first call of the function, when the function is called by the user)
        """
        if not self.is_vertex_in_graph(vertex):
            raise GraphException(f"ERROR: The vertex {vertex} is not in the graph.")
        visited[vertex] = True
        for neighbour in self.__dict_out[vertex]:
            if not visited[neighbour]:
                self.__dfs1(neighbour, visited, stack)
        stack.append(vertex)

    def __dfs2(self, vertex, visited, strongly_connected_comps):
        """
        Traverses all the vertices from the graph using the Depth First Search algorithm and appends the currently
        visited vertex in the last list from the <strongly_connected_comps> list. This function is meant to be
        used as the second DFS in The Kosaraju Algorithm.
        :param vertex: The current vertex that is being traversed; Integer
        :param visited: Keeps track of whether or not a vertex was already visited; List of bool values
        :param strongly_connected_comps: List of lists where the strongly connected components will be stored
        :except GraphException: If the given vertex <vertex> is not in the graph (This can only happen in the
        first call of the function, when the function is called by the user)
        """
        if not self.is_vertex_in_graph(vertex):
            raise GraphException(f"ERROR: The vertex {vertex} is not in the graph.")
        visited[vertex] = True
        strongly_connected_comps[-1].append(vertex)
        for neighbour in self.__dict_out[vertex]:
            if not visited[neighbour]:
                self.__dfs2(neighbour, visited, strongly_connected_comps)

    def transposed_graph(self):
        """
        Transposes the graph (i.e., reverses the orientation of all the edges). This does NOT happen in-place.
        :return: A new graph (instance of the TripleDictGraph class) where each edge was obtained by reversing
        some edge from this graph.
        """
        new_graph = TripleDictGraph()
        for vertex in self.get_all_vertices():
            new_graph.add_vertex(vertex)
        for _from, _to, _cost in self.get_all_edges():
            new_graph.add_edge(_to, _from, _cost)
        return new_graph

    def find_all_scc(self):
        """
        Finds all of the strongly connected components of the graph using the Kosaraju algorithm.
        :return: List of lists where each lists contains all the vertices from a strongly connected component
        """
        stack = []
        visited = [False] * self.get_no_vertices()
        for vertex in self.get_all_vertices():
            if not visited[vertex]:
                self.__dfs1(vertex, visited, stack)
        transposed_graph = self.transposed_graph()
        visited = [False] * self.get_no_vertices()
        strongly_connected_comps = []
        while stack:
            top = stack.pop()
            if not visited[top]:
                strongly_connected_comps.append([])
                transposed_graph.__dfs2(top, visited, strongly_connected_comps)
        return strongly_connected_comps

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
    new_graph = TripleDictGraph(no_vertices)
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
