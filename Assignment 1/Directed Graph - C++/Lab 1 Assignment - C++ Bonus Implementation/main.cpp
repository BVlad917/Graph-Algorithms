#include <iostream>
#include "tests.h"
#include "DirectedGraph.h"
#include "utils.h"
#include "presentation.h"

int main() {
    run_all_tests();
    char cmd[256];
    int cmd_as_int;
    DirectedGraph graph;

    std::cout << "Read the graph from a file or generate the graph randomly?\n"
                 "1 - Read the graph from a file\n"
                 "2 - Generate a random graph\n";
    std::cout << "What's your wish: ";

    std::cin.getline(cmd, sizeof(cmd));
    cmd_as_int = atoi(cmd);

    if (cmd_as_int == 1) {
        char file_name[256];
        std::cout << "\nGive the name of the file (with extension): ";
        std::cin.getline(file_name, sizeof(file_name));
        graph = read_graph_from_file(file_name);
    } else if (cmd_as_int == 2) {
        int nr_vertices, nr_edges;
        std::cout << "\nGive the number of vertices: ";
        std::cin >> nr_vertices;
        std::cout << "\nGive the number of edges: ";
        std::cin >> nr_edges;
        try {
            graph = generate_random_graph(nr_vertices, nr_edges);
        }
        catch (std::exception&) {
            std::cout << "\nError! Too many edges given!\n";
            return 0;
        }
    } else {
        std::cout << "\nInvalid command given.\n";
        return 0;
    }

    UI ui = UI(graph);
    ui.run_app();
    std::cout << "\nHave a great day!\n";

    return 0;
}
