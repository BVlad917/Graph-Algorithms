from directed_graph import read_graph, create_random_graph
from errors import GraphException
from presentation import UI

"""
The files graph1k.txt, graph10k.txt, graph100k.txt, and graph1m.txt were downloaded from the assignment page
and were used to test the program (i.e., to see if the program can work with such large inputs). Although it is
a little bit slow for the 1m graph, it is acceptable. After testing the operations on these files new files 
called *_modif.txt were saved, each corresponding to one of the testing files.
graph1k.txt - 
graph10k.txt - 
graph100k.txt -
graph1m.txt - 

The files test_in_graph.txt and test_out_graph.txt were used in the testing module.
"""


def run():
    print("Read the graph from a file of generate a random graph?\n"
          "1 - Read the graph from a file\n"
          "2 - Generate a random graph\n")
    cmd = input("Choice: ").strip()
    if cmd == '1':
        file_name = input("Give the name of the file (with extension): ")
        graph = read_graph(file_name)
    elif cmd == '2':
        vertices = int(input("How many vertices do you want the graph to have: "))
        edges = int(input("How many edges do you want the graph to have: "))
        try:
            graph = create_random_graph(vertices, edges)
        except GraphException as ge:
            print(str(ge))
            return
    else:
        print("Invalid choice.")
        return

    ui = UI(graph)
    ui.start()
    print("Have a great day!")


if __name__ == '__main__':
    run()
