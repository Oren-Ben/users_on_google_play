from LinkedList_from_class import LinkedList
from collections import deque
import json

def load_graph_from_json(file_name):
    try:
        with open(file_name + '.json', 'r') as file:
            data = json.load(file)
        return WeightedGraph.deserialize(data)
    except:
        print("Error while trying to open file")


def save_graph_to_json(graph_ob, file_name):
    with open(file_name + '.json', 'w') as my_file_write:
        d_file = graph_ob.serialize()
        json.dump(d_file, my_file_write)

class WeightedGraph:
    # O(V+E)
    def __init__(self, dict_list):
        self.dict_list = dict_list
        self.new_dict = {}
        for vertex in self.dict_list.keys():
            self.new_dict[vertex] = LinkedList()
            for next_vertex in self.dict_list[vertex]:
                self.new_dict[vertex].add_new_head(next_vertex)

    # O(V)
    def get_vertices(self):
        return list(self.new_dict.keys())

    # O(V+E)
    def get_edges(self):
        edges = []
        for vertex in self.new_dict:
            temp = self.new_dict[vertex].head
            while temp is not None:
                if {vertex, temp.data[0], temp.data[1]} not in edges:
                    edges.append({vertex, temp.data[0], temp.data[1]})
                temp = temp.next
        return edges

    # O(V+E)
    def delete_vertex(self, del_ver):
        for v in list(self.new_dict):
            if del_ver == v:
                del self.new_dict[v]
                break
        for v in list(self.new_dict):
            for edge in self.new_dict[v].create_list():
                if edge[0] == del_ver:
                    self.new_dict[v].delete_node(edge)

    # O(V+E)
    def add_vertex(self, ver, connections):
        if ver not in self.new_dict.keys():
            self.new_dict[ver] = LinkedList()
        new_connections = []
        exist_connection = []
        for connection in self.new_dict[ver].create_list():
            exist_connection.append(connection[0])
            print(exist_connection)
        for connection in connections:  # will add connection that not exist already
            if connection[0] in exist_connection:
                continue
            else:
                new_connections.append(connection)
        for connection in new_connections:
            if connection[0] not in self.new_dict.keys():  # if we get invalid edge we won't add it
                continue
            self.new_dict[ver].add_new_head(connection)
            self.new_dict[connection[0]].add_new_head([ver] + [connection[1]])

    # O(V+E)
    def BFS(self, start, goal):
        x = (start, [start])  # touple
        queue = deque()
        queue.append(x)  # enqueue X to queue
        new_results = []  # list for all paths
        while queue:  # not empty
            (vertex, path) = queue.popleft()
            temp = self.new_dict[vertex]
            if temp is None:
                return new_results
            else:
                exist_connection = []
                for next in temp.create_list():             # new  append all the connections that the vertex has
                    exist_connection.append(next[0])  # new
                for next in set(exist_connection) - set(path):  # new
                    if next == goal:
                        new_results.append(path + [next])
                    else:
                        queue.append((next, path + [next]))
        return new_results

        # O(V+E)
    def shortest_path(self, start, goal):
        all_paths = self.BFS(start, goal)
        if all_paths == []:  # no path exist
            return []
        else:
            weights = []
            for path in all_paths: # each path
                weight = 0
                for i in range(len(path)-1):
                    for edge in self.new_dict[path[i]].create_list():
                        if path[i+1] == edge[0]:
                            weight += edge[1]
                weights.append(weight)
            return all_paths[weights.index(min(weights))]  # map the path with the minimum weight


    def print_the_graph(self):
        for key in self.new_dict.keys():
            print(key + ": ", end="")
            self.new_dict[key].print_list()
            print('---')

    # O(V+E)
    def serialize(self):
        ser_dict = {}
        for vertex in self.new_dict.keys():
            temp = self.new_dict[vertex]
            ser_dict[vertex] = temp.create_list()
        return ser_dict

    # O(V+E)
    @staticmethod
    def deserialize(graph_for_dict):
        user_graph = WeightedGraph(graph_for_dict)
        return user_graph



x = load_graph_from_json('weighted_graph')  # contains deserialize
print('---BFS---')
print(x.BFS("Tel-Aviv", "Eilat"))
print('---shortest path---')
print(x.shortest_path("Tel-Aviv", "Eilat"))
print('---ver---')
print(x.get_vertices())
print('---edge---')
print(x.get_edges())
print('---delete Eilat---')
x.delete_vertex('Eilat')
print(x.print_the_graph())
print('---add Eilat ---')
x.add_vertex('Eilat',[['Tel-Aviv',0.13],['Tel aviv', 0.12]])
print(x.print_the_graph())
save_graph_to_json(x, "oren_test")
