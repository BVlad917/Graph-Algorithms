import unittest

from directed_graph import read_graph, create_random_graph, write_graph, TripleDictGraph
from errors import GraphException


class TestTripleDictGraph(unittest.TestCase):
    def test_read_graph(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_vertices(), 5)
        self.assertEqual(graph.get_no_edges(), 6)
        out_neighbours_with_cost = []
        for out_neighbour, cost in graph.get_outbound_neighbours_with_cost(0):
            out_neighbours_with_cost.append((out_neighbour, cost))
        self.assertEqual(len(out_neighbours_with_cost), 2)
        out_neighbours_with_cost.clear()

        for out_neighbour, cost in graph.get_outbound_neighbours_with_cost(1):
            out_neighbours_with_cost.append((out_neighbour, cost))
        self.assertEqual(len(out_neighbours_with_cost), 2)
        out_neighbours_with_cost.clear()

        for out_neighbour, cost in graph.get_outbound_neighbours_with_cost(2):
            out_neighbours_with_cost.append((out_neighbour, cost))
        self.assertEqual(len(out_neighbours_with_cost), 2)
        out_neighbours_with_cost.clear()

        for out_neighbour, cost in graph.get_outbound_neighbours_with_cost(3):
            out_neighbours_with_cost.append((out_neighbour, cost))
        self.assertEqual(len(out_neighbours_with_cost), 0)
        out_neighbours_with_cost.clear()

        for out_neighbour, cost in graph.get_outbound_neighbours_with_cost(4):
            out_neighbours_with_cost.append((out_neighbour, cost))
        self.assertEqual(len(out_neighbours_with_cost), 0)

    def test_get_no_vertices(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_vertices(), 5)

    def test_get_no_edges(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_edges(), 6)

    def test_get_all_vertices(self):
        graph = read_graph("test_in_graph.txt")
        expected_vertices = [0, 1, 2, 3, 4]
        for index, vertex in enumerate(graph.get_all_vertices()):
            self.assertEqual(vertex, expected_vertices[index])

    def test_get_all_edges(self):
        graph = read_graph("test_in_graph.txt")
        all_edges_with_cost = []
        expected_all_edges_with_cost = [(0, 0, 1), (0, 1, 7), (1, 2, 2), (2, 1, -1), (1, 3, 8), (2, 3, 5)]
        for _from, _to, _cost in graph.get_all_edges():
            all_edges_with_cost.append((_from, _to, _cost))
        self.assertEqual(all_edges_with_cost, expected_all_edges_with_cost)
        # self.assertEqual(graph.get_all_edges(), [(0, 0, 1), (0, 1, 7), (1, 2, 2), (2, 1, -1), (1, 3, 8), (2, 3, 5)])

    def test_get_cost_of_edge(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_cost_of_edge(0, 0), 1)
        self.assertEqual(graph.get_cost_of_edge(1, 2), 2)
        self.assertEqual(graph.get_cost_of_edge(1, 3), 8)
        self.assertRaises(GraphException, graph.get_cost_of_edge, 1, 4)

    def test_check_edge(self):
        graph = read_graph("test_in_graph.txt")
        self.assertTrue(graph.is_edge_in_graph(0, 0))
        self.assertTrue(graph.is_edge_in_graph(0, 1))
        self.assertTrue(graph.is_edge_in_graph(1, 3))
        self.assertFalse(graph.is_edge_in_graph(1, 4))

    def test_check_vertex(self):
        graph = read_graph("test_in_graph.txt")
        self.assertTrue(graph.is_vertex_in_graph(0))
        self.assertTrue(graph.is_vertex_in_graph(1))
        self.assertTrue(graph.is_vertex_in_graph(4))
        self.assertFalse(graph.is_vertex_in_graph(7))

    def test_get_in_degree(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_in_degree(0), 1)
        self.assertEqual(graph.get_in_degree(1), 2)
        self.assertEqual(graph.get_in_degree(4), 0)

    def test_get_out_degree(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_out_degree(0), 2)
        self.assertEqual(graph.get_out_degree(1), 2)
        self.assertEqual(graph.get_out_degree(4), 0)

    def test_get_outbound_neighbours(self):
        graph = read_graph("test_in_graph.txt")
        list_of_neighbours = []
        for x in graph.get_outbound_neighbours(1):
            list_of_neighbours.append(x)
        self.assertEqual(list_of_neighbours, [2, 3])
        list_of_neighbours.clear()
        for x in graph.get_outbound_neighbours(2):
            list_of_neighbours.append(x)
        self.assertEqual(list_of_neighbours, [1, 3])
        list_of_neighbours.clear()
        for x in graph.get_outbound_neighbours(4):
            list_of_neighbours.append(x)
        self.assertEqual(list_of_neighbours, [])
        self.assertTrue(graph.get_out_degree(4) == 0)

    def test_get_inbound_neighbours(self):
        graph = read_graph("test_in_graph.txt")
        list_of_neighbours = []
        for x in graph.get_inbound_neighbours(1):
            list_of_neighbours.append(x)
        self.assertEqual(list_of_neighbours, [0, 2])
        list_of_neighbours.clear()
        for x in graph.get_inbound_neighbours(2):
            list_of_neighbours.append(x)
        self.assertEqual(list_of_neighbours, [1])
        list_of_neighbours.clear()
        for x in graph.get_inbound_neighbours(4):
            list_of_neighbours.append(x)
        self.assertEqual(list_of_neighbours, [])
        self.assertTrue(graph.get_in_degree(4) == 0)

    def test_get_outbound_neighbours_with_cost(self):
        graph = read_graph("test_in_graph.txt")
        info = []
        for neighbour_and_cost in graph.get_outbound_neighbours_with_cost(1):
            info.append(neighbour_and_cost)
        self.assertEqual(info, [(2, 2), (3, 8)])
        info.clear()
        for neighbour_and_cost in graph.get_outbound_neighbours_with_cost(2):
            info.append(neighbour_and_cost)
        self.assertEqual(info, [(1, -1), (3, 5)])
        info.clear()
        for neighbour_and_cost in graph.get_outbound_neighbours_with_cost(4):
            info.append(neighbour_and_cost)
        self.assertEqual(info, [])
        info.clear()
        self.assertTrue(graph.get_out_degree(4) == 0)

    def test_get_inbound_neighbours_with_cost(self):
        graph = read_graph("test_in_graph.txt")
        info = []
        for neighbour_and_cost in graph.get_inbound_neighbours_with_cost(1):
            info.append(neighbour_and_cost)
        self.assertEqual(info, [(0, 7), (2, -1)])
        info.clear()
        for neighbour_and_cost in graph.get_inbound_neighbours_with_cost(2):
            info.append(neighbour_and_cost)
        self.assertEqual(info, [(1, 2)])
        info.clear()
        for neighbour_and_cost in graph.get_inbound_neighbours_with_cost(4):
            info.append(neighbour_and_cost)
        self.assertEqual(info, [])
        info.clear()
        self.assertTrue(graph.get_in_degree(4) == 0)

    def test_get_all_info_outbound_neighbours(self):
        graph = read_graph("test_in_graph.txt")
        info_list = []
        for x in graph.get_outbound_neighbours(1):
            info_list.append((x, graph.get_cost_of_edge(1, x)))
        self.assertEqual(info_list, [(2, 2), (3, 8)])
        info_list.clear()
        for x in graph.get_outbound_neighbours(2):
            info_list.append((x, graph.get_cost_of_edge(2, x)))
        self.assertEqual(info_list, [(1, -1), (3, 5)])
        info_list.clear()
        for x in graph.get_outbound_neighbours(4):
            info_list.append((x, graph.get_cost_of_edge(4, x)))
        self.assertEqual(info_list, [])

    def test_get_all_info_inbound_neighbours(self):
        graph = read_graph("test_in_graph.txt")
        info_list = []
        for x in graph.get_inbound_neighbours(1):
            info_list.append((x, graph.get_cost_of_edge(x, 1)))
        self.assertEqual(info_list, [(0, 7), (2, -1)])
        info_list.clear()
        for x in graph.get_inbound_neighbours(2):
            info_list.append((x, graph.get_cost_of_edge(x, 2)))
        self.assertEqual(info_list, [(1, 2)])
        info_list.clear()
        for x in graph.get_inbound_neighbours(4):
            info_list.append((x, graph.get_cost_of_edge(x, 4)))
        self.assertEqual(info_list, [])

    def test_change_edge_cost(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_cost_of_edge(1, 2), 2)
        graph.change_edge_cost(1, 2, 10)
        self.assertEqual(graph.get_cost_of_edge(1, 2), 10)

    def test_add_edge(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_edges(), 6)
        self.assertFalse(graph.is_edge_in_graph(1, 4))
        graph.add_edge(1, 4, 10)
        self.assertTrue(graph.is_edge_in_graph(1, 4))
        self.assertEqual(graph.get_no_edges(), 7)
        self.assertTrue(graph.is_edge_in_graph(1, 4))
        self.assertEqual(graph.get_cost_of_edge(1, 4), 10)
        self.assertRaises(GraphException, graph.add_edge, 1, 4, 20)

    def test_remove_edge(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_edges(), 6)
        self.assertTrue(graph.is_edge_in_graph(1, 2))
        graph.remove_edge(1, 2)
        self.assertFalse(graph.is_edge_in_graph(1, 2))
        self.assertEqual(graph.get_no_edges(), 5)
        self.assertFalse(graph.is_edge_in_graph(1, 2))
        self.assertRaises(GraphException, graph.remove_edge, 1, 2)

    def test_add_vertex(self):
        graph = read_graph("test_in_graph.txt")
        self.assertEqual(graph.get_no_vertices(), 5)
        self.assertFalse(graph.is_vertex_in_graph(5))
        graph.add_vertex(5)
        self.assertTrue(graph.is_vertex_in_graph(5))
        self.assertEqual(graph.get_no_vertices(), 6)
        self.assertEqual(graph.get_out_degree(5), 0)
        self.assertEqual(graph.get_in_degree(5), 0)
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
        self.assertNotIn(3, graph.get_outbound_neighbours(0))
        self.assertNotIn(3, graph.get_outbound_neighbours(1))
        self.assertNotIn(3, graph.get_outbound_neighbours(2))
        self.assertNotIn(3, graph.get_outbound_neighbours(4))
        self.assertNotIn(3, graph.get_inbound_neighbours(0))
        self.assertNotIn(3, graph.get_inbound_neighbours(1))
        self.assertNotIn(3, graph.get_inbound_neighbours(2))
        self.assertNotIn(3, graph.get_inbound_neighbours(4))
        all_edges_with_cost = []
        for _from, _to, _cost in graph.get_all_edges():
            all_edges_with_cost.append((_from, _to, _cost))
        self.assertNotIn(3, [triplet[0] for triplet in all_edges_with_cost])
        self.assertNotIn(3, [triplet[1] for triplet in all_edges_with_cost])

    def test_dijkstra(self):
        graph = TripleDictGraph()
        graph.add_vertex(1)
        graph.add_vertex(2)
        graph.add_vertex(3)
        graph.add_vertex(4)
        graph.add_vertex(5)
        graph.add_vertex(6)
        graph.add_edge(1, 2, 50)
        graph.add_edge(1, 3, 45)
        graph.add_edge(1, 4, 10)
        graph.add_edge(2, 3, 10)
        graph.add_edge(2, 4, 15)
        graph.add_edge(3, 5, 30)
        graph.add_edge(4, 1, 10)
        graph.add_edge(4, 5, 15)
        graph.add_edge(5, 2, 20)
        graph.add_edge(5, 3, 35)
        graph.add_edge(6, 5, 3)

        walk = graph.reverse_dijkstra(1, 4)
        cost = 0
        for first, second in zip(walk, walk[1:]):
            cost += graph.get_cost_of_edge(first, second)
        self.assertEqual(walk, [1, 4])
        self.assertEqual(cost, 10)

        walk = graph.reverse_dijkstra(1, 5)
        cost = 0
        for first, second in zip(walk, walk[1:]):
            cost += graph.get_cost_of_edge(first, second)
        self.assertEqual(walk, [1, 4, 5])
        self.assertEqual(cost, 25)

        walk = graph.reverse_dijkstra(1, 2)
        cost = 0
        for first, second in zip(walk, walk[1:]):
            cost += graph.get_cost_of_edge(first, second)
        self.assertEqual(walk, [1, 4, 5, 2])
        self.assertEqual(cost, 45)

        walk = graph.reverse_dijkstra(1, 3)
        cost = 0
        for first, second in zip(walk, walk[1:]):
            cost += graph.get_cost_of_edge(first, second)
        self.assertEqual(walk, [1, 3])
        self.assertEqual(cost, 45)

        self.assertRaises(GraphException, graph.reverse_dijkstra, 1, 6)

    def test_simple_dijkstra(self):
        g = TripleDictGraph()
        g.add_vertex(0)
        g.add_vertex(1)
        g.add_vertex(2)
        g.add_vertex(3)
        g.add_edge(0, 1, 4)
        g.add_edge(1, 2, 3)
        g.add_edge(0, 2, 9)
        walk = g.reverse_dijkstra(0, 2)
        self.assertEqual(walk, [0, 1, 2])

    def test_second_time_dijkstra(self):
        g = TripleDictGraph()
        g.add_vertex(0)
        g.add_vertex(1)
        g.add_vertex(2)
        g.add_vertex(3)
        g.add_vertex(4)
        g.add_vertex(5)
        g.add_edge(0, 1, 3)
        g.add_edge(0, 2, 4)
        g.add_edge(1, 2, 6)
        g.add_edge(1, 3, 2)
        g.add_edge(1, 4, 7)
        g.add_edge(2, 4, 5)
        g.add_edge(3, 4, 1)
        g.add_edge(3, 5, 8)
        g.add_edge(4, 5, 4)
        walk = g.reverse_dijkstra(0, 5)
        self.assertEqual(walk, [0, 1, 3, 4, 5])
        self.assertEqual(g.calculate_walk_cost(walk), 10)
        walk = g.reverse_dijkstra(0, 4)
        self.assertEqual(walk, [0, 1, 3, 4])
        self.assertEqual(g.calculate_walk_cost(walk), 6)
        walk = g.reverse_dijkstra(0, 3)
        self.assertEqual(walk, [0, 1, 3])
        self.assertEqual(g.calculate_walk_cost(walk), 5)

    def test_exist_negative_cost_cycles(self):
        graph = TripleDictGraph(5)
        graph.add_edge(0, 1, -1)
        graph.add_edge(0, 2, 4)
        graph.add_edge(1, 2, 3)
        graph.add_edge(1, 3, 2)
        graph.add_edge(1, 4, 2)
        graph.add_edge(3, 2, 5)
        graph.add_edge(3, 1, 1)
        graph.add_edge(4, 3, -3)
        self.assertFalse(graph.exist_negative_cost_cycles(0))
        graph = TripleDictGraph(4)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, -1)
        graph.add_edge(2, 3, -1)
        graph.add_edge(3, 0, -1)
        self.assertTrue(graph.exist_negative_cost_cycles(0))

    def test_bellman(self):
        graph = TripleDictGraph(5)
        graph.add_edge(0, 1, -1)
        graph.add_edge(0, 2, 4)
        graph.add_edge(1, 2, 3)
        graph.add_edge(1, 3, 2)
        graph.add_edge(1, 4, 2)
        graph.add_edge(3, 2, 5)
        graph.add_edge(3, 1, 1)
        graph.add_edge(4, 3, -3)

        walk = graph.bellman(0, 1)
        cost = 0
        for first, second in zip(walk, walk[1:]):
            cost += graph.get_cost_of_edge(first, second)
        self.assertEqual(walk, [0, 1])
        self.assertEqual(cost, -1)

        walk = graph.bellman(0, 2)
        cost = 0
        for first, second in zip(walk, walk[1:]):
            cost += graph.get_cost_of_edge(first, second)
        self.assertEqual(walk, [0, 1, 2])
        self.assertEqual(cost, 2)

        walk = graph.bellman(0, 3)
        cost = 0
        for first, second in zip(walk, walk[1:]):
            cost += graph.get_cost_of_edge(first, second)
        self.assertEqual(walk, [0, 1, 4, 3])
        self.assertEqual(cost, -2)

        walk = graph.bellman(0, 4)
        cost = 0
        for first, second in zip(walk, walk[1:]):
            cost += graph.get_cost_of_edge(first, second)
        self.assertEqual(walk, [0, 1, 4])
        self.assertEqual(cost, 1)

    def test_second_time_bellman(self):
        g = TripleDictGraph()
        g.add_vertex(0)
        g.add_vertex(1)
        g.add_vertex(2)
        g.add_vertex(3)
        g.add_vertex(4)
        g.add_vertex(5)
        g.add_edge(0, 1, 3)
        g.add_edge(0, 2, 4)
        g.add_edge(1, 2, 6)
        g.add_edge(1, 3, 2)
        g.add_edge(1, 4, 7)
        g.add_edge(2, 4, 5)
        g.add_edge(3, 4, 1)
        g.add_edge(3, 5, 8)
        g.add_edge(4, 5, 4)
        walk = g.bellman(0, 5)
        self.assertEqual(walk, [0, 1, 3, 4, 5])
        self.assertEqual(g.calculate_walk_cost(walk), 10)
        walk = g.bellman(0, 4)
        self.assertEqual(walk, [0, 1, 3, 4])
        self.assertEqual(g.calculate_walk_cost(walk), 6)
        walk = g.bellman(0, 3)
        self.assertEqual(walk, [0, 1, 3])
        self.assertEqual(g.calculate_walk_cost(walk), 5)

    def test_bellman_with_negative_costs(self):
        g = TripleDictGraph()
        g.add_vertex(0)
        g.add_vertex(1)
        g.add_vertex(2)
        g.add_vertex(3)
        g.add_vertex(4)
        g.add_vertex(5)
        g.add_edge(0, 1, 4)
        g.add_edge(0, 3, 3)
        g.add_edge(1, 2, 5)
        g.add_edge(1, 4, 4)
        g.add_edge(2, 1, 5)
        g.add_edge(2, 5, -2)
        g.add_edge(3, 0, 4)
        g.add_edge(3, 4, 3)
        g.add_edge(4, 1, -3)
        g.add_edge(4, 3, 3)
        g.add_edge(4, 5, 2)
        g.add_edge(5, 2, 4)
        walk = g.bellman(0, 5)
        self.assertEqual(walk, [0, 3, 4, 1, 2, 5])
        self.assertEqual(g.calculate_walk_cost(walk), 6)

    def test_count_walks_of_minimum_cost(self):
        # Just one shortest walk from 0 to 2 in the below graph
        g = TripleDictGraph()
        g.add_vertex(0)
        g.add_vertex(1)
        g.add_vertex(2)
        g.add_vertex(3)
        g.add_edge(0, 1, 4)
        g.add_edge(1, 2, 3)
        g.add_edge(0, 2, 9)
        self.assertEqual(g.count_walks_of_minimum_cost(0, 2), 1)
        # Modified the above graph by changing the cost of the edge 0->2 to 7, so now there are 2 shortest walks
        g = TripleDictGraph()
        g.add_vertex(0)
        g.add_vertex(1)
        g.add_vertex(2)
        g.add_vertex(3)
        g.add_edge(0, 1, 4)
        g.add_edge(1, 2, 3)
        g.add_edge(0, 2, 7)
        self.assertEqual(g.count_walks_of_minimum_cost(0, 2), 2)
        # The graph used for testing Dijkstra and Bellman-Ford. It has just one shortest walk from 0 to 5
        g = TripleDictGraph()
        g.add_vertex(0)
        g.add_vertex(1)
        g.add_vertex(2)
        g.add_vertex(3)
        g.add_vertex(4)
        g.add_vertex(5)
        g.add_edge(0, 1, 4)
        g.add_edge(0, 3, 3)
        g.add_edge(1, 2, 5)
        g.add_edge(1, 4, 4)
        g.add_edge(2, 1, 5)
        g.add_edge(2, 5, -2)
        g.add_edge(3, 0, 4)
        g.add_edge(3, 4, 3)
        g.add_edge(4, 1, -3)
        g.add_edge(4, 3, 3)
        g.add_edge(4, 5, 2)
        g.add_edge(5, 2, 4)
        g.add_vertex(6)
        self.assertEqual(g.count_walks_of_minimum_cost(0, 5), 1)
        # Modified the above graph by adding a new vertex and 2 edges in such a way that now there are 2 shortest
        # walks from 0 to 5
        g = TripleDictGraph()
        g.add_vertex(0)
        g.add_vertex(1)
        g.add_vertex(2)
        g.add_vertex(3)
        g.add_vertex(4)
        g.add_vertex(5)
        g.add_edge(0, 1, 4)
        g.add_edge(0, 3, 3)
        g.add_edge(1, 2, 5)
        g.add_edge(1, 4, 4)
        g.add_edge(2, 1, 5)
        g.add_edge(2, 5, -2)
        g.add_edge(3, 0, 4)
        g.add_edge(3, 4, 3)
        g.add_edge(4, 1, -3)
        g.add_edge(4, 3, 3)
        g.add_edge(4, 5, 2)
        g.add_edge(5, 2, 4)
        g.add_vertex(6)
        g.add_edge(0, 6, -3)
        g.add_edge(6, 5, 9)
        self.assertEqual(g.count_walks_of_minimum_cost(0, 5), 2)

    def test_get_copy_of_graph(self):
        graph = read_graph("test_in_graph.txt")
        copy = graph.get_copy_of_graph()
        copy.add_vertex(5)
        self.assertEqual(graph.get_no_vertices(), 5)
        self.assertEqual(copy.get_no_vertices(), 6)
        self.assertNotIn(5, graph.get_all_vertices())
        self.assertIn(5, copy.get_all_vertices())
        copy.add_edge(1, 5, 20)
        self.assertEqual(copy.get_no_edges(), 7)
        self.assertEqual(graph.get_no_edges(), 6)
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
