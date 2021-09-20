from directed_graph import read_graph, create_random_graph
from errors import GraphException
from presentation import UI


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
