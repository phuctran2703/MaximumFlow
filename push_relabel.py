from collections import defaultdict, deque
import time
from graph import *

class PushRelabel:
    def __init__(self, graph):
        self.G = graph

    def initialize_residual_graph(self):
        """Khởi tạo đồ thị dư thừa từ đồ thị gốc với flow ban đầu khác 0."""
        for u in self.G:
            for v, edge in self.G[u].items():
                if edge.capacity > edge.flow:
                    self.residual_graph[u][v] = edge.capacity - edge.flow
                    self.residual_graph[v][u] = edge.capacity - edge.flow

    def initialize_preflow(self, source):
        """Khởi tạo tiền luồng từ đỉnh nguồn."""
        self.height = defaultdict(int)
        self.height[source] = len(self.residual_graph)
        for v, _ in self.residual_graph[source].items():
            flow = self.residual_graph[source][v]
            self.residual_graph[source][v] -= flow
            self.residual_graph[v][source] += flow
            self.excess[v] += flow
            self.excess[source] -= flow

            if v != source and self.excess[v] > 0:
                self.queue.append(v)  # Thêm đỉnh vào hàng đợi nếu có luồng dư thừa

    def push(self, u, v):
        """Đẩy luồng từ u đến v qua cạnh dư thừa."""
        delta = min(self.excess[u], self.residual_graph[u][v])
        self.residual_graph[u][v] -= delta
        self.residual_graph[v][u] += delta
        self.excess[u] -= delta
        self.excess[v] += delta

        if v != self.sink and self.excess[v] > 0 and v not in self.queue:
            self.queue.append(v)  # Thêm đỉnh v vào hàng đợi nếu nó có luồng dư thừa và chưa có trong hàng đợi

    def relabel(self, u):
        """Nâng nhãn độ cao của u."""
        min_height = float('inf')
        for v in self.residual_graph[u]:
            if self.residual_graph[u][v] > 0:
                min_height = min(min_height, self.height[v])
        self.height[u] = min_height + 1

    def discharge(self, u):
        """Xử lý đỉnh dư thừa u."""
        while self.excess[u] > 0:
            for v in self.residual_graph[u]:
                if self.residual_graph[u][v] > 0 and self.height[u] > self.height[v]:
                    self.push(u, v)
                    if self.excess[u] == 0:
                        break
            else:
                self.relabel(u)

    def find_max_flow(self, source, sink):
        """Tìm luồng cực đại từ source đến sink."""
        self.residual_graph = defaultdict(lambda: defaultdict(int))
        self.sink = sink
        self.height = defaultdict(int)
        self.excess = defaultdict(int)
        self.queue = deque()
        
        self.initialize_residual_graph()
        self.initialize_preflow(source)

        while self.queue:
            u = self.queue.popleft()
            self.discharge(u)
            # Nếu đỉnh u vẫn còn luồng dư thừa, đưa lại vào cuối hàng đợi
            if self.excess[u] > 0:
                self.queue.append(u)

        return self.excess[sink]

if __name__ == "__main__":
    graph = Graph()
    data = graph.load_data_from_excel("data/street_graph_data.xlsx")

    pr = PushRelabel(data)

    coordinates = [
        ("(10.8000091, 106.6606224)", "(10.7877414, 106.683245)"),
        ("(10.7881629, 106.6830814)", "(10.8226899, 106.7308992)"),
        ("(10.8394422, 106.6758107)", "(10.8190898, 106.7013338)"),
        ("(10.7898058, 106.6937982)", "(10.7768031, 106.6861427)"),
        ("(10.8012894, 106.6659545)", "(10.8003005, 106.6611255)")
    ]

    for source, sink in coordinates:
        start_time = time.time()
        result = pr.find_max_flow(source, sink)
        end_time = time.time()
        print(f"Max flow from {source} to {sink}: {result}")
        print("Duration:", end_time - start_time, "seconds")