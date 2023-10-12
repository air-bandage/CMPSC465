class Graph(object):
    def __init__(self, vertices=None, edges=None, undirected=False):
        if vertices is None:
            vertices = []
        if edges is None:
            edges = []
        self.vertices = vertices
        self.graph = {vertex: [] for vertex in vertices}
        for edge in edges:
            self.graph[edge[0]].append(edge[1])
            if undirected:
                self.graph[edge[1]].append(edge[0])

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, self.graph)

        # create a method to reverse a graph

    def reverse_graph(self):
        # create a Graph object that still has the same vertices
        reversal = Graph()
        reversal.graph = {vertex: [] for vertex in self.graph}
        # for each vertex, reverse the direction of edges with its connected vertices
        for vertex in self.graph:
            for connected_vertex in self.graph[vertex]:
                reversal.graph[connected_vertex].append(vertex)
        # return the reversed graph
        return reversal

    def explore_dfs(self, vertex):
        self.visited[vertex] = self.color
        self.pre[vertex] = self.count
        self.count += 1
        for connected_vertex in self.graph[vertex]:
            if self.visited[connected_vertex] == 0:
                self.explore_dfs(connected_vertex)
        self.post[vertex] = self.count
        self.count += 1
        # when a post order is assigned, add the vertex to the post order list,
        # so that the list must have vertices with post number in ascending order.
        self.post_order.append(vertex)

    def explore_bfs(self, vertex):
        self.visited[vertex] = self.color
        q = [vertex]
        self.pre[vertex] = self.count
        self.count += 1
        while q:
            processing_vertex = q.pop(0)
            self.post[processing_vertex] = self.count
            self.count += 1
            for connected_vertex in self.graph[processing_vertex]:
                if connected_vertex not in self.visited:
                    q.append(connected_vertex)
                    self.pre[connected_vertex] = self.count
                    self.count += 1
                    self.visited[connected_vertex] = self.color

    def dfs(self, order=None):
        # if no order is given for dfs, use the initialized order when creating the
        # graph
        if order is None:
            order = [vertex for vertex in self.graph]
        self.visited = {}
        self.pre = {}
        self.post = {}
        self.color = 1
        self.count = 1
        # initialize all unvisited vertices in the visiting dict
        for vertex in self.graph:
            self.visited[vertex] = 0
        # create a list that is going to store vertices in ascending post number order.
        self.post_order = []
        # visit all connected components
        for key in order:
            if self.visited[key] == 0:
                self.explore_dfs(key)
                self.color += 1

    def bfs(self):
        self.visited = {}
        self.pre = {}
        self.post = {}
        self.count = 1
        # for vertex in self.graph:
        #     self.visited[vertex]=0
        self.color = 1
        for key in self.graph:
            if key not in self.visited:
                self.explore_bfs(key)
                self.color += 1

    # find strongly connected components
    def scc(self):
        reversal = self.reverse_graph()  # reverse the order of original graph
        reversal.dfs()  # dfs reversal to get dfs order from ascending post numbers for further dfs
        # on original graph
        self.dfs(
            order=reversal.post_order[::-1]
        )  # dfs g1 by descending order of post number of the
        # vertices of the reversed graph
        return self.visited  # return the colored visited vertices

    def shortest_path(self, start):
        self.distfromS = {}
        for vertex in self.vertices:
            self.distfromS[vertex] = float("inf")
        self.distfromS[start] = 0
        q = [start]
        while q:
            processing_vertex = q.pop(0)
            for connected_vertex in self.graph[processing_vertex]:
                if self.distfromS[connected_vertex] == float("inf"):
                    q.append(connected_vertex)
                    self.distfromS[connected_vertex] = (
                            self.distfromS[processing_vertex] + 1
                    )


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

    def dijkstra_naive(self, start):
        self.dist = {}
        for vertex in self._vertices:
            self.dist[vertex] = float("inf")
        self.dist[start] = 0
        i = len(self._vertices)
        alarm = -1
        while i > 0:
            smallest = float("inf")
            smallest_v = self._vertices[0]
            for vertex in self._vertices:
                if alarm < self.dist[vertex] < smallest:
                    smallest = self.dist[vertex]
                    smallest_v = vertex
            for connected_vertex in self._graph[smallest_v]:
                if (self.dist[connected_vertex[0]] > self.dist[smallest_v] +
                        int(connected_vertex[1])):
                    self.dist[connected_vertex[0]] = (self.dist[smallest_v] +
                                                      int(connected_vertex[1]))
            alarm = self.dist[smallest_v]
            i -= 1

    def dijkstra(self):
        pass


def main():
    graph = WeightedGraph(path="./graph.in2", undirected=True)
    graph.dijkstra_naive("S")
    print(graph.dist)


if __name__ == "__main__":
    main()
