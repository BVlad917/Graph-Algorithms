import unittest

from directed_graph import read_graph, create_random_graph, write_graph, UndirectedGraph
from errors import GraphException


class TestTripleDictGraph(unittest.TestCase):
    def test_read_graph(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_vertices(), 5)
        self.assertEqual(graph.get_no_edges(), 5)
        neighbours_with_cost = []
        for out_neighbour, cost in graph.get_neighbours_with_cost(0):
            neighbours_with_cost.append((out_neighbour, cost))
        self.assertEqual(len(neighbours_with_cost), 2)
        neighbours_with_cost.clear()

        for neighbour, cost in graph.get_neighbours_with_cost(1):
            neighbours_with_cost.append((neighbour, cost))
        self.assertEqual(len(neighbours_with_cost), 3)
        neighbours_with_cost.clear()

        for neighbour, cost in graph.get_neighbours_with_cost(2):
            neighbours_with_cost.append((neighbour, cost))
        self.assertEqual(len(neighbours_with_cost), 2)
        neighbours_with_cost.clear()

        for neighbour, cost in graph.get_neighbours_with_cost(3):
            neighbours_with_cost.append((neighbour, cost))
        self.assertEqual(len(neighbours_with_cost), 2)
        neighbours_with_cost.clear()

        for neighbour, cost in graph.get_neighbours_with_cost(4):
            neighbours_with_cost.append((neighbour, cost))
        self.assertEqual(len(neighbours_with_cost), 0)

    def test_get_no_vertices(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_vertices(), 5)

    def test_get_no_edges(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_edges(), 5)

    def test_get_all_vertices(self):
        graph = read_graph("test_in_graph.txt")
        expected_vertices = [0, 1, 2, 3, 4]
        for index, vertex in enumerate(graph.get_all_vertices()):
            self.assertEqual(vertex, expected_vertices[index])

    def test_get_all_edges(self):
        graph = read_graph("test_in_graph.txt")
        all_edges_with_cost = []
        for _from, _to, _cost in graph.get_all_edges():
            all_edges_with_cost.append((_from, _to, _cost))
        self.assertEqual(len(all_edges_with_cost), 5)
        self.assertTrue(all_edges_with_cost[0] == (0, 0, 1))
        self.assertTrue(all_edges_with_cost[1] == (0, 1, 7) or all_edges_with_cost[1] == (1, 0, 7))
        self.assertTrue(all_edges_with_cost[2] == (1, 2, 2) or all_edges_with_cost[2] == (2, 1, 2))
        self.assertTrue(all_edges_with_cost[3] == (1, 3, 8) or all_edges_with_cost[3] == (3, 1, 8))
        self.assertTrue(all_edges_with_cost[4] == (2, 3, 5) or all_edges_with_cost[4] == (3, 2, 5))
        graph.add_edge(1, 4, 10)
        all_edges_with_cost.clear()
        for _from, _to, _cost in graph.get_all_edges():
            all_edges_with_cost.append((_from, _to, _cost))
        self.assertEqual(len(all_edges_with_cost), 6)
        self.assertTrue(all_edges_with_cost[5] == (4, 1, 10) or all_edges_with_cost[5] == (1, 4, 10))

    def test_get_cost_of_edge(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_cost_of_edge(0, 0), 1)
        self.assertEqual(graph.get_cost_of_edge(1, 2), 2)
        self.assertEqual(graph.get_cost_of_edge(2, 1), 2)
        self.assertEqual(graph.get_cost_of_edge(1, 3), 8)
        self.assertEqual(graph.get_cost_of_edge(3, 1), 8)
        self.assertRaises(GraphException, graph.get_cost_of_edge, 1, 4)
        self.assertRaises(GraphException, graph.get_cost_of_edge, 4, 1)

    def test_check_edge(self):
        graph = read_graph("test_in_graph.txt")
        self.assertTrue(graph.is_edge_in_graph(0, 0))

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

    def test_get_neighbours_with_cost(self):
        graph = read_graph("test_in_graph.txt")
        info = []
        for neighbour_and_cost in graph.get_neighbours_with_cost(1):
            info.append(neighbour_and_cost)
        self.assertIn((0, 7), info)
        self.assertIn((2, 2), info)
        self.assertIn((3, 8), info)
        self.assertEqual(len(info), 3)
        info.clear()

        for neighbour_and_cost in graph.get_neighbours_with_cost(2):
            info.append(neighbour_and_cost)
        self.assertIn((1, 2), info)
        self.assertIn((3, 5), info)
        self.assertEqual(len(info), 2)
        info.clear()

        for neighbour_and_cost in graph.get_neighbours_with_cost(4):
            info.append(neighbour_and_cost)
        self.assertEqual(info, [])
        info.clear()

    def test_change_edge_cost(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_cost_of_edge(1, 2), 2)
        self.assertEqual(graph.get_cost_of_edge(2, 1), 2)
        graph.change_edge_cost(1, 2, 10)
        self.assertEqual(graph.get_cost_of_edge(1, 2), 10)
        self.assertEqual(graph.get_cost_of_edge(2, 1), 10)

    def test_add_edge(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_edges(), 5)
        self.assertFalse(graph.is_edge_in_graph(1, 4))
        self.assertFalse(graph.is_edge_in_graph(4, 1))
        graph.add_edge(1, 4, 10)
        self.assertTrue(graph.is_edge_in_graph(1, 4))
        self.assertTrue(graph.is_edge_in_graph(4, 1))
        self.assertEqual(graph.get_no_edges(), 6)
        self.assertTrue(graph.is_edge_in_graph(1, 4))
        self.assertTrue(graph.is_edge_in_graph(4, 1))
        self.assertEqual(graph.get_cost_of_edge(1, 4), 10)
        self.assertEqual(graph.get_cost_of_edge(4, 1), 10)
        self.assertRaises(GraphException, graph.add_edge, 1, 4, 20)

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

    def test_remove_vertex(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_vertices(), 5)
        self.assertRaises(GraphException, graph.remove_vertex, 7)
        self.assertTrue(graph.is_vertex_in_graph(3))
        graph.remove_vertex(3)
        self.assertFalse(graph.is_vertex_in_graph(3))
        self.assertEqual(graph.get_no_vertices(), 4)
        self.assertNotIn(3, graph.get_all_vertices())
        self.assertNotIn(3, graph.get_neighbours(0))
        self.assertNotIn(3, graph.get_neighbours(1))
        self.assertNotIn(3, graph.get_neighbours(2))
        self.assertNotIn(3, graph.get_neighbours(4))
        all_edges_with_cost = []
        for _from, _to, _cost in graph.get_all_edges():
            all_edges_with_cost.append((_from, _to, _cost))
        self.assertNotIn(3, [triplet[0] for triplet in all_edges_with_cost])
        self.assertNotIn(3, [triplet[1] for triplet in all_edges_with_cost])

    def test_get_copy_of_graph(self):
        graph = read_graph("test_in_graph.txt")
        copy = graph.get_copy_of_graph()
        copy.add_vertex(5)
        self.assertEqual(graph.get_no_vertices(), 5)
        self.assertEqual(copy.get_no_vertices(), 6)
        self.assertNotIn(5, graph.get_all_vertices())
        self.assertIn(5, copy.get_all_vertices())
        copy.add_edge(1, 5, 20)
        self.assertEqual(copy.get_no_edges(), 6)
        self.assertEqual(graph.get_no_edges(), 5)
        graph.remove_vertex(1)
        self.assertEqual(graph.get_no_vertices(), 4)
        self.assertEqual(copy.get_no_vertices(), 6)

    def test_write_graph(self):
        graph = read_graph("test_in_graph.txt")
        graph.remove_vertex(3)
        graph.remove_edge(0, 0)
        graph.add_vertex(5)
        graph.add_edge(4, 5, 10)
        graph.add_edge(0, 4, 20)
        write_graph(graph, "test_out_graph.txt")

    def test_create_random_graph(self):
        random_graph = create_random_graph(6, 7)
        self.assertEqual(random_graph.get_no_vertices(), 6)
        self.assertEqual(random_graph.get_no_edges(), 7)
        # for x in random_graph.get_all_vertices():
        #     print(f"{x}: ")
        #     for y in random_graph.get_outbound_neighbours(x):
        #         print(f"\t{x} -> {y}, cost: {random_graph.get_cost_of_edge(x, y)}")

    def test_prim_algorithm(self):
        # 1st example
        graph = UndirectedGraph(5)
        graph.add_edge(0, 1, 2)
        graph.add_edge(0, 3, 6)
        graph.add_edge(1, 2, 3)
        graph.add_edge(1, 3, 8)
        graph.add_edge(1, 4, 5)
        graph.add_edge(2, 4, 7)
        graph.add_edge(4, 3, 9)
        mst_edges = graph.prim_algorithm(0)
        total_cost = 0
        for start_vertex, end_vertex in mst_edges:
            total_cost += graph.get_cost_of_edge(start_vertex, end_vertex)
        self.assertEqual(total_cost, 16)

        # 2nd example
        graph = UndirectedGraph(7)
        graph.add_edge(0, 1, 2)
        graph.add_edge(0, 2, 3)
        graph.add_edge(0, 3, 3)
        graph.add_edge(1, 2, 4)
        graph.add_edge(1, 4, 3)
        graph.add_edge(2, 4, 1)
        graph.add_edge(2, 5, 6)
        graph.add_edge(3, 5, 7)
        graph.add_edge(4, 5, 8)
        graph.add_edge(5, 6, 9)
        mst_edges = graph.prim_algorithm(0)
        total_cost = 0
        for start_vertex, end_vertex in mst_edges:
            total_cost += graph.get_cost_of_edge(end_vertex, start_vertex)
        self.assertEqual(total_cost, 24)

        # 3rd example
        graph = UndirectedGraph(9)
        graph.add_edge(0, 1, 4)
        graph.add_edge(0, 7, 8)
        graph.add_edge(1, 7, 11)
        graph.add_edge(1, 2, 8)
        graph.add_edge(7, 8, 7)
        graph.add_edge(7, 6, 1)
        graph.add_edge(2, 8, 2)
        graph.add_edge(8, 6, 6)
        graph.add_edge(6, 5, 2)
        graph.add_edge(2, 5, 4)
        graph.add_edge(2, 3, 7)
        graph.add_edge(3, 5, 14)
        graph.add_edge(3, 4, 9)
        graph.add_edge(4, 5, 10)
        self.assertEqual(graph.get_no_vertices(), 9)
        self.assertEqual(graph.get_no_edges(), 14)
        self.assertEqual(graph.get_cost_of_edge(7, 1), graph.get_cost_of_edge(1, 7))
        mst_edges = graph.prim_algorithm(0)
        total_cost = 0
        # print(mst_edges)
        for start_vertex, end_vertex in mst_edges:
            total_cost += graph.get_cost_of_edge(start_vertex, end_vertex)
        self.assertEqual(total_cost, 37)
