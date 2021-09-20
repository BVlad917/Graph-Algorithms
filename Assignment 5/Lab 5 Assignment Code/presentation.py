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
            '7': self.__ui_get_degree,
            '8': self.__ui_get_neighbours,
            '9': self.__ui_add_edge,
            '10': self.__ui_remove_edge,
            '11': self.__ui_add_vertex,
            '12': self.__ui_remove_vertex,
            '13': self.__ui_save_graph_to_file,
            '14': self.__ui_find_hamiltonian_cycle,
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
              "\t7 - Get the degree of a vertex\n"
              "\t8 - Get the neighbours of a vertex\n"
              "\t9 - Add an edge\n"
              "\t10 - Remove an edge\n"
              "\t11 - Add a vertex\n"
              "\t12 - Remove a vertex\n"
              "\t13 - Write the graph to a file\n"
              "\t*14 - Find a Hamiltonian cycle\n"
              "\tx - Exit\n"
              "* - Added in Assignment 5")

    def __ui_find_hamiltonian_cycle(self):
        hamiltonian_cycle = self.__graph.find_hamiltonian_cycle()
        if hamiltonian_cycle is None:
            print("There is no Hamiltonian cycle in the given graph.")
        else:
            print(f"One Hamiltonian cycle is: {hamiltonian_cycle}")

    def __ui_get_number_of_vertices(self):
        print(f"The number of vertices in the graph is {self.__graph.get_no_vertices()}.")

    def __ui_get_number_of_edges(self):
        print(f"The number of edges in the graph is {self.__graph.get_no_edges()}.")

    def __ui_get_set_of_vertices(self):
        print(f"The set of vertices in the graph is: ", end='')
        print(', '.join(str(vertex) for vertex in self.__graph.get_all_vertices()))

    def __ui_get_set_of_edges(self):
        print(f"The set of edges in the graph is:")
        for _from, _to in sorted(self.__graph.get_all_edges()):
            print(f"\t{_from}<->{_to}")

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
            print(f"Yes, there is an edge between {_from} and {_to}.")
        else:
            print(f"No, there is no edge between {_from} and {_to}.")

    def __ui_get_degree(self):
        vertex = int(input("Give the vertex: "))
        print(f"The in degree of the vertex {vertex} is {self.__graph.get_degree(vertex)}.")

    def __ui_get_neighbours(self):
        vertex = int(input("Give the vertex: "))
        if self.__graph.get_degree(vertex) == 0:
            print(f"The vertex {vertex} has no neighbours.")
            return
        print(f"The neighbours of vertex {vertex} are: ", end='')
        print(', '.join(str(neighbour) for neighbour in sorted(self.__graph.get_neighbours(vertex))))

    def __ui_add_edge(self):
        _from = int(input("Give the starting vertex: "))
        _to = int(input("Give the ending vertex: "))
        self.__graph.add_edge(_from, _to)
        print(f"Edge {_from}<->{_to} added.")

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
