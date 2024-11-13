import pandas as pd
from collections import defaultdict

class Edge:
    def __init__(self, flow, capacity, distance):
        self.flow = flow
        self.capacity = capacity
        self.distance = distance


class Graph:
    def __init__(self):
        self.adj_matrix = defaultdict(lambda: defaultdict(lambda: None))

    def load_data_from_excel(self, file_name):
        df = pd.read_excel(file_name, usecols="B:G")
        df.fillna(0, inplace=True)
        for index, row in df.iterrows():
            self.adj_matrix[row["Column"]][row["Row"]] = Edge(row["Flow"],row["Capacity"],row["Distance"])
        
        print(f"Data has been loaded from {file_name}")
        return self.adj_matrix

    def load_data_from_csv(self, file_name):
        df = pd.read_csv(file_name, index_col=0, low_memory=False)

        for source in df.index:
            for target in df.columns:
                value = df.at[source, target]
                if pd.isna(value): continue
                flow, capacity, distance = map(float, value.split("/"))
                self.adj_matrix[source][target] = Edge(flow, capacity, distance)

        print(f"Data has been loaded from {file_name}")
        return self.adj_matrix

    def display(self):
        for src in self.adj_matrix:
            for dst in self.adj_matrix[src]:
                edge = self.adj_matrix[src][dst]
                if edge is not None:
                    print(f"Edge from {src} to {dst} -> Flow: {edge.flow}, Capacity: {edge.capacity}, Distance: {edge.distance}")

    def export_to_csv(self, file_name):
        coordinates = list(self.adj_matrix.keys())
        df = pd.DataFrame(index=coordinates, columns=coordinates)
        
        # Điền giá trị vào ma trận (Flow, Capacity, Distance)
        for source, targets in self.adj_matrix.items():
            for target, edge in targets.items():
                df.at[source, target] = f"{edge.flow}/{edge.capacity}/{edge.distance}"

        # Ghi DataFrame vào CSV
        df.to_csv(file_name)
        print(f"Data has been exported")

if __name__ == "__main__":
    graph = Graph()
    graph.load_data_from_csv("data/graph_matrix.csv")
    print(len(graph.adj_matrix))
    edge = graph.adj_matrix["(10.8032397, 106.6845465)"]["(10.8017564, 106.6830292)"]
    print(f"Flow: {edge.flow}, Capacity: {edge.capacity}, Distance: {edge.distance}")