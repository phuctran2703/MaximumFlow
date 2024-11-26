from collections import deque, defaultdict
from graph import *
import time

class Dinic:
    def __init__(self, graph):
        self.G = graph

    def build_residual_graph(self):
        """Builds the residual graph G_R from G with edge capacities."""
        self.G_R = defaultdict(dict)
        for u in self.G:
            for v, edge in self.G[u].items():
                if edge.capacity > edge.flow:
                    self.G_R[u][v] = edge.capacity - edge.flow
                if edge.flow > 0:
                    self.G_R[v][u] = edge.flow

    def bfs(self, S, T):
        """Performs BFS to build the level graph."""
        self.level = {node: -1 for node in self.G_R}
        queue = deque([S])
        self.level[S] = 0

        while queue:
            u = queue.popleft()
            for v in self.G_R[u]:
                if self.level[v] == -1 and self.G_R[u][v] > 0:
                    self.level[v] = self.level[u] + 1
                    queue.append(v)

        return self.level[T] != -1

    def dfs(self, u, T, flow):
        """Performs DFS to find a blocking flow."""
        if u == T:
            return flow

        for v in list(self.G_R[u].keys()):
            if self.level[v] == self.level[u] + 1 and self.G_R[u][v] > 0:
                min_flow = min(flow, self.G_R[u][v])
                result = self.dfs(v, T, min_flow)
                if result > 0:
                    self.G_R[u][v] -= result
                    self.G_R[v][u] += result
                    return result

        return 0

    def find_max_flow(self, S, T):
        """Computes the maximum flow from S to T."""
        self.build_residual_graph()
        max_flow = 0
        self.flow_path = []

        while self.bfs(S, T):
            while True:
                flow = self.dfs(S, T, float('inf'))
                if flow == 0:
                    break
                max_flow += flow

        return max_flow, self.flow_path


if __name__ == "__main__":
    graph = Graph()
    data = graph.load_data_from_excel("data/street_graph_data.xlsx")

    dinic = Dinic(data)

    coordinates = [
        ("(10.8000091, 106.6606224)", "(10.7877414, 106.683245)"),
        ("(10.7881629, 106.6830814)", "(10.8226899, 106.7308992)"),
        ("(10.8394422, 106.6758107)", "(10.8190898, 106.7013338)"),
        ("(10.7898058, 106.6937982)", "(10.7768031, 106.6861427)"),
        ("(10.8012894, 106.6659545)", "(10.8003005, 106.6611255)")
    ]

    for start, end in coordinates:
        start_time = time.time()
        result, _ = dinic.find_max_flow(start, end)
        end_time = time.time()
        print(f"Max flow from {start} to {end}: {result}")
        print("Duration:", end_time - start_time, "seconds")