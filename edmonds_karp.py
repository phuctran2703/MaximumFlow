from collections import deque, defaultdict
from graph import *

class EdmondsKarp:
    def __init__(self, graph):
        self.G = graph
        self.G_R = defaultdict(dict)
        self.F = defaultdict(lambda: defaultdict(int))
        self.flow_path = []

    def build_residual_graph(self):
        """Xây dựng đồ thị dư thừa G_R từ G với dung lượng cạnh"""
        for u in self.G:
            for v, edge in self.G[u].items():
                if v not in self.G_R[u]:
                    if edge.capacity > edge.flow:
                        self.G_R[u][v] = edge.capacity - edge.flow
                        self.G_R[v][u] = edge.capacity - edge.flow

    def bfs(self, S, T, parent):
        """Hàm tìm kiếm theo chiều rộng (BFS) để tìm đường tăng cường"""
        visited = set()
        queue = deque([S])
        visited.add(S)
        
        while queue:
            u = queue.popleft()
            
            for v in self.G_R[u]:
                if v not in visited and self.G_R[u][v] > 0:
                    queue.append(v)
                    visited.add(v)
                    parent[v] = u
                    if v == T:
                        return True
        return False

    def find_max_flow(self, S, T):
        """Tính luồng cực đại từ S đến T"""
        self.build_residual_graph()

        while True:
            parent = {}
            if not self.bfs(S, T, parent):
                break

            path = [T]
            cmin = float('inf')
            v = T

            while v != S:
                u = parent[v]
                cmin = min(cmin, self.G_R[u][v])
                v = u
                path.append(v)

            v = T
            while v != S:
                u = parent[v]
                self.F[u][v] += cmin
                self.F[v][u] += cmin
                self.G_R[u][v] -= cmin
                self.G_R[v][u] -= cmin

                if self.G_R[u][v] == 0:
                    del self.G_R[u][v]
                if self.G_R[v][u] == 0:
                    del self.G_R[v][u]
                v = u

            self.flow_path.append({"flow": cmin, "path": path[::-1]})
        
        # Tính tổng luồng cực đại từ S
        # fmax = sum(F[S][v] for v in F[S])

        return self.flow_path

if __name__ == "__main__":
    graph = Graph()
    data = graph.load_data_from_excel("data/street_graph_data.xlsx")
    ek = EdmondsKarp(data)
    flow_path = ek.find_max_flow("(10.774706, 106.6995506)","(10.7740726, 106.6990186)")
    print(flow_path)
    