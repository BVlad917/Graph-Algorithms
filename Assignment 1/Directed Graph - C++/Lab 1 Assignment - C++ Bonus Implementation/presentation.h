//
// Created by VladB on 20-Mar-21.
//

#ifndef LAB_1_ASSIGNMENT___C___BONUS_IMPLEMENTATION_PRESENTATION_H
#define LAB_1_ASSIGNMENT___C___BONUS_IMPLEMENTATION_PRESENTATION_H


#include "DirectedGraph.h"

class UI {
private:
    DirectedGraph &graph;

    static void print_menu();

    void ui_get_number_of_vertices();

    void ui_get_number_of_edges();

    void ui_get_vertices();

    void ui_get_edges();

    void ui_check_vertex();

    void ui_check_edge();

    void ui_get_cost_of_edge();

    void ui_in_degree_of_vertex();

    void ui_out_degree_of_vertex();

    void ui_outbound_neighbours();

    void ui_inbound_neighbours();

    void ui_change_edge_cost();

    void ui_add_edge();

    void ui_remove_edge();

    void ui_add_vertex();

    void ui_remove_vertex();

    void ui_write_graph_to_file();

public:
    explicit UI(DirectedGraph &graph);

    void run_app();
};


#endif //LAB_1_ASSIGNMENT___C___BONUS_IMPLEMENTATION_PRESENTATION_H
