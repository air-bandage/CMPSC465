#!/home/davocado/miniconda3/envs/default/bin/python
import timeit
import PriorityQueue


# create an object "Graph", with a dictionary of vertices and corresponding edges
# as attribute, and methods "explore()", "reverse()", and "dfs()"
class Graph(object):
    def __init__(self, path=None, vertices=None, edges=None):
        if path is not None:
            with open(path) as f:
                vertices = f.readline().strip().split(", ")
                edges = [line.split(", ") for line in f.read().strip().split("\n")]
        if vertices is None:
            vertices = []
        if edges is None:
            edges = []
        self._vertices = vertices
        self._graph = {vertex: [] for vertex in vertices}
        for edge in edges:
            self._graph[edge[0]].append(edge[1])

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, self._graph)

    # define a Graph object for reserved original graph with its dictionary
    # attribute, for each vertex in the original, reverse the direction of
    # edge with its corresponding vertices, and return the reversed Graph.
    def reverse(self):
        self_reversed = Graph()
        self_reversed._graph = {vertex: [] for vertex in self._graph}
        for vertex in self._graph:
            for connected_vertex in self._graph[vertex]:
                self_reversed._graph[connected_vertex].append(vertex)
        return self_reversed

    def explore(self, vertex):
        self._visited[vertex] = self._color  # color the visited vertex
        self._pre[vertex] = self._cnt  # assign a pre number to the vertex
        self._cnt += 1  # the pre number for the next visited vertex
        # for all vertices in this connected component, if it is not visited, color it,
        # and assign pre- and post-number to it.
        for connected_vertex in self._graph[vertex]:
            if self._visited[connected_vertex] == 0:
                self.explore(connected_vertex)
        self._post[
            vertex
        ] = self._cnt  # after all the vertices are visited in this component,
        # assign post numbers to each of them backwards
        self._cnt += 1  # post number for the next vertex
        self._post_order.append(vertex)
        return 0

    # deep first search all vertices
    def dfs(self, order=None):
        # initialize the parameter order in the order of vertex initialized if not
        # assigned
        if order is None:
            order = [vertex for vertex in self._graph]
        # initialize a dictionary for storing vertices labeled with their color
        # color is for identifying different trees they belong to
        self._visited = {}
        # initialize a dictionary for storing pre- and post-number of the vertices
        self._pre = {}
        self._post = {}
        # initialize vertices with 'unvisited' value color
        for vertex in self._graph:
            self._visited[vertex] = 0
        self._color = 1  # define a color
        self._cnt = 1  # count for pre- and post-numbers
        # for all vertices in the graph, if it is unvisited, visited this vertex as root
        # and all vertices that connected to this vertex one by one until the end of
        # this tree and change to another color for the next tree after visited all the
        # vertices, return the dictionaries of their colors, pre numbers, and post
        # numbers respectively.
        self._post_order = []
        for vertex in order:
            if self._visited[vertex] == 0:
                self.explore(vertex)
                self._color += 1
        return 0

    def find_scc(self):
        self_reversed = self.reverse()
        self_reversed.dfs()
        self.dfs(order=self_reversed._post_order[::-1])
        self._scc = self._visited
        return 0

    @property
    def scc(self):
        return self._scc


class WeightedGraph(object):
    def __init__(self, path=None, vertices=None, edges=None, undirected=False):
        if path is not None:
            with open(path) as f:
                vertices = f.readline().strip().split(", ")
                edges = [line.split(", ") for line in f.read().strip().split("\n")]
        if vertices is None:
            vertices = []
        if edges is None:
            edges = []
        self._vertices = vertices
        self._graph = {vertex: [] for vertex in vertices}
        for edge in edges:
            self._graph[edge[0]].append((edge[1], int(edge[2])))
            if undirected:
                self._graph[edge[1]].append((edge[0], int(edge[2])))

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, self._graph)

    @property
    def dist(self):
        return self._dist

    def dijkstra_naive(self, source):
        self._dist = {vertex: float("Inf") for vertex in self._vertices}
        self._dist[source] = 0
        clock = 0
        for _ in range(len(self._vertices)):
            next_vertex = source
            next_alarm = float("Inf")
            for vertex in self._vertices:
                if self._dist[vertex] > clock and self._dist[vertex] < next_alarm:
                    next_vertex = vertex
                    next_alarm = self._dist[vertex]
            clock = self._dist[next_vertex]
            for connected_vertex in self._graph[next_vertex]:
                if (
                    self._dist[connected_vertex[0]]
                    > self._dist[next_vertex] + connected_vertex[1]
                ):
                    self._dist[connected_vertex[0]] = (
                        self._dist[next_vertex] + connected_vertex[1]
                    )
        return 0

    def dijkstra(self, source):
        self._dist = {vertex: float("Inf") for vertex in self._vertices}
        self._dist[source] = 0
        self._pre = {}
        pq_list = [(self._dist[v], v) for v in self._vertices]
        pq = PriorityQueue.PriorityQueue(pq_list)
        for _ in range(len(self._vertices)):
            vertex = pq.pop(0)[1]
            for connected_vertex in self._graph[vertex]:
                if (
                    self._dist[connected_vertex[0]]
                    > self._dist[vertex] + connected_vertex[1]
                ):
                    self._dist[connected_vertex[0]] = (
                        self._dist[vertex] + connected_vertex[1]
                    )
                    pq.decrease_priority(
                        pq.pos(connected_vertex[0]), self._dist[connected_vertex[0]]
                    )
                    self._pre[connected_vertex[0]] = vertex
        return 0


def main():
    path = "../graph/graph.in2"
    graph = WeightedGraph(path=path, undirected=True)
    print(graph)
    graph.dijkstra_naive("S")
    print(graph.dist)
    graph.dijkstra("S")
    print(graph.dist)


if __name__ == "__main__":
    main()
    # d = timeit.timeit("main()", number=10)
    # print(d)
