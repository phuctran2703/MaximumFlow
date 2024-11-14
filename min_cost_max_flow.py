from collections import defaultdict, deque
import heapq
import time
from graph import *

class MinCostMaxFlow:
    def __init__(self, graph):
        self.graph = graph
        self.adj_matrix = graph.adj_matrix
        self.inf = float('inf')

    def find_shortest_path(self, source, sink, potential):
        dist = defaultdict(lambda: self.inf)
        parent = {}  # To reconstruct path
        dist[source] = 0
        priority_queue = [(0, source)]  # (cost, node)
        
        while priority_queue:
            current_dist, u = heapq.heappop(priority_queue)
            if current_dist > dist[u]:
                continue
            
            for v in self.adj_matrix[u]:
                edge = self.adj_matrix[u][v]
                if edge and edge.flow < edge.capacity:  # If there's remaining capacity
                    reduced_cost = edge.distance + potential[u] - potential[v]
                    if dist[v] > dist[u] + reduced_cost:
                        dist[v] = dist[u] + reduced_cost
                        parent[v] = u
                        heapq.heappush(priority_queue, (dist[v], v))
        
        # Return distance to sink and the path
        path = []
        if sink in parent:
            v = sink
            while v != source:
                path.append((parent[v], v))
                v = parent[v]
            path.reverse()
        return dist[sink], path

    def successive_shortest_paths(self, source, sink):
        # Initialize potentials to zero for all nodes
        potential = defaultdict(int)
        max_flow = 0
        min_cost = 0

        while True:
            distance, path = self.find_shortest_path(source, sink, potential)
            if not path or distance == self.inf:
                break  # No more augmenting path available

            # Find the minimum capacity along the path
            flow = min(self.adj_matrix[u][v].capacity - self.adj_matrix[u][v].flow for u, v in path)
            
            # Augment flow and update costs
            for u, v in path:
                self.adj_matrix[u][v].flow += flow
                # Update the reverse edge (for residual graph)
                if self.adj_matrix[v][u] is None:
                    self.adj_matrix[v][u] = Edge(0, 0, -self.adj_matrix[u][v].distance)
                self.adj_matrix[v][u].flow -= flow

            max_flow += flow
            min_cost += flow * distance

            # Update potentials
            for node in potential:
                if distance != self.inf:
                    potential[node] += distance

        return max_flow, min_cost

if __name__ == "__main__":
    # Load data
    graph = Graph()
    graph.load_data_from_excel("data/street_graph_data.xlsx")
    
    # Create MinCostMaxFlow instance and find the min-cost max flow
    mcmf = MinCostMaxFlow(graph)
    source = "(10.8000091, 106.6606224)"
    sink = "(10.7877414, 106.683245)"
    start_time = time.time()
    max_flow, min_cost = mcmf.successive_shortest_paths(source, sink)
    end_time = time.time()
    print(f"Maximum Flow: {max_flow}")
    print(f"Minimum Cost: {min_cost}")
    print("Duration:", end_time - start_time, "seconds")