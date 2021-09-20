from directed_graph import write_graph
from errors import GraphException


class UI:
    def __init__(self, graph):
        self.__graph = graph
        self.__commands = {
            '1': self.__ui_get_number_of_vertices,
            '2': self.__ui_get_number_of_edges,
            '3': self.__ui_get_set_of_vertices,
            '4': self.__ui_get_set_of_edges,
            '5': self.__ui_check_vertex,
            '6': self.__ui_check_edge,
            '7': self.__ui_get_cost_of_edge,
            '8': self.__ui_get_degree,
            '9': self.__ui_get_neighbours,
            '10': self.__ui_change_edge_cost,
            '11': self.__ui_add_edge,
            '12': self.__ui_remove_edge,
            '13': self.__ui_add_vertex,
            '14': self.__ui_remove_vertex,
            '15': self.__ui_save_graph_to_file,
            '16': self.__ui_prim_algorithm,
        }

    @staticmethod
    def __print_menu():
        print("Graph operations:\n"
              "\t1 - Get the number of vertices in the graph\n"
              "\t2 - Get the number of edges in the graph\n"
              "\t3 - Get the set of vertices in the graph\n"
              "\t4 - Get the set of edges in the graph\n"
              "\t5 - Check if a given vertex is in the graph\n"
              "\t6 - Check if there is an edge between 2 vertices\n"
              "\t7 - Get the cost of an edge\n"
              "\t8 - Get the degree of a vertex\n"
              "\t9 - Get the neighbours of a vertex\n"
              "\t10 - Modify the cost of an edge\n"
              "\t11 - Add an edge\n"
              "\t12 - Remove an edge\n"
              "\t13 - Add a vertex\n"
              "\t14 - Remove a vertex\n"
              "\t15 - Write the graph to a file\n"
              "\t*16 - Get a minimum spanning tree (using Prim's Algorithm)\n"
              "\tx - Exit\n"
              "* - Added in Assignment 4")

    def __ui_prim_algorithm(self):
        start_vertex = int(input("Give the starting vertex: "))
        mst_edges = self.__graph.prim_algorithm(start_vertex)
        total_cost = 0
        print("The minimum spanning tree will have the edges: ")
        for start, end in mst_edges:
            print(f"{start} <-> {end}")
            total_cost += self.__graph.get_cost_of_edge(start, end)
        print(f"The total cost of this MST is {total_cost}.")

    def __ui_get_number_of_vertices(self):
        print(f"The number of vertices in the graph is {self.__graph.get_no_vertices()}.")

    def __ui_get_number_of_edges(self):
        print(f"The number of edges in the graph is {self.__graph.get_no_edges()}.")

    def __ui_get_set_of_vertices(self):
        print(f"The set of vertices in the graph is: ", end='')
        print(', '.join(str(vertex) for vertex in self.__graph.get_all_vertices()))

    def __ui_get_set_of_edges(self):
        print(f"The set of edges in the graph is:")
        for _from, _to, _cost in sorted(self.__graph.get_all_edges()):
            print(f"{_from}<->{_to}, cost: {_cost}")

    def __ui_check_vertex(self):
        vertex = int(input("Give the vertex you want to check: "))
        if self.__graph.is_vertex_in_graph(vertex):
            print(f"Yes, the vertex {vertex} is in the graph.")
        else:
            print(f"No, the vertex {vertex} is not in the graph.")

    def __ui_check_edge(self):
        _from = int(input("Give the starting edge: "))
        _to = int(input("Give the ending edge: "))
        if self.__graph.is_edge_in_graph(_from, _to):
            cost = self.__graph.get_cost_of_edge(_from, _to)
            print(f"Yes, there is an edge between {_from} and {_to} (with a cost of {cost})")
        else:
            print(f"No, there is no edge between {_from} and {_to}.")

    def __ui_get_cost_of_edge(self):
        _from = int(input("Give the starting edge: "))
        _to = int(input("Give the ending edge: "))
        print(f"The cost of the edge {_from}<->{_to} is {self.__graph.get_cost_of_edge(_from, _to)}.")

    def __ui_get_degree(self):
        vertex = int(input("Give the vertex: "))
        print(f"The in degree of the vertex {vertex} is {self.__graph.get_degree(vertex)}.")

    def __ui_get_neighbours(self):
        vertex = int(input("Give the vertex: "))
        if self.__graph.get_degree(vertex) == 0:
            print(f"The vertex {vertex} has no neighbours.")
            return
        print(f"The neighbours of vertex {vertex} are:")
        for neighbour in sorted(self.__graph.get_neighbours(vertex)):
            print(f"\t{neighbour} (cost of {self.__graph.get_cost_of_edge(vertex, neighbour)})")

    def __ui_change_edge_cost(self):
        _from = int(input("Give the starting vertex: "))
        _to = int(input("Give the ending vertex: "))
        new_cost = int(input("Give the new cost of the edge: "))
        self.__graph.change_edge_cost(_from, _to, new_cost)
        print(f"The cost of the edge {_from}<->{_to} was modified to {new_cost}.")

    def __ui_add_edge(self):
        _from = int(input("Give the starting vertex: "))
        _to = int(input("Give the ending vertex: "))
        cost = int(input("Give the cost of the edge: "))
        self.__graph.add_edge(_from, _to, cost)
        print(f"Edge {_from}<->{_to} with a cost of {cost} added.")

    def __ui_remove_edge(self):
        _from = int(input("Give the starting vertex: "))
        _to = int(input("Give the ending vertex: "))
        self.__graph.remove_edge(_from, _to)
        print(f"Edge {_from}<->{_to} removed.")

    def __ui_add_vertex(self):
        vertex = int(input("Give the new vertex: "))
        self.__graph.add_vertex(vertex)
        print(f"Vertex {vertex} added.")

    def __ui_remove_vertex(self):
        vertex = int(input("Give the vertex: "))
        self.__graph.remove_vertex(vertex)
        print(f"Vertex {vertex} removed.")

    def __ui_save_graph_to_file(self):
        file_name = input("Give the name of the file (with extension): ")
        graph_copy = self.__graph.get_copy_of_graph()
        write_graph(graph_copy, file_name)
        print(f"The graph was saved to {file_name}")

    def start(self):
        while True:
            self.__print_menu()
            cmd = input("Command: ")
            if cmd == 'x':
                break
            elif cmd in self.__commands.keys():
                try:
                    self.__commands[cmd]()
                except GraphException as ge:
                    print(str(ge))
                except ValueError:
                    print("Invalid numerical input.")
            else:
                print("Invalid command.")
            print()
