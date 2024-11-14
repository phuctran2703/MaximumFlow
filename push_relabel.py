from collections import defaultdict, deque
from graph import *

class PushRelabel:
    def __init__(self, graph):
        self.G = graph
        self.residual_graph = defaultdict(lambda: defaultdict(int))
        self.height = defaultdict(int)  # Nhãn độ cao
        self.excess = defaultdict(int)  # Luồng dư thừa
        self.queue = deque()  # Hàng đợi lưu các đỉnh dư thừa

    def initialize_residual_graph(self):
        """Khởi tạo đồ thị dư thừa từ đồ thị gốc với flow ban đầu khác 0."""
        for u in self.G:
            for v, edge in self.G[u].items():
                if edge.capacity > edge.flow:
                    self.residual_graph[u][v] = edge.capacity - edge.flow
                    self.residual_graph[v][u] = edge.capacity - edge.flow

    def initialize_preflow(self, source):
        """Khởi tạo tiền luồng từ đỉnh nguồn."""
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
        self.sink = sink
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
    ek = PushRelabel(data)
    flow_path = ek.find_max_flow("(10.8000091, 106.6606224)","(10.7999075, 106.6605181)")
    print(flow_path)