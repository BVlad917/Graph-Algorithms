import random
import numpy
from copy import deepcopy

import graphviz

from errors import GraphException


class DirectedGraph:
    def __init__(self):
        """
        Creates a graph represented by 3 dictionaries with <no_vertices> vertices (optional argument).
        """
        self.__dict_in = {}
        self.__dict_out = {}
        self.__duration = {}  # Added for the bonus; the duration of each vertex

    def get_all_durations(self):
        """
        Returns all the activity durations from the graph (along with the corresponding activity vertex)
        :return: (vertex, duration) pairs in a dictionary representing the activity durations of the vertices
        in the graph
        """
        for vertex, duration in self.__duration.items():
            yield vertex, duration

    def change_activity_duration(self, vertex, new_duration):
        """
        Changes the duration of the activity represented by the vertex <vertex>
        :param vertex: The activity vertex whose duration we want to change; integer
        :param new_duration: The new duration of the activity; integer
        :exception: GraphException - if the given vertex is not in the graph
        """
        if not self.is_vertex_in_graph(vertex):
            raise GraphException(f"ERROR: The vertex {vertex} is not in the graph.")
        if new_duration < 0:
            raise GraphException("Invalid activity duration given: it must be a positive integer")
        self.__duration[vertex] = new_duration

    def get_no_vertices(self):
        """
        Returns the number of vertices in the graph.
        """
        return len(self.__dict_in.keys())

    def get_no_edges(self):
        """
        Returns the number of edges in the graph.
        """
        no_edges = 0
        for key in self.__dict_out.keys():
            no_edges += len(self.__dict_out[key])
        return no_edges

    def get_all_vertices(self):
        """
        Returns all the vertices from the graph using an iterator.
        """
        for vertex in self.__dict_out.keys():
            yield vertex

    def get_all_edges(self):
        """
        Using a generator, returns all the edges in the graph as triples in the following format (_from, _to):
        <_from> - starting vertex,
        <_to> - ending index
        """
        for key in self.__dict_out.keys():
            for neighbour in self.__dict_out[key]:
                yield key, neighbour

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
        return _to in self.__dict_out[_from]

    def is_vertex_in_graph(self, vertex):
        """
        Checks if the given vertex exists in the graph or not
        :param vertex: The vertex we want to check; integer
        :return: True if the vertex is in the graph; False otherwise
        """
        return vertex in self.__dict_out.keys()

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

    def add_edge(self, _from, _to):
        """
        Adds an edge between 2 given vertices. If there already exists an edge between those 2 vertices in the graph
        or one of the 2 given vertices is not present in the graph an exception is thrown (GraphException).
        :param _from: The starting vertex of the edge; integer
        :param _to: The ending vertex of the edge; integer
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

    def add_vertex(self, vertex, duration=0):
        """
        Adds a vertex in the graph. If the vertex is already present in the graph an exception is thrown.
        :param vertex: The number of the vertex we want to add; integer
        :param duration: The duration of the new vertex; integer
        :return: -
        :preconditions: The vertex does not already exist in the graph
        """
        if self.is_vertex_in_graph(vertex):
            raise GraphException("The vertex already exists.")
        if duration < 0:
            raise GraphException("Invalid activity duration given: it must be a positive integer")
        self.__dict_in[vertex] = []
        self.__dict_out[vertex] = []
        self.__duration[vertex] = duration

    def remove_vertex(self, vertex):
        """
        Removes a vertex from the graph. If the given vertex is not present in the graph an exception is thrown.
        :param vertex: The number of the vertex we want to remove; integer
        :return: -
        :preconditions: The vertex exists in the graph
        """
        if not self.is_vertex_in_graph(vertex):
            raise GraphException("The vertex does not exist, so it cannot be removed.")
        # First delete the 2 lists related to <vertex> in <dict_in>
        del self.__dict_in[vertex]
        del self.__dict_out[vertex]
        # Delete this vertex's appearance from the duration dictionary
        del self.__duration[vertex]

        # Now delete all appearances of <vertex> from <dict_in> and <dict_out>
        for v in self.get_all_vertices():
            if vertex in self.__dict_in[v]:
                self.__dict_in[v] = [node for node in self.__dict_in[v] if node != vertex]
        for v in self.get_all_vertices():
            if vertex in self.__dict_out[v]:
                self.__dict_out[v] = [node for node in self.__dict_out[v] if node != vertex]

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

    ####################################################################################
    # ##### THE BELOW CODE WAS IMPLEMENTED FOR THE BONUS OF ASSIGNMENT 4 - BONUS ##### #
    ####################################################################################

    def get_duration(self, vertex):
        """
        Return the activity duration of the given vertex
        :param vertex: A vertex in the graph; int
        :return: The duration of the vertex <vertex>; int
        :exception: GraphException - if the given vertex is not in the graph
        """
        if not self.is_vertex_in_graph(vertex):
            raise GraphException(f"ERROR: Vertex {vertex} is not in the graph.")
        return self.__duration[vertex]

    def topological_sort_dfs_util(self, start, lst, full, current):
        """
        Utility function which sorts the vertices of the graph (starting from the vertex <start>) in
        topological order using depth first search.
        :param start: The starting vertex; integer
        :param lst: The list that will contain the sorted vertices; list of integers
        :param full: A list which will hold all the vertices which were already visited and sorted
        :param current: The current path we are traversing; this is used to detect cycles
        :return: True if no problems were found; False if a cycle was detected
        """
        current.add(start)
        for inbound_neighbour in self.get_inbound_neighbours(start):
            if inbound_neighbour in full:
                continue
            if inbound_neighbour in current:
                return False
            ok = self.topological_sort_dfs_util(inbound_neighbour, lst, full, current)
            if not ok:
                return False
        current.remove(start)
        full.add(start)
        lst.append(start)
        return True

    def topological_sort(self):
        """
        Sort the vertices from the graph topologically. Uses the utility function <topological_sort_dfs_util> to
        achieve this.
        :return: The graph vertices sorted in topological order (list of integers) OR None if the graph is not
        a Directed Acyclic Graph so it cannot be sorted topologically.
        """
        lst = []
        full = set()
        current = set()
        for vertex in self.get_all_vertices():
            if vertex not in full:
                ok = self.topological_sort_dfs_util(vertex, lst, full, current)
                if not ok:
                    return None
        return lst

    def schedule_activities(self):
        """
        Treats the vertices in the graph as activities and sorts them using earliest scheduling and latest scheduling.
        :return: 4 dictionaries representing (in this order): the start of the earliest scheduling of each
        activity, the end of the earliest scheduling of each activity, the start of the latest scheduling of each
        activity, and finally, the end of the latest scheduling of each activity
        :exception: GraphException - if the graph is not DAG so it cannot be sorted topologically
        """
        # The following 2 lists will hold the starting and ending times of the earliest scheduling
        earliest_start = {node: 0 for node in self.get_all_vertices()}
        earliest_end = {node: 0 for node in self.get_all_vertices()}
        # The following 2 lists will hold the starting and ending times of the latest scheduling
        latest_start = {node: numpy.inf for node in self.get_all_vertices()}
        latest_end = {node: numpy.inf for node in self.get_all_vertices()}
        topological_sorted_vertices = self.topological_sort()
        if topological_sorted_vertices is None:
            raise GraphException("ERROR: The graph is not a DAG. We cannot schedule the activities.")

        for vertex in topological_sorted_vertices:
            for inbound_neighbour in self.get_inbound_neighbours(vertex):
                earliest_start[vertex] = max(earliest_start[vertex], earliest_end[inbound_neighbour])
            earliest_end[vertex] = earliest_start[vertex] + self.__duration[vertex]

        last_activity = topological_sorted_vertices[self.get_no_vertices() - 1]
        latest_end[last_activity] = earliest_end[last_activity]
        latest_start[last_activity] = latest_end[last_activity] - self.__duration[last_activity]
        for vertex in reversed(topological_sorted_vertices):
            for outbound_neighbour in self.get_outbound_neighbours(vertex):
                latest_end[vertex] = min(latest_end[vertex], latest_start[outbound_neighbour])
            latest_start[vertex] = latest_end[vertex] - self.__duration[vertex]
        # Return the 4 lists
        return earliest_start, earliest_end, latest_start, latest_end

    def count_no_paths_dfs_util(self, visited, paths, end):
        """
        Utility function used to find the paths between a list of vertices as the start of the path (<visited>) and
        a given vertex <end> using depth first search.
        :param visited: The partial path built so far; list of integers
        :param paths: All of the paths built so far; list of lists of integers
        :param end: The ending vertex; integer
        :return: -
        """
        if not self.is_vertex_in_graph(end):
            raise GraphException(f"ERROR: The vertex {end} is not in the graph")
        for outbound_neighbour in self.get_outbound_neighbours(visited[-1]):
            if outbound_neighbour in visited:
                continue
            if outbound_neighbour == end:
                visited.append(outbound_neighbour)
                paths.append(visited)
                del visited[-1]
                break
        for outbound_neighbour in self.get_outbound_neighbours(visited[-1]):
            if outbound_neighbour in visited or outbound_neighbour == end:
                continue
            visited.append(outbound_neighbour)
            self.count_no_paths_dfs_util(visited, paths, end)
            del visited[-1]

    def get_no_paths_between_2_vertices(self, start, end):
        """
        Find the number of distinct paths between the vertex <start> and the vertex <end>. Uses the function
        <count_no_paths_dfs_util> as a utility function.
        :param start: The starting vertex of the paths; integer
        :param end: The ending vertex of the paths; integer
        :return: The number of distinct paths between vertex <start> and vertex <end>; integer
        """
        if not self.is_vertex_in_graph(start):
            raise GraphException(f"ERROR: The vertex {start} is not in the graph")
        if not self.is_vertex_in_graph(end):
            raise GraphException(f"ERROR: The vertex {end} is not in the graph")
        if self.topological_sort() is None:
            raise GraphException("ERROR: The graph is not a Directed Acyclic Graph")
        visited = []
        paths = []
        visited.append(start)
        self.count_no_paths_dfs_util(visited, paths, end)
        return len(paths)


def read_graph(file_name):
    """
    Reads a graph from a given file, builds this graph and returns it.
    :param file_name: The name of the file where the graph is stored (should be given with extension i.e., 'txt')
    :return: An instance of DirectedGraph; the randomly generated graph
    """
    with open(file_name, 'r') as f:
        lines = f.readlines()
    first_line = lines[0].strip().split()
    no_vertices = int(first_line[0])
    new_graph = DirectedGraph()
    second_line = lines[1].strip().split()
    if len(second_line) != no_vertices:
        raise GraphException(f"ERROR while reading the file: {no_vertices} vertices given but {len(second_line)}"
                             f"durations given.")
    for vertex, duration in enumerate(second_line):
        new_graph.add_vertex(vertex, int(duration))
    for line in lines[2:]:
        if line == "":
            continue
        line = line.strip().split()
        _from, _to = int(line[0]), int(line[1])
        new_graph.add_edge(_from, _to)
    return new_graph


def write_graph(graph, file_name):
    """
    Writes the given graph in a file.
    :param graph: The graph we want to save; an instance of DirectedGraph
    :param file_name: The name of the file where we want to save the graph (should be given with extension i.e., 'txt')
    :return: -
    """
    all_vertices = graph.get_all_vertices()
    with open(file_name, 'w') as f:
        first_line = str(graph.get_no_vertices()) + ' ' + str(graph.get_no_edges()) + '\n'
        f.write(first_line)
        second_line = ""
        for vertex in graph.get_all_vertices():
            second_line += str(graph.get_duration(vertex)) + ' '
        second_line += "\n"
        f.write(second_line)
        for vertex in all_vertices:
            if graph.get_out_degree(vertex) == 0:
                line = str(vertex) + '\n'
                f.write(line)
            else:
                for neighbour in graph.get_outbound_neighbours(vertex):
                    line = str(vertex) + ' ' + str(neighbour) + '\n'
                    f.write(line)


def create_random_graph(no_vertices, no_edges):
    """
    Creates a random graph with <no_vertices> vertices and <no_edges> edges.
    :param no_vertices: The number of vertices the graph should have; integer
    :param no_edges: The number of edges the graph should have; integer
    :return: An instance of DirectedGraph; the randomly generated graph
    """
    if no_vertices < 0 or no_edges < 0:
        raise GraphException("Error! The number of edges and number of vertices must be non-negative.")
    if no_edges > no_vertices * (no_vertices - 1):
        raise GraphException("Error! Too many edges given.")
    random_graph = DirectedGraph()
    vertex = 0
    while vertex < no_vertices:
        duration = random.randrange(1, 11)  # The random duration will be in the range [1, 10]
        random_graph.add_vertex(vertex, duration)
        vertex += 1
    while no_edges:
        _from = random.randrange(0, no_vertices)
        _to = random.randrange(0, no_vertices)
        if not random_graph.is_edge_in_graph(_from, _to):
            random_graph.add_edge(_from, _to)
            no_edges = no_edges - 1
    return random_graph
