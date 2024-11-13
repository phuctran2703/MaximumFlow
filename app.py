from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_route', methods=['POST'])
def find_route_api():
    data = request.json
    start_coords = data.get('start') #['10.773358', '106.6611492']
    end_coords = data.get('end')
    algorithm = data.get('algorithm')

    print(start_coords)
    print(end_coords)
    print(algorithm)

    if not start_coords or not end_coords or not algorithm:
        return jsonify({"error": "Invalid input"}), 400

#################
    if algorithm == "1": pass

    route = [
    [10.774706, 106.6995506],
    [10.7756638, 106.7004291],
    [10.7768018, 106.6999227],
    [10.7758208, 106.6990461],
    [10.7748371, 106.6981499],
    [10.7739958, 106.697121],
    [10.7731556, 106.6976491],
    [10.7734407, 106.6981058],
    [10.7740726, 106.6990186]
]
##################

    log_data = {
        "start": start_coords,
        "end": end_coords,
        "algorithm": algorithm
    }

    with open('route_log.json', 'a') as json_file:
        json.dump(log_data, json_file)
        json_file.write("\n")  # Write a newline to separate records

    return jsonify({"route": route})  # Return JSON including coordinates

if __name__ == '__main__':
    app.run(debug=True)
