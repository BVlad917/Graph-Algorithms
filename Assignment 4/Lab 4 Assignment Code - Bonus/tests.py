import unittest

from directed_graph import read_graph, create_random_graph, write_graph, DirectedGraph
from errors import GraphException


class TestTripleDictGraph(unittest.TestCase):
    def test_read_graph(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_vertices(), 6)
        self.assertEqual(graph.get_no_edges(), 7)
        out_neighbours = []
        for out_neighbour in graph.get_outbound_neighbours(0):
            out_neighbours.append(out_neighbour)
        self.assertEqual(len(out_neighbours), 1)
        out_neighbours.clear()

        for out_neighbour in graph.get_outbound_neighbours(1):
            out_neighbours.append(out_neighbour)
        self.assertEqual(len(out_neighbours), 1)
        out_neighbours.clear()

        for out_neighbour in graph.get_outbound_neighbours(2):
            out_neighbours.append(out_neighbour)
        self.assertEqual(len(out_neighbours), 1)
        out_neighbours.clear()

        for out_neighbour in graph.get_outbound_neighbours(3):
            out_neighbours.append(out_neighbour)
        self.assertEqual(len(out_neighbours), 0)
        out_neighbours.clear()

        for out_neighbour in graph.get_outbound_neighbours(4):
            out_neighbours.append(out_neighbour)
        self.assertEqual(len(out_neighbours), 2)

    def test_get_no_vertices(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_vertices(), 6)

    def test_get_no_edges(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_edges(), 7)

    def test_get_all_vertices(self):
        graph = read_graph("test_in_graph.txt")
        expected_vertices = [0, 1, 2, 3, 4, 5]
        for index, vertex in enumerate(graph.get_all_vertices()):
            self.assertEqual(vertex, expected_vertices[index])

    def test_get_all_edges(self):
        graph = read_graph("test_in_graph.txt")
        all_edges = []
        expected_all_edges = [(0, 3), (1, 3), (2, 3), (4, 0), (4, 1), (5, 0), (5, 2)]
        for _from, _to in graph.get_all_edges():
            all_edges.append((_from, _to))
        self.assertEqual(len(all_edges), 7)
        self.assertTrue(expected_all_edges[0] in all_edges)
        self.assertTrue(expected_all_edges[1] in all_edges)
        self.assertTrue(expected_all_edges[2] in all_edges)
        self.assertTrue(expected_all_edges[3] in all_edges)
        self.assertTrue(expected_all_edges[4] in all_edges)
        self.assertTrue(expected_all_edges[5] in all_edges)
        self.assertTrue(expected_all_edges[6] in all_edges)

    def test_check_edge(self):
        graph = read_graph("test_in_graph.txt")
        self.assertTrue(graph.is_edge_in_graph(0, 3))
        self.assertTrue(graph.is_edge_in_graph(1, 3))
        self.assertTrue(graph.is_edge_in_graph(4, 0))
        self.assertFalse(graph.is_edge_in_graph(1, 5))

    def test_check_vertex(self):
        graph = read_graph("test_in_graph.txt")
        self.assertTrue(graph.is_vertex_in_graph(0))
        self.assertTrue(graph.is_vertex_in_graph(1))
        self.assertTrue(graph.is_vertex_in_graph(4))
        self.assertFalse(graph.is_vertex_in_graph(7))

    def test_get_in_degree(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_in_degree(0), 2)
        self.assertEqual(graph.get_in_degree(1), 1)
        self.assertEqual(graph.get_in_degree(4), 0)

    def test_get_out_degree(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_out_degree(0), 1)
        self.assertEqual(graph.get_out_degree(1), 1)
        self.assertEqual(graph.get_out_degree(4), 2)

    def test_get_outbound_neighbours(self):
        graph = read_graph("test_in_graph.txt")
        list_of_neighbours = []
        for x in graph.get_outbound_neighbours(1):
            list_of_neighbours.append(x)
        self.assertEqual(list_of_neighbours, [3])
        list_of_neighbours.clear()
        for x in graph.get_outbound_neighbours(2):
            list_of_neighbours.append(x)
        self.assertEqual(list_of_neighbours, [3])
        list_of_neighbours.clear()
        for x in graph.get_outbound_neighbours(4):
            list_of_neighbours.append(x)
        self.assertEqual(list_of_neighbours, [0, 1])
        self.assertTrue(graph.get_out_degree(4) == 2)

    def test_get_inbound_neighbours(self):
        graph = read_graph("test_in_graph.txt")
        list_of_neighbours = []
        for x in graph.get_inbound_neighbours(1):
            list_of_neighbours.append(x)
        self.assertEqual(list_of_neighbours, [4])
        list_of_neighbours.clear()
        for x in graph.get_inbound_neighbours(2):
            list_of_neighbours.append(x)
        self.assertEqual(list_of_neighbours, [5])
        list_of_neighbours.clear()
        for x in graph.get_inbound_neighbours(4):
            list_of_neighbours.append(x)
        self.assertEqual(list_of_neighbours, [])
        self.assertTrue(graph.get_in_degree(4) == 0)

    def test_add_edge(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_edges(), 7)
        self.assertFalse(graph.is_edge_in_graph(1, 4))
        graph.add_edge(1, 4)
        self.assertTrue(graph.is_edge_in_graph(1, 4))
        self.assertEqual(graph.get_no_edges(), 8)
        self.assertTrue(graph.is_edge_in_graph(1, 4))
        self.assertRaises(GraphException, graph.add_edge, 1, 4)

    def test_remove_edge(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_edges(), 7)
        self.assertTrue(graph.is_edge_in_graph(1, 3))
        graph.remove_edge(1, 3)
        self.assertFalse(graph.is_edge_in_graph(1, 3))
        self.assertEqual(graph.get_no_edges(), 6)
        self.assertFalse(graph.is_edge_in_graph(1, 3))
        self.assertRaises(GraphException, graph.remove_edge, 1, 2)

    def test_add_vertex(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_vertices(), 6)
        self.assertTrue(graph.is_vertex_in_graph(5))
        self.assertFalse(graph.is_vertex_in_graph(6))
        graph.add_vertex(6)
        self.assertTrue(graph.is_vertex_in_graph(6))
        self.assertEqual(graph.get_no_vertices(), 7)
        self.assertEqual(graph.get_out_degree(6), 0)
        self.assertEqual(graph.get_in_degree(6), 0)
        self.assertRaises(GraphException, graph.add_vertex, 5)

    def test_remove_vertex(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_vertices(), 6)
        self.assertRaises(GraphException, graph.remove_vertex, 7)
        self.assertTrue(graph.is_vertex_in_graph(3))
        graph.remove_vertex(3)
        self.assertFalse(graph.is_vertex_in_graph(3))
        self.assertEqual(graph.get_no_vertices(), 5)
        self.assertNotIn(3, graph.get_all_vertices())
        self.assertNotIn(3, graph.get_outbound_neighbours(0))
        self.assertNotIn(3, graph.get_outbound_neighbours(1))
        self.assertNotIn(3, graph.get_outbound_neighbours(2))
        self.assertNotIn(3, graph.get_outbound_neighbours(4))
        self.assertNotIn(3, graph.get_inbound_neighbours(0))
        self.assertNotIn(3, graph.get_inbound_neighbours(1))
        self.assertNotIn(3, graph.get_inbound_neighbours(2))
        self.assertNotIn(3, graph.get_inbound_neighbours(4))
        all_edges = []
        for _from, _to in graph.get_all_edges():
            all_edges.append((_from, _to))
        self.assertNotIn(3, [pair[0] for pair in all_edges])
        self.assertNotIn(3, [pair[1] for pair in all_edges])

    def test_get_copy_of_graph(self):
        graph = read_graph("test_in_graph.txt")
        copy = graph.get_copy_of_graph()
        copy.add_vertex(6)
        self.assertEqual(graph.get_no_vertices(), 6)
        self.assertEqual(copy.get_no_vertices(), 7)
        self.assertNotIn(6, graph.get_all_vertices())
        self.assertIn(6, copy.get_all_vertices())
        copy.add_edge(1, 5)
        self.assertEqual(copy.get_no_edges(), 8)
        self.assertEqual(graph.get_no_edges(), 7)
        graph.remove_vertex(1)
        self.assertEqual(graph.get_no_vertices(), 5)
        self.assertEqual(copy.get_no_vertices(), 7)

    def test_write_graph(self):
        graph = read_graph("test_in_graph.txt")
        graph.remove_vertex(3)
        graph.remove_edge(4, 0)
        graph.add_vertex(6)
        graph.add_edge(4, 6)
        graph.add_edge(0, 2)
        write_graph(graph, "test_out_graph.txt")

    def test_create_random_graph(self):
        random_graph = create_random_graph(6, 7)
        self.assertEqual(random_graph.get_no_vertices(), 6)
        self.assertEqual(random_graph.get_no_edges(), 7)
        # for x in random_graph.get_all_vertices():
        #     print(f"{x}: ")
        #     for y in random_graph.get_outbound_neighbours(x):
        #         print(f"\t{x} -> {y}")

    ###############################################################
    # ##### TESTS FOR THE ASSIGNMENT 4 BONUS IMPLEMENTATION ##### #
    ###############################################################

    def test_get_duration(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_duration(0), 1)
        self.assertEqual(graph.get_duration(1), 2)
        self.assertEqual(graph.get_duration(2), 3)
        self.assertEqual(graph.get_duration(3), 5)
        self.assertEqual(graph.get_duration(4), 4)
        self.assertEqual(graph.get_duration(5), 3)

    def test_topological_sort(self):
        graph = DirectedGraph()
        graph.add_vertex(0, 1)
        graph.add_vertex(1, 2)
        graph.add_vertex(2, 3)
        graph.add_vertex(3, 5)
        graph.add_vertex(4, 4)
        graph.add_vertex(5, 3)
        graph.add_edge(0, 3)
        graph.add_edge(1, 3)
        graph.add_edge(2, 3)
        graph.add_edge(4, 0)
        graph.add_edge(4, 1)
        graph.add_edge(5, 0)
        graph.add_edge(5, 2)
        topological_sort = graph.topological_sort()
        self.assertTrue(topological_sort.index(1) > topological_sort.index(4))
        self.assertTrue(topological_sort.index(0) > topological_sort.index(4))
        self.assertTrue(topological_sort.index(0) > topological_sort.index(5))
        self.assertTrue(topological_sort.index(2) > topological_sort.index(5))
        self.assertTrue(topological_sort.index(3) > topological_sort.index(0))
        self.assertTrue(topological_sort.index(3) > topological_sort.index(1))
        self.assertTrue(topological_sort.index(3) > topological_sort.index(2))
        self.assertTrue(topological_sort.index(3) > topological_sort.index(4))
        self.assertTrue(topological_sort.index(3) > topological_sort.index(5))

    def test_schedule_activities(self):
        graph = DirectedGraph()
        graph.add_vertex(0, 1)
        graph.add_vertex(1, 2)
        graph.add_vertex(2, 3)
        graph.add_vertex(3, 5)
        graph.add_vertex(4, 4)
        graph.add_vertex(5, 3)
        graph.add_edge(0, 3)
        graph.add_edge(1, 3)
        graph.add_edge(2, 3)
        graph.add_edge(4, 0)
        graph.add_edge(4, 1)
        graph.add_edge(5, 0)
        graph.add_edge(5, 2)
        earliest_start, earliest_end, latest_start, latest_end = graph.schedule_activities()
        # Test the earliest scheduling
        self.assertEqual(earliest_start[0], 4)
        self.assertEqual(earliest_end[0], 5)
        self.assertEqual(earliest_start[1], 4)
        self.assertEqual(earliest_end[1], 6)
        self.assertEqual(earliest_start[2], 3)
        self.assertEqual(earliest_end[2], 6)
        self.assertEqual(earliest_start[3], 6)
        self.assertEqual(earliest_end[3], 11)
        self.assertEqual(earliest_start[4], 0)
        self.assertEqual(earliest_end[4], 4)
        self.assertEqual(earliest_start[5], 0)
        self.assertEqual(earliest_end[5], 3)
        # Test the latest scheduling
        self.assertEqual(latest_start[0], 5)
        self.assertEqual(latest_end[0], 6)
        self.assertEqual(latest_start[1], 4)
        self.assertEqual(latest_end[1], 6)
        self.assertEqual(latest_start[2], 3)
        self.assertEqual(latest_end[2], 6)
        self.assertEqual(latest_start[3], 6)
        self.assertEqual(latest_end[3], 11)
        self.assertEqual(latest_start[4], 0)
        self.assertEqual(latest_end[4], 4)
        self.assertEqual(latest_start[5], 0)
        self.assertEqual(latest_end[5], 3)

    def test_get_no_paths_between_2_vertices(self):
        graph = DirectedGraph()
        graph.add_vertex(0, 1)
        graph.add_vertex(1, 2)
        graph.add_vertex(2, 3)
        graph.add_vertex(3, 5)
        graph.add_vertex(4, 4)
        graph.add_vertex(5, 3)
        graph.add_edge(0, 3)
        graph.add_edge(1, 3)
        graph.add_edge(2, 3)
        graph.add_edge(4, 0)
        graph.add_edge(4, 1)
        graph.add_edge(5, 0)
        graph.add_edge(5, 2)
        self.assertEqual(graph.get_no_paths_between_2_vertices(4, 3), 2)
        self.assertEqual(graph.get_no_paths_between_2_vertices(5, 3), 2)
        self.assertEqual(graph.get_no_paths_between_2_vertices(4, 0), 1)
        self.assertEqual(graph.get_no_paths_between_2_vertices(1, 3), 1)
        self.assertEqual(graph.get_no_paths_between_2_vertices(4, 2), 0)
