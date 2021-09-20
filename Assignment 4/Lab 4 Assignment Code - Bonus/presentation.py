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
            '5': self.__ui_get_all_durations,
            '6': self.__ui_check_vertex,
            '7': self.__ui_check_edge,
            '8': self.__ui_change_activity_duration,
            '9': self.__ui_get_in_degree,
            '10': self.__ui_get_out_degree,
            '11': self.__ui_get_outbound_neighbours,
            '12': self.__ui_get_inbound_neighbours,
            '13': self.__ui_add_edge,
            '14': self.__ui_remove_edge,
            '15': self.__ui_add_vertex,
            '16': self.__ui_remove_vertex,
            '17': self.__ui_save_graph_to_file,
            '18': self.__ui_activities_sort,
            '19': self.__ui_find_no_distinct_paths_between_2_vertices,
        }

    @staticmethod
    def __print_menu():
        print("Graph operations:\n"
              "\t1 - Get the number of vertices in the graph\n"
              "\t2 - Get the number of edges in the graph\n"
              "\t3 - Get the set of vertices in the graph\n"
              "\t4 - Get the set of edges in the graph\n"
              "\t5 - Get all the activity durations\n"
              "\t6 - Check if a given vertex is in the graph\n"
              "\t7 - Check if a given edge is in the graph\n"
              "\t8 - Change the duration of an activity\n"
              "\t9 - Get the in degree of a vertex\n"
              "\t10 - Get the out degree of a vertex\n"
              "\t11 - Get the outbound neighbours of a vertex\n"
              "\t12 - Get the inbound neighbours of a vertex\n"
              "\t13 - Add an edge\n"
              "\t14 - Remove an edge\n"
              "\t15 - Add a vertex\n"
              "\t16 - Remove a vertex\n"
              "\t17 - Write the graph to a file\n"
              "\t*18 - Sort the activities\n"
              "\t*19 - Find the number of distinct paths between 2 given vertices\n"
              "\tx - Exit\n"
              "* - Added in Assignment 3")

    def __ui_get_all_durations(self):
        print("The activity durations are:")
        for vertex, duration in self.__graph.get_all_durations():
            print(f"Vertex {vertex}: {duration} hours")

    def __ui_change_activity_duration(self):
        vertex = int(input("Give the activity vertex whose duration you want changed: "))
        new_duration = int(input("Give the new duration: "))
        self.__graph.change_activity_duration(vertex, new_duration)
        print(f"The activity duration of vertex {vertex} was changed to {new_duration} hours.")

    def __ui_activities_sort(self):
        earliest_start, earliest_end, latest_start, latest_end = self.__graph.schedule_activities()
        # Earliest sorting
        print("EARLIEST SORTING")
        for vertex in self.__graph.get_all_vertices():
            print(f"Activity {vertex}: Starts at {earliest_start[vertex]}, Ends at {earliest_end[vertex]}")
        # Latest sorting
        print("\nLATEST SORTING")
        for vertex in self.__graph.get_all_vertices():
            print(f"Activity {vertex}: Starts at {latest_start[vertex]}, Ends at {latest_end[vertex]}")

    def __ui_find_no_distinct_paths_between_2_vertices(self):
        start = int(input("Give the starting vertex: "))
        end = int(input("Give the ending vertex: "))
        no_paths = self.__graph.get_no_paths_between_2_vertices(start, end)
        print(f"The number of distinct paths between vertex {start} and vertex {end} is {no_paths}")

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
            print(f"{_from}->{_to}")

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

    def __ui_get_in_degree(self):
        vertex = int(input("Give the vertex: "))
        print(f"The in degree of the vertex {vertex} is {self.__graph.get_in_degree(vertex)}.")

    def __ui_get_out_degree(self):
        vertex = int(input("Give the vertex: "))
        print(f"The out degree of the vertex {vertex} is {self.__graph.get_out_degree(vertex)}.")

    def __ui_get_outbound_neighbours(self):
        vertex = int(input("Give the vertex: "))
        if self.__graph.get_out_degree(vertex) == 0:
            print(f"The vertex {vertex} has no outbound neighbours.")
            return
        print(f"The outbound neighbours of vertex {vertex} are:")
        for neighbour in sorted(self.__graph.get_outbound_neighbours(vertex)):
            print(f"{neighbour} ", end='')
        print()

    def __ui_get_inbound_neighbours(self):
        vertex = int(input("Give the vertex: "))
        if self.__graph.get_in_degree(vertex) == 0:
            print(f"The vertex {vertex} has no outbound neighbours.")
            return
        print(f"The inbound neighbours of vertex {vertex} are:")
        for neighbour in sorted(self.__graph.get_inbound_neighbours(vertex)):
            print(f"{neighbour} ", end='')
        print()

    def __ui_add_edge(self):
        _from = int(input("Give the starting vertex: "))
        _to = int(input("Give the ending vertex: "))
        self.__graph.add_edge(_from, _to)
        print(f"Edge {_from}->{_to} added.")

    def __ui_remove_edge(self):
        _from = int(input("Give the starting vertex: "))
        _to = int(input("Give the ending vertex: "))
        self.__graph.remove_edge(_from, _to)
        print(f"Edge {_from}->{_to} removed.")

    def __ui_add_vertex(self):
        vertex = int(input("Give the new vertex: "))
        duration = int(input("Give the duration of the new vertex: "))
        self.__graph.add_vertex(vertex, duration)
        print(f"Vertex {vertex} (with a duration of {duration} hours) added.")

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
