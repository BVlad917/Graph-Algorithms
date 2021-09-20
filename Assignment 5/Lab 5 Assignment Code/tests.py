import unittest

from directed_graph import read_graph, create_random_graph, write_graph, UndirectedGraph
from errors import GraphException


class TestUndirectedGraph(unittest.TestCase):
    def test_read_graph(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_vertices(), 5)
        self.assertEqual(graph.get_no_edges(), 5)
        neighbours = []
        for neighbour in graph.get_neighbours(0):
            neighbours.append(neighbour)
        self.assertEqual(len(neighbours), 2)
        neighbours.clear()

        for neighbour in graph.get_neighbours(1):
            neighbours.append(neighbour)
        self.assertEqual(len(neighbours), 3)
        neighbours.clear()

        for neighbour in graph.get_neighbours(2):
            neighbours.append(neighbour)
        self.assertEqual(len(neighbours), 2)
        neighbours.clear()

        for neighbour in graph.get_neighbours(3):
            neighbours.append(neighbour)
        self.assertEqual(len(neighbours), 3)
        neighbours.clear()

        for neighbour, cost in graph.get_neighbours(4):
            neighbours.append((neighbour, cost))
        self.assertEqual(len(neighbours), 0)

    def test_get_no_vertices(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_vertices(), 5)

    def test_get_no_edges(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_edges(), 5)

    def test_get_all_vertices(self):
        graph = read_graph("test_in_graph.txt")
        expected_vertices = [0, 1, 2, 3, 4]
        actual_vertices = []
        for vertex in graph.get_all_vertices():
            actual_vertices.append(vertex)
        self.assertEqual(len(expected_vertices), len(actual_vertices))
        self.assertIn(actual_vertices[0], expected_vertices)
        self.assertIn(actual_vertices[1], expected_vertices)
        self.assertIn(actual_vertices[2], expected_vertices)
        self.assertIn(actual_vertices[3], expected_vertices)
        self.assertIn(actual_vertices[4], expected_vertices)

    def test_get_all_edges(self):
        graph = read_graph("test_in_graph.txt")
        all_edges = []
        for _from, _to in graph.get_all_edges():
            all_edges.append((_from, _to))
        self.assertEqual(len(all_edges), 5)
        self.assertTrue(all_edges[0] == (0, 1))
        self.assertTrue(all_edges[1] == (0, 3))
        self.assertTrue(all_edges[2] == (1, 2))
        self.assertTrue(all_edges[3] == (1, 3))
        self.assertTrue(all_edges[4] == (2, 3))
        graph.add_edge(1, 4)
        all_edges.clear()
        for _from, _to in graph.get_all_edges():
            all_edges.append((_from, _to))
        self.assertEqual(len(all_edges), 6)
        self.assertIn((1, 4), all_edges)

    def test_check_edge(self):
        graph = read_graph("test_in_graph.txt")
        self.assertTrue(graph.is_edge_in_graph(0, 1))
        self.assertTrue(graph.is_edge_in_graph(1, 0))

        self.assertTrue(graph.is_edge_in_graph(1, 3))
        self.assertTrue(graph.is_edge_in_graph(3, 1))

        self.assertFalse(graph.is_edge_in_graph(1, 4))
        self.assertFalse(graph.is_edge_in_graph(4, 1))

    def test_check_vertex(self):
        graph = read_graph("test_in_graph.txt")
        self.assertTrue(graph.is_vertex_in_graph(0))
        self.assertTrue(graph.is_vertex_in_graph(1))
        self.assertTrue(graph.is_vertex_in_graph(4))
        self.assertFalse(graph.is_vertex_in_graph(7))

    def test_get_degree(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_degree(0), 2)
        self.assertEqual(graph.get_degree(1), 3)
        self.assertEqual(graph.get_degree(3), 3)
        self.assertEqual(graph.get_degree(4), 0)
        self.assertRaises(GraphException, graph.get_degree, 12)

    def test_get_neighbours(self):
        graph = read_graph("test_in_graph.txt")
        list_of_neighbours = []
        for x in graph.get_neighbours(1):
            list_of_neighbours.append(x)
        self.assertIn(0, list_of_neighbours)
        self.assertIn(2, list_of_neighbours)
        self.assertIn(3, list_of_neighbours)
        self.assertEqual(len(list_of_neighbours), 3)
        list_of_neighbours.clear()

        for x in graph.get_neighbours(2):
            list_of_neighbours.append(x)
        self.assertIn(1, list_of_neighbours)
        self.assertIn(3, list_of_neighbours)
        self.assertEqual(len(list_of_neighbours), 2)
        list_of_neighbours.clear()

        for x in graph.get_neighbours(4):
            list_of_neighbours.append(x)
        self.assertEqual(list_of_neighbours, [])
        self.assertTrue(graph.get_degree(4) == 0)

    def test_add_edge(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_edges(), 5)
        self.assertFalse(graph.is_edge_in_graph(1, 4))
        self.assertFalse(graph.is_edge_in_graph(4, 1))
        graph.add_edge(1, 4)
        self.assertTrue(graph.is_edge_in_graph(1, 4))
        self.assertTrue(graph.is_edge_in_graph(4, 1))
        self.assertEqual(graph.get_no_edges(), 6)
        self.assertRaises(GraphException, graph.add_edge, 1, 4)

    def test_remove_edge(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_edges(), 5)
        self.assertTrue(graph.is_edge_in_graph(1, 2))
        self.assertTrue(graph.is_edge_in_graph(2, 1))
        graph.remove_edge(1, 2)
        self.assertFalse(graph.is_edge_in_graph(1, 2))
        self.assertFalse(graph.is_edge_in_graph(2, 1))
        self.assertEqual(graph.get_no_edges(), 4)
        self.assertRaises(GraphException, graph.remove_edge, 1, 2)

    def test_add_vertex(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_vertices(), 5)
        self.assertFalse(graph.is_vertex_in_graph(5))
        graph.add_vertex(5)
        self.assertEqual(graph.get_no_vertices(), 6)
        self.assertTrue(graph.is_vertex_in_graph(5))
        self.assertEqual(graph.get_degree(5), 0)
        self.assertRaises(GraphException, graph.add_vertex, 5)
        graph.add_edge(1, 5)
        graph.add_edge(2, 5)
        self.assertEqual(graph.get_degree(5), 2)
        neighbours = []
        for neighbour in graph.get_neighbours(5):
            neighbours.append(neighbour)
        self.assertEqual(len(neighbours), 2)
        self.assertIn(1, neighbours)
        self.assertIn(2, neighbours)

    def test_remove_vertex(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_vertices(), 5)
        self.assertEqual(graph.get_no_edges(), 5)
        self.assertRaises(GraphException, graph.remove_vertex, 7)
        self.assertTrue(graph.is_vertex_in_graph(3))
        graph.remove_vertex(3)
        self.assertFalse(graph.is_vertex_in_graph(3))
        self.assertEqual(graph.get_no_vertices(), 4)
        self.assertEqual(graph.get_no_edges(), 2)
        self.assertNotIn(3, graph.get_all_vertices())
        self.assertNotIn(3, graph.get_neighbours(0))
        self.assertNotIn(3, graph.get_neighbours(1))
        self.assertNotIn(3, graph.get_neighbours(2))
        self.assertNotIn(3, graph.get_neighbours(4))
        all_edges = []
        for _from, _to in graph.get_all_edges():
            all_edges.append((_from, _to))
        self.assertNotIn(3, [pair[0] for pair in all_edges])
        self.assertNotIn(3, [pair[1] for pair in all_edges])

    def test_get_copy_of_graph(self):
        graph = read_graph("test_in_graph.txt")
        copy = graph.get_copy_of_graph()
        copy.add_vertex(5)
        self.assertEqual(graph.get_no_vertices(), 5)
        self.assertEqual(copy.get_no_vertices(), 6)
        self.assertNotIn(5, graph.get_all_vertices())
        self.assertIn(5, copy.get_all_vertices())
        copy.add_edge(1, 5)
        self.assertEqual(copy.get_no_edges(), 6)
        self.assertEqual(graph.get_no_edges(), 5)
        graph.remove_vertex(1)
        self.assertEqual(graph.get_no_vertices(), 4)
        self.assertEqual(copy.get_no_vertices(), 6)

    def test_write_graph(self):
        graph = read_graph("test_in_graph.txt")
        graph.remove_vertex(3)
        graph.remove_edge(0, 1)
        graph.add_vertex(5)
        graph.add_edge(4, 5)
        graph.add_edge(0, 4)
        write_graph(graph, "test_out_graph.txt")

    def test_create_random_graph(self):
        random_graph = create_random_graph(6, 7)
        self.assertEqual(random_graph.get_no_vertices(), 6)
        self.assertEqual(random_graph.get_no_edges(), 7)
        # for edge in random_graph.get_all_edges():
        #     print(edge)
        # print()
        # for x in random_graph.get_all_vertices():
        #     print(f"{x}: ")
        #     for y in random_graph.get_neighbours(x):
        #         print(f"\t{x} <-> {y}")

    #################################################################################
    # ##### TESTS FOR THE NEWLY IMPLEMENTED FUNCTIONALITY - HAMILTONIAN CYCLE ##### #
    #################################################################################
    def test_find_hamiltonian_cycle(self):
        """
        Only this test will run since the others use an external file that is not included in the directory.
        The important thing is that this test function shows that the algorithm for finding a Hamiltonian cycle works.
        (And this function can be run in isolation, without running the other test functions)
        """
        graph1 = UndirectedGraph()
        graph1.add_vertex(0)
        graph1.add_vertex(1)
        graph1.add_vertex(2)
        graph1.add_vertex(3)
        graph1.add_vertex(4)
        graph1.add_edge(0, 1)
        graph1.add_edge(0, 4)
        graph1.add_edge(1, 2)
        graph1.add_edge(1, 3)
        graph1.add_edge(1, 4)
        graph1.add_edge(2, 3)
        graph1.add_edge(3, 4)
        path = graph1.find_hamiltonian_cycle()
        self.assertEqual(len(path), 6)
        self.assertEqual(path[0], path[-1])
        self.assertTrue(graph1.is_edge_in_graph(path[0], path[1]))
        self.assertTrue(graph1.is_edge_in_graph(path[1], path[2]))
        self.assertTrue(graph1.is_edge_in_graph(path[2], path[3]))
        self.assertTrue(graph1.is_edge_in_graph(path[3], path[4]))
        self.assertTrue(graph1.is_edge_in_graph(path[4], path[5]))
        self.assertEqual(len(path[:-1]), 5)
        self.assertIn(0, path[:-1])
        self.assertIn(1, path[:-1])
        self.assertIn(2, path[:-1])
        self.assertIn(3, path[:-1])
        self.assertIn(4, path[:-1])
        # print(path)
        # The returned Hamiltonian cycle is: [0, 1, 2, 3, 4, 0]

        # Now we test the case where there is no Hamiltonian cycle in the graph
        graph2 = UndirectedGraph()
        graph2.add_vertex(0)
        graph2.add_vertex(1)
        graph2.add_vertex(2)
        graph2.add_vertex(3)
        graph2.add_vertex(4)
        graph2.add_edge(0, 1)
        graph2.add_edge(0, 3)
        graph2.add_edge(1, 2)
        graph2.add_edge(1, 3)
        graph2.add_edge(2, 3)
        path = graph2.find_hamiltonian_cycle()
        # print(path)
        self.assertIsNone(path)
