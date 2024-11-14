from flask import Flask, request, jsonify, render_template
import json
import random
from graph import *
from edmonds_karp import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_route', methods=['POST'])
def find_route_api():
    data = request.json
    start_coords = data.get('start')
    end_coords = data.get('end')
    algorithm = data.get('algorithm')

    if not start_coords or not end_coords or not algorithm:
        return jsonify({"error": "Invalid input"}), 400

    print(algorithm)
    routes = None
    if algorithm == "1":
        graph = Graph()
        data = graph.load_data_from_excel("data/street_graph_data.xlsx")
        ek = EdmondsKarp(data)
        # result = ek.find_max_flow("(10.774706, 106.6995506)","(10.7740726, 106.6990186)")
        result = ek.find_max_flow(format_coordinates(start_coords), format_coordinates(end_coords))
        routes = format_result(result)

        print("completed")
    if routes==[]: routes = None
    log_data = {
        "start": start_coords,
        "end": end_coords,
        "algorithm": algorithm,
        "routes": routes
    }

    with open('route_log.json', 'w') as json_file:
        json.dump(log_data, json_file)
        json_file.write("\n")

    return jsonify({"routes": routes})

if __name__ == '__main__':
    app.run(debug=True)
